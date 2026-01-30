"""
Board Router - Jinja2 템플릿 렌더링 방식
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_
from typing import Optional, List
import math
import os
from pathlib import Path

from database import get_db
#from models_freeboard import Board, BoardImg, BoardLike, Comment, Member
from models import Board, BoardImg, BoardLike, Comment, Member
from auth import get_current_user_optional

# Jinja2 템플릿
#from main import templates # ImportError: cannot import name 'templates' from partially initialized module 'main' (most likely due to a circular import) (/app/main.py)
from core.templates import templates

router = APIRouter(prefix="/board", tags=["게시판"])


# ============================================
# 게시판 목록 (Jinja2 렌더링)
# ============================================

@router.get("/list", response_class=HTMLResponse, name="board_list")
async def board_list_page(
    request: Request,
    page: int = Query(default=1, ge=1, description="페이지 번호"),
    limit: int = Query(default=7, ge=1, le=50, description="페이지당 개수"),
    keyword: Optional[str] = Query(default=None, description="검색 키워드"),
    search_type: str = Query(default="title", regex="^(title|content|author|all)$"),
    sort_by: str = Query(default="recent", regex="^(recent|views|likes)$"),
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    게시판 목록 페이지 (Jinja2 템플릿)
    """
    
    # 기본 쿼리 (자유게시판, 삭제되지 않은 글)
    query = db.query(Board).filter(
        Board.board_code == 3,
        Board.board_del_fl == 'N'
    ).options(joinedload(Board.author))
    
    # 검색 조건
    if keyword:
        if search_type == "title":
            query = query.filter(Board.board_title.like(f"%{keyword}%"))
        elif search_type == "content":
            query = query.filter(Board.board_content.like(f"%{keyword}%"))
        elif search_type == "author":
            query = query.join(Member).filter(Member.member_nickname.like(f"%{keyword}%"))
        elif search_type == "all":
            query = query.join(Member).filter(
                or_(
                    Board.board_title.like(f"%{keyword}%"),
                    Board.board_content.like(f"%{keyword}%"),
                    Member.member_nickname.like(f"%{keyword}%")
                )
            )
    
    # 전체 개수
    total = query.count()
    
    # 정렬
    if sort_by == "recent":
        query = query.order_by(desc(Board.b_create_date))
    elif sort_by == "views":
        query = query.order_by(desc(Board.board_count))
    elif sort_by == "likes":
        like_count_subquery = db.query(
            BoardLike.board_no,
            func.count(BoardLike.member_no).label('like_count')
        ).group_by(BoardLike.board_no).subquery()
        
        query = query.outerjoin(
            like_count_subquery,
            Board.board_no == like_count_subquery.c.board_no
        ).order_by(desc(like_count_subquery.c.like_count))
    
    # 페이징
    offset = (page - 1) * limit
    boards = query.offset(offset).limit(limit).all()
    
    # 각 게시글에 통계 정보 추가
    board_list = []
    for board in boards:
        # 썸네일
        thumbnail = None
        first_image = db.query(BoardImg).filter(
            BoardImg.board_no == board.board_no,
            BoardImg.img_order == 0
        ).first()
        if first_image:
            thumbnail = f"/uploads{first_image.img_path}"
        
        # 좋아요 개수
        like_count = db.query(func.count(BoardLike.member_no)).filter(
            BoardLike.board_no == board.board_no
        ).scalar() or 0
        
        # 댓글 개수
        comment_count = db.query(func.count(Comment.comment_no)).filter(
            Comment.board_no == board.board_no,
            Comment.comment_del_fl == 'N'
        ).scalar() or 0
        
        board_list.append({
            'board': board,
            'thumbnail': thumbnail,
            'like_count': like_count,
            'comment_count': comment_count
        })
    
    # 총 페이지 수
    total_pages = math.ceil(total / limit) if total > 0 else 0
    
    # 페이지 번호 리스트 (최대 10개)
    start_page = max(1, page - 4)
    end_page = min(total_pages, start_page + 9)
    page_numbers = list(range(start_page, end_page + 1))
    
    # 템플릿 렌더링
    return templates.TemplateResponse("board/freeboardList.html", {
        "request": request,
        "current_user": current_user,
        "board_list": board_list,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "page_numbers": page_numbers,
        "keyword": keyword or "",
        "search_type": search_type,
        "sort_by": sort_by
    })


# ============================================
# 게시글 상세 (Jinja2 렌더링)
# ============================================

@router.get("/{board_no}", response_class=HTMLResponse, name="board_detail")
async def board_detail_page(
    request: Request,
    board_no: int,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    게시글 상세 페이지 (Jinja2 템플릿)
    """
    
    # 게시글 조회
    board = db.query(Board).options(
        joinedload(Board.author),
        joinedload(Board.images)
    ).filter(
        Board.board_no == board_no,
        Board.board_del_fl == 'N'
    ).first()
    
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    
    # 조회수 증가
    board.board_count += 1
    db.commit()
    
    # 이미지 목록
    images = sorted(board.images, key=lambda x: x.img_order)
    image_list = [f"/uploads{img.img_path}" for img in images]
    
    # 좋아요 개수
    like_count = db.query(func.count(BoardLike.member_no)).filter(
        BoardLike.board_no == board_no
    ).scalar() or 0
    
    # 현재 사용자 좋아요 여부
    is_liked = False
    if current_user:
        is_liked = db.query(BoardLike).filter(
            BoardLike.board_no == board_no,
            BoardLike.member_no == current_user['memberNo']
        ).first() is not None
    
    # 댓글 개수
    comment_count = db.query(func.count(Comment.comment_no)).filter(
        Comment.board_no == board_no,
        Comment.comment_del_fl == 'N'
    ).scalar() or 0
    
    # 작성자 여부
    is_author = current_user and current_user['memberNo'] == board.member_no
    
    # 템플릿 렌더링
    return templates.TemplateResponse("board/freeboardDetail.html", {
        "request": request,
        "current_user": current_user,
        "board": board,
        "images": image_list,
        "like_count": like_count,
        "is_liked": is_liked,
        "comment_count": comment_count,
        "is_author": is_author
    })


# ============================================
# 게시글 작성 페이지 (다음 단계)
# ============================================

@router.get("/write", response_class=HTMLResponse, name="board_write_page")
async def board_write_page(
    request: Request,
    current_user = Depends(get_current_user_optional)
):
    """게시글 작성 페이지 - 다음 단계에서 구현"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    return templates.TemplateResponse("board/freeboardWrite.html", {
        "request": request,
        "current_user": current_user
    })
