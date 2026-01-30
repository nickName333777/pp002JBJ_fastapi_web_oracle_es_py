"""
Board Router - 자유게시판 API
게시글 CRUD, 댓글, 좋아요 기능
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, or_
from typing import Optional
import math

from database import get_db
#from models_freeboard import Board, BoardImg, BoardLike, Comment, Member
from models import Board, BoardImg, BoardLike, Comment, Member
from board_schemas import (
    BoardCreate, BoardUpdate, BoardDetailResponse, BoardListResponse,
    BoardListItem, BoardAuthorResponse, BoardImageResponse, MessageResponse
)
from auth import get_current_user

router = APIRouter(prefix="/api/board/freeboard", tags=["자유게시판"])


# ============================================
# 게시글 목록 조회
# ============================================

@router.get("/list", response_model=BoardListResponse)
async def get_board_list(
    page: int = Query(default=1, ge=1, description="페이지 번호"),
    limit: int = Query(default=10, ge=1, le=50, description="페이지당 개수"),
    keyword: Optional[str] = Query(default=None, description="검색 키워드"),
    search_type: str = Query(default="title", regex="^(title|content|author|all)$", description="검색 타입"),
    sort_by: str = Query(default="recent", regex="^(recent|views|likes)$", description="정렬 기준"),
    db: Session = Depends(get_db)
):
    """
    자유게시판 목록 조회 (페이징, 검색, 정렬)
    
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 게시글 개수 (기본 10, 최대 50)
    - **keyword**: 검색 키워드
    - **search_type**: 검색 타입 (title, content, author, all)
    - **sort_by**: 정렬 기준 (recent:최신순, views:조회수순, likes:좋아요순)
    """
    
    # 기본 쿼리 (삭제되지 않은 자유게시판 게시글만)
    query = db.query(Board).filter(
        Board.board_code == 3,
        Board.board_del_fl == 'N'
    )
    
    # 검색 조건 추가
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
    
    # 전체 개수 조회
    total = query.count()
    
    # 정렬
    if sort_by == "recent":
        query = query.order_by(desc(Board.b_create_date))
    elif sort_by == "views":
        query = query.order_by(desc(Board.board_count))
    elif sort_by == "likes":
        # 좋아요 개수로 정렬 (서브쿼리 사용)
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
    
    # 응답 데이터 구성
    board_items = []
    for board in boards:
        # 작성자 정보
        author_data = BoardAuthorResponse(
            member_no=board.author.member_no,
            member_nickname=board.author.member_nickname,
            profile_img=board.author.profile_img,
            member_level_no=board.author.member_level_no
        )
        
        # 썸네일 (첫 번째 이미지)
        thumbnail = None
        if board.images:
            first_image = next((img for img in board.images if img.img_order == 0), None)
            if first_image:
                thumbnail = first_image.img_path
        
        # 좋아요 개수
        like_count = db.query(func.count(BoardLike.member_no)).filter(
            BoardLike.board_no == board.board_no
        ).scalar() or 0
        
        # 댓글 개수
        comment_count = db.query(func.count(Comment.comment_no)).filter(
            Comment.board_no == board.board_no,
            Comment.comment_del_fl == 'N'
        ).scalar() or 0
        
        board_items.append(BoardListItem(
            board_no=board.board_no,
            board_title=board.board_title,
            board_count=board.board_count,
            b_create_date=board.b_create_date,
            author=author_data,
            thumbnail=thumbnail,
            like_count=like_count,
            comment_count=comment_count
        ))
    
    # 총 페이지 수 계산
    total_pages = math.ceil(total / limit) if total > 0 else 0
    
    return BoardListResponse(
        boards=board_items,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


# ============================================
# 게시글 상세 조회
# ============================================

@router.get("/{board_no}", response_model=BoardDetailResponse)
async def get_board_detail(
    board_no: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    게시글 상세 조회
    
    - 조회수 자동 증가
    - 작성자 정보, 이미지, 좋아요 수, 댓글 수 포함
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
    
    # 작성자 정보
    author_data = BoardAuthorResponse(
        member_no=board.author.member_no,
        member_nickname=board.author.member_nickname,
        profile_img=board.author.profile_img,
        member_level_no=board.author.member_level_no
    )
    
    # 이미지 목록 (img_order 순서대로 정렬)
    images = [
        BoardImageResponse(
            img_no=img.img_no,
            img_path=img.img_path,
            img_orig=img.img_orig,
            img_rename=img.img_rename,
            img_order=img.img_order
        )
        for img in sorted(board.images, key=lambda x: x.img_order)
    ]
    
    # 좋아요 개수
    like_count = db.query(func.count(BoardLike.member_no)).filter(
        BoardLike.board_no == board_no
    ).scalar() or 0
    
    # 현재 사용자가 좋아요 눌렀는지 확인
    is_liked = db.query(BoardLike).filter(
        BoardLike.board_no == board_no,
        BoardLike.member_no == current_user['memberNo']
    ).first() is not None
    
    # 댓글 개수
    comment_count = db.query(func.count(Comment.comment_no)).filter(
        Comment.board_no == board_no,
        Comment.comment_del_fl == 'N'
    ).scalar() or 0
    
    return BoardDetailResponse(
        board_no=board.board_no,
        board_title=board.board_title,
        board_content=board.board_content,
        board_count=board.board_count,
        b_create_date=board.b_create_date,
        b_update_date=board.b_update_date,
        author=author_data,
        images=images,
        like_count=like_count,
        is_liked=is_liked,
        comment_count=comment_count
    )


# ============================================
# 게시글 작성 (다음 단계에서 구현)
# ============================================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_board(
    board_data: BoardCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시글 작성 (이미지 업로드 포함) - 다음 단계에서 구현"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="게시글 작성 기능은 다음 단계에서 구현됩니다."
    )


# ============================================
# 게시글 수정 (다음 단계에서 구현)
# ============================================

@router.put("/{board_no}")
async def update_board(
    board_no: int,
    board_data: BoardUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시글 수정 - 다음 단계에서 구현"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="게시글 수정 기능은 다음 단계에서 구현됩니다."
    )


# ============================================
# 게시글 삭제 (다음 단계에서 구현)
# ============================================

@router.delete("/{board_no}")
async def delete_board(
    board_no: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시글 삭제 (소프트 삭제) - 다음 단계에서 구현"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="게시글 삭제 기능은 다음 단계에서 구현됩니다."
    )
