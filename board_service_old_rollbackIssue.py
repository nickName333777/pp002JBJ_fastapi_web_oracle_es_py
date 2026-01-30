"""
Board Service - 게시글 비즈니스 로직
이미지 업로드 포함
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from models_freeboard import Board, BoardImg
from utils import Util
from exceptions import (
    FileUploadException, 
    InvalidFileExtensionException, 
    FileSizeLimitException,
    NotFoundException
)
from dotenv import load_dotenv # 로컬 개발일때  + .env 사용
# load_dotenv()  # .env → OS 환경변수로 로드; 앱 시작 시 한 번만, 보통 config.py에서 처리
# .env 파일 명시적 로드 (최우선)
load_dotenv(override=True)

class BoardService:
    """게시판 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # 환경 변수에서 설정 가져오기
        self.upload_dir = os.getenv("UPLOAD_DIR", "/mnt/user-data/uploads")
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.max_images = int(os.getenv("MAX_IMAGES_PER_POST", "5"))
        self.allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,webp").split(",")
    
    
    def create_board(
        self, 
        board_title: str,
        board_content: str,
        member_no: int,
        board_code: int = 3,
        images: List[UploadFile] = None
    ) -> Board:
        """
        게시글 작성
        
        Args:
            board_title: 제목
            board_content: 내용 (XSS 처리)
            member_no: 작성자 번호
            board_code: 게시판 코드 (기본값: 3 = 자유게시판)
            images: 업로드 이미지 파일 리스트 (최대 5개)
            
        Returns:
            생성된 Board 객체
            
        Raises:
            FileUploadException: 파일 업로드 실패
            InvalidFileExtensionException: 잘못된 파일 확장자
            FileSizeLimitException: 파일 크기 초과
        """
        try:
            # 1. XSS 방지 처리
            board_title = Util.xss_handling(board_title)
            board_content = Util.xss_handling(board_content)
            
            # 2. 게시글 DB 저장
            new_board = Board(
                board_title=board_title,
                board_content=board_content,
                board_code=board_code,
                member_no=member_no
            )
            
            self.db.add(new_board)
            self.db.flush()  # board_no 생성을 위해 flush
            
            # 3. 이미지 업로드 처리
            if images:
                self._upload_images(new_board.board_no, images)
            
            # 4. 커밋
            self.db.commit() # Exception 발생시 transactional(rollback)을 여기서 처리?
            self.db.refresh(new_board)
            
            return new_board
        
        except Exception as e:
            self.db.rollback()   # Exception 발생시 transactional(rollback)처리
            raise e              # 예외는 상위로 전달    
    
    def _upload_images(self, board_no: int, images: List[UploadFile]) -> List[BoardImg]:
        """
        게시글 이미지 업로드
        
        Args:
            board_no: 게시글 번호
            images: 업로드 파일 리스트
            
        Returns:
            생성된 BoardImg 객체 리스트
            
        Raises:
            FileUploadException: 파일 업로드 실패
            InvalidFileExtensionException: 잘못된 확장자
            FileSizeLimitException: 파일 크기 초과
        """
        
        # 이미지 개수 검증
        if len(images) > self.max_images:
            raise FileUploadException(f"이미지는 최대 {self.max_images}개까지 업로드 가능합니다.")
        
        board_images = []
        
        for idx, image in enumerate(images):
            # 파일명 안전하게 처리
            original_filename = Util.sanitize_filename(image.filename)
            
            # 확장자 검증
            if not Util.validate_image_extension(original_filename, self.allowed_extensions):
                raise InvalidFileExtensionException(
                    f"허용되지 않은 파일 형식입니다. ({original_filename})"
                )
            
            # 파일 크기 검증
            if image.size and image.size > self.max_file_size:
                max_mb = self.max_file_size / (1024 * 1024)
                raise FileSizeLimitException(
                    f"파일 크기는 {max_mb}MB를 초과할 수 없습니다. ({original_filename})"
                )
            
            # 파일명 변경 (중복 방지)
            renamed_filename = Util.file_rename_uuid(original_filename)
            
            # 저장 경로 생성
            save_dir = Path(self.upload_dir) / "boards" / str(board_no)
            save_dir.mkdir(parents=True, exist_ok=True)
            
            save_path = save_dir / renamed_filename
            
            try:
                # 파일 저장
                with save_path.open("wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                
                # DB에 이미지 정보 저장
                board_img = BoardImg(
                    img_path=f"/boards/{board_no}/{renamed_filename}",
                    img_orig=original_filename,
                    img_rename=renamed_filename,
                    img_order=idx,  # 0: 썸네일, 1~4: 서브 이미지
                    board_no=board_no
                )
                
                self.db.add(board_img)
                board_images.append(board_img)
                
            except Exception as e:
                # 업로드 실패 시 이미 저장된 파일 삭제
                if save_path.exists():
                    save_path.unlink()
                raise FileUploadException(f"파일 업로드 중 오류 발생: {str(e)}")
        
        return board_images
    
    
    def update_board(
        self,
        board_no: int,
        board_title: str,
        board_content: str,
        member_no: int,
        delete_image_orders: List[int] = None,
        new_images: List[UploadFile] = None
    ) -> Board:
        """
        게시글 수정
        
        Args:
            board_no: 게시글 번호
            board_title: 수정할 제목
            board_content: 수정할 내용
            member_no: 수정 요청자 (권한 검증용)
            delete_image_orders: 삭제할 이미지 순서 리스트
            new_images: 새로 추가할 이미지 리스트
            
        Returns:
            수정된 Board 객체
            
        Raises:
            NotFoundException: 게시글 없음
            ForbiddenException: 권한 없음
        """
        from exceptions import ForbiddenException
        from datetime import datetime
        
        # 게시글 조회
        board = self.db.query(Board).filter(
            Board.board_no == board_no,
            Board.board_del_fl == 'N'
        ).first()
        
        if not board:
            raise NotFoundException("게시글을 찾을 수 없습니다.")
        
        # 작성자 확인
        if board.member_no != member_no:
            raise ForbiddenException("게시글을 수정할 권한이 없습니다.")
        
        # 제목/내용 업데이트 (XSS 처리)
        board.board_title = Util.xss_handling(board_title)
        board.board_content = Util.xss_handling(board_content)
        board.b_update_date = datetime.now()
        
        # 이미지 삭제 처리
        if delete_image_orders:
            self._delete_images(board_no, delete_image_orders)
        
        # 새 이미지 추가
        if new_images:
            # 현재 이미지 개수 확인
            current_count = self.db.query(BoardImg).filter(
                BoardImg.board_no == board_no
            ).count()
            
            if current_count + len(new_images) > self.max_images:
                raise FileUploadException(
                    f"이미지는 최대 {self.max_images}개까지 가능합니다."
                )
            
            # 새 이미지 순서 계산 (기존 이미지 다음부터)
            max_order = self.db.query(BoardImg).filter(
                BoardImg.board_no == board_no
            ).count()
            
            # 이미지 업로드 (순서 재조정)
            for idx, image in enumerate(new_images):
                self._upload_single_image(board_no, image, max_order + idx)
        
        self.db.commit() # Exceptionb 발생시 transactional(rollback)을 여기서 처리?
        self.db.refresh(board)
        
        return board
    
    
    def _upload_single_image(self, board_no: int, image: UploadFile, order: int) -> BoardImg:
        """단일 이미지 업로드"""
        original_filename = Util.sanitize_filename(image.filename)
        
        if not Util.validate_image_extension(original_filename, self.allowed_extensions):
            raise InvalidFileExtensionException(f"허용되지 않은 파일 형식입니다.")
        
        renamed_filename = Util.file_rename_uuid(original_filename)
        save_dir = Path(self.upload_dir) / "boards" / str(board_no)
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / renamed_filename
        
        try:
            with save_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            board_img = BoardImg(
                img_path=f"/boards/{board_no}/{renamed_filename}",
                img_orig=original_filename,
                img_rename=renamed_filename,
                img_order=order,
                board_no=board_no
            )
            
            self.db.add(board_img)
            return board_img
            
        except Exception as e:
            if save_path.exists():
                save_path.unlink()
            raise FileUploadException(f"파일 업로드 실패: {str(e)}")
    
    
    def _delete_images(self, board_no: int, image_orders: List[int]):
        """
        이미지 삭제 (DB + 파일 시스템)
        
        Args:
            board_no: 게시글 번호
            image_orders: 삭제할 이미지 순서 리스트
        """
        from exceptions import ImageDeleteException
        
        images = self.db.query(BoardImg).filter(
            BoardImg.board_no == board_no,
            BoardImg.img_order.in_(image_orders)
        ).all()
        
        for image in images:
            # 파일 삭제
            file_path = Path(self.upload_dir) / image.img_path.lstrip("/")
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception as e:
                raise ImageDeleteException(f"이미지 파일 삭제 실패: {str(e)}")
            
            # DB 삭제
            self.db.delete(image)
