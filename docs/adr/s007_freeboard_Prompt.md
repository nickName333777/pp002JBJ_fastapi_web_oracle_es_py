###[old] 친구야, 이번 단계에서는 자유게시판 기능을 FastAPI 기반으로 옮겨왔으면 좋겠어서, 아래 1, 2, 3번으로 이와 관련한 요청내용과 관련화일을 구성해 보았어. 완벽하지 않은 부분들은 네가 추가로 보충해서 구현해주고 자세한 설명을 첨부해줘.

친구야, 이번 단계에서는 자유게시판 기능을 FastAPI 기반으로 옮겨왔으면 좋겠어서, 아래 1번 데이터베이스 작업, 2번 frontend 작업(게시판 기능별 html, css, js), 3번 backend작업(controller, service, modelDTO)으로 이와 관련한 요청내용과 관련화일을 구성해 보았는데, 용량이 커서  1, 2, 3 번을 다시 순차적으로 진행하도록 할께. 완벽하지 않은 부분들은 네가 추가로 보충해서 구현해주고 자세한 설명을 첨부해줘.


1. 자유게시판 기능에 필요한 오라클 DB의 해당 테이블들(BOARDTYPE, BOARD, BOARD_IMG, BOARD_LIKE, COMMENT)은 다음과 같이 ERD에서 정의했어. BOARDTYPE, BOARD, BOARD_IMG, BOARD_LIKE, COMMENT테이블들을 생성하고, 또 자유게시판 기능에 맞는 myBatis용 DTO들(BoardTypeDB, BoardDB, Freeboard, BoardImgDB, BoardLikeDB, CommnetDB, CommentFB, PaginationFB)를 아래처럼 생성했는데, 이걸 아래 3번에 첨부한 컨트롤러 로직과 함께 FastAPI백엔드에 맞게 바꿔줘.
자유게시판은 BOARDTYPE 테이블에서 BOARD_CODE=3 번이야. 

DROP TABLE "BOARD_IMG";
DROP TABLE "BOARD_LIKE";
DROP TABLE "COMMENT";
DROP TABLE "BOARD";
DROP TABLE "BOARDTYPE";

CREATE TABLE "BOARDTYPE" (
   "BOARD_CODE"   NUMBER      NOT NULL,
   "BOARD_NAME"   VARCHAR2(20)      NOT NULL,
   "PARENTS_BOARD_CODE"   NUMBER      NULL
);
COMMENT ON COLUMN "BOARDTYPE"."BOARD_CODE" IS '게시판코드';
COMMENT ON COLUMN "BOARDTYPE"."BOARD_NAME" IS '게시판이름';
COMMENT ON COLUMN "BOARDTYPE"."PARENTS_BOARD_CODE" IS '게시판코드';

ALTER TABLE "BOARDTYPE" ADD CONSTRAINT "PK_BOARDTYPE" PRIMARY KEY (
   "BOARD_CODE"
);
ALTER TABLE "BOARDTYPE" ADD CONSTRAINT "FK_BOARDTYPE_TO_BOARDTYPE_1" FOREIGN KEY (
   "PARENTS_BOARD_CODE"
)
REFERENCES "BOARDTYPE" (
   "BOARD_CODE"
);


CREATE TABLE "BOARD" (
   "BOARD_NO"   NUMBER      NOT NULL,
   "BOARD_TITLE"   VARCHAR2(300)      NOT NULL,
   "BOARD_CONTENT"   CLOB      NOT NULL,
   "B_CREATE_DATE"   DATE   DEFAULT SYSDATE   NOT NULL,
   "B_UPDATE_DATE"   DATE      NULL,
   "BOARD_COUNT"   NUMBER   DEFAULT 0   NOT NULL,
   "BOARD_DEL_FL"   CHAR(1)   DEFAULT 'N'   NOT NULL,
   "BOARD_CODE"   NUMBER      NOT NULL,
   "MEMBER_NO"   NUMBER      NOT NULL,
   "NEWS_REPORTER"   VARCHAR2(100)      NULL
);
COMMENT ON COLUMN "BOARD"."BOARD_NO" IS '게시글번호(SEQ_BOARD_NO)';
COMMENT ON COLUMN "BOARD"."BOARD_TITLE" IS '게시글제목';
COMMENT ON COLUMN "BOARD"."BOARD_CONTENT" IS '게시글내용';
COMMENT ON COLUMN "BOARD"."B_CREATE_DATE" IS '게시글작성일';
COMMENT ON COLUMN "BOARD"."B_UPDATE_DATE" IS '게시글최종수정일';
COMMENT ON COLUMN "BOARD"."BOARD_COUNT" IS '게시글조회수';
COMMENT ON COLUMN "BOARD"."BOARD_DEL_FL" IS '게시글삭제여부';
COMMENT ON COLUMN "BOARD"."BOARD_CODE" IS '게시판코드';
COMMENT ON COLUMN "BOARD"."MEMBER_NO" IS '회원번호';
COMMENT ON COLUMN "BOARD"."NEWS_REPORTER" IS '기자명';

ALTER TABLE "BOARD" ADD CONSTRAINT "PK_BOARD" PRIMARY KEY (
   "BOARD_NO"
);
ALTER TABLE "BOARD" ADD CONSTRAINT "FK_BOARDTYPE_TO_BOARD_1" FOREIGN KEY (
   "BOARD_CODE"
)
REFERENCES "BOARDTYPE" (
   "BOARD_CODE"
);
ALTER TABLE "BOARD" ADD CONSTRAINT "FK_MEMBER_TO_BOARD_1" FOREIGN KEY (
   "MEMBER_NO"
)
REFERENCES "MEMBER" (
   "MEMBER_NO"
);


CREATE TABLE "BOARD_IMG" (
   "IMG_NO"   NUMBER      NOT NULL,
   "IMG_PATH"   VARCHAR2(500)      NOT NULL,
   "IMG_ORIG"   VARCHAR2(200)      NULL,
   "IMG_RENAME"   VARCHAR2(200)      NULL,
   "IMG_ORDER"   NUMBER      NOT NULL,
   "BOARD_NO"   NUMBER      NOT NULL
);
COMMENT ON COLUMN "BOARD_IMG"."IMG_NO" IS '이미지번호(SEQ_IMAGE_NO)';
COMMENT ON COLUMN "BOARD_IMG"."IMG_PATH" IS '이미지경로';
COMMENT ON COLUMN "BOARD_IMG"."IMG_ORIG" IS '원본이미지명';
COMMENT ON COLUMN "BOARD_IMG"."IMG_RENAME" IS '변경이미지명';
COMMENT ON COLUMN "BOARD_IMG"."IMG_ORDER" IS '이미지파일순서번호';
COMMENT ON COLUMN "BOARD_IMG"."BOARD_NO" IS '게시글번호(SEQ_BOARD_NO)';

ALTER TABLE "BOARD_IMG" ADD CONSTRAINT "PK_BOARD_IMG" PRIMARY KEY (
   "IMG_NO"
);
ALTER TABLE "BOARD_IMG" ADD CONSTRAINT "FK_BOARD_TO_BOARD_IMG_1" FOREIGN KEY (
   "BOARD_NO"
)
REFERENCES "BOARD" (
   "BOARD_NO"
);



CREATE TABLE "BOARD_LIKE" (
   "BOARD_NO"   NUMBER      NOT NULL,
   "MEMBER_NO"   NUMBER      NOT NULL
);
COMMENT ON COLUMN "BOARD_LIKE"."BOARD_NO" IS '게시글번호(SEQ_BOARD_NO)';
COMMENT ON COLUMN "BOARD_LIKE"."MEMBER_NO" IS '회원번호(SEQ_MEMBER_NO)';

ALTER TABLE "BOARD_LIKE" ADD CONSTRAINT "PK_BOARD_LIKE" PRIMARY KEY (
   "BOARD_NO",
   "MEMBER_NO"
);
ALTER TABLE "BOARD_LIKE" ADD CONSTRAINT "FK_BOARD_TO_BOARD_LIKE_1" FOREIGN KEY (
   "BOARD_NO"
)
REFERENCES "BOARD" (
   "BOARD_NO"
);
ALTER TABLE "BOARD_LIKE" ADD CONSTRAINT "FK_MEMBER_TO_BOARD_LIKE_1" FOREIGN KEY (
   "MEMBER_NO"
)
REFERENCES "MEMBER" (
   "MEMBER_NO"
);



CREATE TABLE "COMMENT" (
   "COMMENT_NO"   NUMBER      NOT NULL,
   "MEMBER_NO"   NUMBER      NOT NULL,
   "BOARD_NO"   NUMBER      NOT NULL,
   "PARENTS_COMMENT_NO"   NUMBER      NULL,
   "C_CREATE_DATE"   DATE   DEFAULT SYSDATE   NULL,
   "COMMENT_CONTENT"   VARCHAR2(2000)      NOT NULL,
   "COMMENT_DEL_FL"   CHAR(1)   DEFAULT 'N'   NOT NULL,
   "SECRET_YN"   CHAR(1)   DEFAULT 'N'   NOT NULL,
   "MODIFY_YN"   CHAR(1)   DEFAULT 'N'   NOT NULL
);
COMMENT ON COLUMN "COMMENT"."COMMENT_NO" IS '댓글번호(SEQ_COMMENT_NO)';
COMMENT ON COLUMN "COMMENT"."MEMBER_NO" IS '회원번호';
COMMENT ON COLUMN "COMMENT"."BOARD_NO" IS '게시글번호';
COMMENT ON COLUMN "COMMENT"."PARENTS_COMMENT_NO" IS '부모 댓글 번호';
COMMENT ON COLUMN "COMMENT"."C_CREATE_DATE" IS '댓글작성일';
COMMENT ON COLUMN "COMMENT"."COMMENT_CONTENT" IS '댓글내용';
COMMENT ON COLUMN "COMMENT"."COMMENT_DEL_FL" IS '댓글삭제여부(N: 삭제X, Y:삭제0)';
COMMENT ON COLUMN "COMMENT"."SECRET_YN" IS '비밀글 여부';
COMMENT ON COLUMN "COMMENT"."MODIFY_YN" IS '수정여부';

ALTER TABLE "COMMENT" ADD CONSTRAINT "PK_COMMENT" PRIMARY KEY (
   "COMMENT_NO"
);
ALTER TABLE "COMMENT" ADD CONSTRAINT "FK_MEMBER_TO_COMMENT_1" FOREIGN KEY (
   "MEMBER_NO"
)
REFERENCES "MEMBER" (
   "MEMBER_NO"
);
ALTER TABLE "COMMENT" ADD CONSTRAINT "FK_BOARD_TO_COMMENT_1" FOREIGN KEY (
   "BOARD_NO"
)
REFERENCES "BOARD" (
   "BOARD_NO"
);
ALTER TABLE "COMMENT" ADD CONSTRAINT "FK_COMMENT_TO_COMMENT_1" FOREIGN KEY (
   "PARENTS_COMMENT_NO"
)
REFERENCES "COMMENT" (
   "COMMENT_NO"
);


DROP SEQUENCE SEQ_COMMENT_NO; 
CREATE SEQUENCE SEQ_COMMENT_NO START WITH 1 NOCACHE;
 
DROP SEQUENCE SEQ_BOARD_NO; 
CREATE SEQUENCE SEQ_BOARD_NO START WITH 1 NOCACHE;
 
DROP SEQUENCE SEQ_IMAGE_NO; 
CREATE SEQUENCE SEQ_IMAGE_NO START WITH 1 NOCACHE;
 
 COMMIT;



package com.devlog.project.board.freeboard.model.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class BoardTypeDB {
    // 게시판코드 
    private Integer boardCode;

    // 게시판이름 
    private String boardName;

    // 부모 게시판 코드 
    private Integer parentsBoardCode;
}


package com.devlog.project.board.freeboard.model.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class BoardDB {
	
    // 게시글번호 
    private Long boardNo;

    // 게시글 제목 
    private String boardTitle;

    // 게시글 내용 
    private String boardContent;

    // 작성일   
    private String bCreateDate;

    // 수정일 
    private String bUpdateDate;

    // 조회수 
    private int boardCount;

    // 삭제 여부 (Y/N) 
    private String boardDelFl;

    // 게시판 코드 
    private Integer boardCode;

    // 작성자 회원번호 
    private Long memberNo;

    // 기자명 (뉴스 게시판용) 
    private String newsReporter;

}



package com.devlog.project.board.freeboard.model.dto;


import java.util.ArrayList;
import java.util.List; 

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class Freeboard {
	private Long boardNo;
	private String boardTitle;
	private String boardContent;
	private String bCreateDate; // LocalDateTime?
	private String bUpdateDate; // LocalDateTime?
	private int boardCount; // 조회수, readCount
	private String boardDelFl;
	private int boardCode; // 3:자유게시판
	
	
	// 서브쿼리 (상세 페이지용 추가 필드)
	private int likeCount;         // 좋아요 개수
	private int commentCount;      // 댓글 개수	
	
	
	// 회원 join
	private Long memberNo;
	private String memberNickname; 
	private String profileImg;
	private String thumbnail;
	
	// 이미지 목록
	private List<BoardImgDB> imageList;

	// 댓글 목록
	private List<CommentDB> commentList;
	
	// null 방어, 2026/01/09
	public void setImageList(List<BoardImgDB> imageList) {
	    this.imageList = (imageList == null)
	        ? new ArrayList <>()
	        : imageList;
	}	
	
	//
	public void setCommnetList(List<CommentDB> commentList) {
	    this.commentList = (commentList == null)
	        ? new ArrayList <>()
	        : commentList;
	}		
}


package com.devlog.project.board.freeboard.model.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class BoardImgDB {
	
    private Long imgNo;
    private String imgPath;
    private String imgOrig;
    private String imgRename;
    private int imgOrder;
    private Long boardNo;
}


package com.devlog.project.board.freeboard.model.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class BoardLikeDB {

    private Long boardNo;
    private Long memberNo;
}


package com.devlog.project.board.freeboard.model.dto;

import java.util.List;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class CommentDB {
	
	// 댓글 번호 
    private Long commentNo;

    // 회원 번호 
    private Long memberNo;

    // 게시글 번호 
    private Long boardNo;

    // 부모 댓글 번호 
    private Long parentsCommentNo;

    // 작성일  
    private String cCreateDate;

    // 댓글 내용 
    private String commentContent;

    // 삭제 여부 (Y/N) 
    private String commentDelFl;

    // 비밀글 여부 (Y/N) 
    private String secretYn;

    // 수정 여부 (Y/N) 
    private String modifyYn;

}




package com.devlog.project.board.freeboard.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class CommentFB {

	@JsonProperty("commentNo") 
	private Long commentNo;
	
	@JsonProperty("memberNo")
	private Long memberNo;
	
	@JsonProperty("boardNo")
	private Long boardNo;
	
	@JsonProperty("parentsCommentNo")
	private Long parentsCommentNo;
	
	@JsonProperty("cCreateDate")
	private String cCreateDate;
	
	@JsonProperty("commentContent")
	private String commentContent;
	
	@JsonProperty("commentDelFl")
	private String commentDelFl;
	
	@JsonProperty("secretYn")
	private String secretYn;
	
	@JsonProperty("modifyYn")
	private String modifyYn;
	
	@JsonProperty("memberNickname")
	private String memberNickname;
	
	@JsonProperty("profileImg")
	private String profileImg;
}


package com.devlog.project.board.freeboard.model.dto;

/*
프론트(JSP/Thymeleaf)에서 사용하는 값들(PaginationFB 으로 인해 바로 사용 가능)
pagination.currentPage
pagination.startPage
pagination.endPage
pagination.prevPage
pagination.nextPage
pagination.maxPage
 */

public class PaginationFB { //
	// 페이지네이션(페이징 처리)에 필요한 모든 값을 저장하고 있는 객체

	// fields
	private int currentPage;      // 현재 페이지 
	private int listCount;         // 전체 게시글 수 

	private int limit = 7;         // 한 페이지에 보여질 게시글 수, "고정"
	private int pageSize = 10;       // 목록 하단 페이지 번호의 노출 개수 

	
	private int maxPage;         // 제일 큰 페이지 번호 == 마지막 페이지 번호
	private int startPage;         // 목록 하단에 노출된 페이지의 시작 번호
	private int endPage;         // 목록 하단에 노출된 페이지의 끝 번호

	private int prevPage;         // 목록 하단에 노출된 번호의 이전 목록 끝 번호
	private int nextPage;         // 목록 하단에 노출된 번호의 다음 목록 시작 번호
	
	// 생성자
	public PaginationFB(int currentPage, int listCount) {
		this.currentPage = currentPage; // 현재 페이지
		this.listCount = listCount; // 전체 게시글 수
		
		calculatePagination(); // 계산 메소드 호출
	}

	public int getCurrentPage() {
		return currentPage;
	}

	public void setCurrentPage(int currentPage) {
		this.currentPage = currentPage;
		calculatePagination(); // 계산 메소드 호출 
	}

	public int getListCount() {
		return listCount;
	}

	public void setListCount(int listCount) {
		this.listCount = listCount;
		calculatePagination(); // 계산 메소드 호출
	}

	public int getLimit() {
		return limit;
	}

	public void setLimit(int limit) {
		this.limit = limit;
		calculatePagination(); // 계산 메소드 호출
	}

	public int getPageSize() {
		return pageSize;
	}

	public void setPageSize(int pageSize) {
		this.pageSize = pageSize;
		calculatePagination(); // 계산 메소드 호출
	}

	public int getMaxPage() {
		return maxPage;
	}

	public void setMaxPage(int maxPage) {
		this.maxPage = maxPage;
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public int getPrevPage() {
		return prevPage;
	}

	public void setPrevPage(int prevPage) {
		this.prevPage = prevPage;
	}

	public int getNextPage() {
		return nextPage;
	}

	public void setNextPage(int nextPage) {
		this.nextPage = nextPage;
	}

	@Override
	public String toString() {
		return "Pagination [currentPage=" + currentPage + ", listCount=" + listCount + ", limit=" + limit
				+ ", pageSize=" + pageSize + ", maxPage=" + maxPage + ", startPage=" + startPage + ", endPage="
				+ endPage + ", prevPage=" + prevPage + ", nextPage=" + nextPage + "]";
	}

	// 페이징 처리에 필요한 값을 계산하는 메소드 (클래스 내부에서만 사용하는 메소드)
	private void calculatePagination() {
		maxPage = (int)Math.ceil( (double)listCount / limit); //(int)Math.ceil( (double)int / int)
		
		// * startPage : 목록 하단에 노출된 페이지의 시작 번호
		startPage = (currentPage - 1)/pageSize * pageSize + 1; 
		
		// * endPage : 목록 하단에 노출된 페이지의 끝 번호
		endPage = startPage + pageSize - 1;
		
		// 만약 endPage가 maxPage를 초과하는 경우
		if (endPage > maxPage) endPage =  maxPage;
		
		
		// ------------------------------------------------------
		//
		// * prevPage(<) : 목록하단에 노출된 번호의 이전 목록 끝번호
		// * nextPage(>) : 목록하단에 노출된 번호의 다음 목록 시작 번호
		
		// 현재 페이지가 1 ~ 10 인 경우 (case1)
		// < : 1 페이지
		// > : 11 페이지
		
		// 현재 페이지가 11 ~ 20 인 경우(case2)
		// < : 10 페이지
		// > : 21 페이지
		
		// 현재 페이지가 41 ~ 50 인 경우 (maxPage가 50) (case3)
		// < : 40 페이지
		// > : 50 페이지
		
		if(currentPage <= pageSize) prevPage = 1; // case1
		else prevPage = startPage - 1; // case2 & case3
		
		if(maxPage == endPage) { // case3
			nextPage = maxPage;
		} else {
			nextPage = endPage + 1; // case1&case2
		}
		
	}
}




###[old] 2. 그래 이제 2단계 frontend작업이야. 자유게시판 frontend의 .html, .css, .js 각 파일들은 자유게시판 목록조회(freeboardList.html, freeboardList.css, freeboardList.js), 게시글 상세조회(reeboardDetail.html, freeboardDetail.css, freeboardDetail.js), 새 게시글 삽입(reeboardWrite.html, freeboardWrite.css, freeboardWrite.js), 상세게시글 수정/삭제(reeboardUpdate.html, freeboardUpdate.css, freeboardUpdate.js) 이고, 아래에 첨부했어. 또한 게시글 상세조회에서 댓글에 대한 CRUD를 위한 댓글 목록조회, 상세조회, 수정/삭제기능에 대한 frontend 파일은 comment.html, comment.css, freeboardComment.js로 이것도 아래 첨부했어. 이것들 모두 FastAPI와 native JS 기반 프론트엔드에 맞게 바꿔줘. 자유게시판 게시글 상세조회에서는 조회수와 좋아요 기능이 구현되어 있고, 게시글 신고기능과 자유게시판 새 게시글 삽입과 상세 게시글 수정에서 사용할 수 있는 챗봇기능은 추후에 porting하도록 할께. 이 모든 것들을 네가 이미 작성해준 main.html과 main.css,main.js들과 잘 integrated되게 작성해줘.


2. 그래 이제 2단계 frontend작업이야. 그런데 이것도 용량이 커서 다시 이걸 2-A,2-B,2-C 단계로 나누자.  자유게시판 frontend의  각 기능과 .html, .css, .js 각 파일들을 나누어보면  자유게시판 목록조회(freeboardList.html, freeboardList.css, freeboardList.js), 게시글 상세조회(freeboardDetail.html, freeboardDetail.css, freeboardDetail.js), 새 게시글 삽입(freeboardWrite.html, freeboardWrite.css, freeboardWrite.js), 상세게시글 수정/삭제(freeboardUpdate.html, freeboardUpdate.css, freeboardUpdate.js) 이고. 또한 게시글 상세조회에서 댓글에 대한 CRUD를 위한 댓글 목록조회, 상세조회, 수정/삭제기능에 대한 frontend 파일은 comment.html, comment.css, freeboardComment.js인데,  이번 2-A단계에서는 자유게시판 목록조회(freeboardList.html, freeboardList.css, freeboardList.js), 게시글 상세조회(freeboardDetail.html, freeboardDetail.css, freeboardDetail.js) 기능을 porting 해보자. 아래 이번 단계 해당 파일들을  첨부 할께,  이것들 모두 FastAPI와 native JS 기반 프론트엔드에 맞게 바꿔줘.이 모든 것들을 네가 이미 작성해준 main.html과 main.css,main.js들과 잘 integrated되게 작성해줘. (==> 이 단계에서 CC 허용 용량초과)



<!DOCTYPE html>
<html lang="ko" xmlns="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>자유게시판</title>

    <link rel="stylesheet" th:href="@{/css/board/freeboard/freeboardList.css}">
    <link rel="stylesheet" th:href="@{/css/common/font.css}">
  	<link rel="stylesheet" th:href="@{/css/common/common.css}" />    
    <link rel="stylesheet" th:href="@{/css/common/notification.css}" />

</head>



<body>

    <!-- <p th:text="${map.pagination}"></p>    
    <p th:text="${map.freeboardList}"></p>     -->
    <main th:with="pagination=${map.pagination}, freeboardList=${map.freeboardList}">
        <!-- 헤더 -->
        <!--<header class="main-header">header</header> -->
        <!-- header.html (fragment) 추가 -->
        <!-- <th:block th:replace="~{/common/header}">header.html</th:block> -->
        <!-- 또는 -->
        <!-- <div th:replace="common/header :: header"></div> -->

		<div th:replace="common/header :: header"></div>
		<script th:src="@{/js/common/header.js}"></script>


        <!-- 네비게이션 -->
        <nav class="main-nav"></nav>
        <!--  ###################################################### -->

        <div class="container-wrapper"> 
			<div class="top-space-bw-header"> </div>
            <h2 class="title-main fw-800">자유게시판</h2>   

            <div class="container">

                <!-- 글쓰기 버튼 -->
                <!-- <p th:text="${session.loginMember}"></p>  -->
                <div class="write-btn-box">
                    <button th:if="${session.loginMember}" class="write-btn" id="fbWriteBtn">글쓰기</button>
                </div>

                <!-- 게시글 리스트 -->
                <div class="card-list">

                    <!-- 게시글이 없을 때 -->
                    <div th:if="${#lists.size(freeboardList) == 0}" style="text-align: center; padding: 50px">
                        <p>작성된 게시글이 없습니다.</p>
                    </div>

                    <!-- 카드 1 -->
                    <th:block th:unless="${#lists.size(freeboardList) == 0}"></th:block>  
                        <div class="fbList-card" th:each="freeboard : ${freeboardList}">
                            <!-- thumbnail -->
                            <img th:if="${freeboard.thumbnail}" th:src="${freeboard.thumbnail}" class="fbList-card-img" th:alt="${freeboard.boardTitle}">
                            <img th:unless="${freeboard.thumbnail}" th:src="@{/images/logo.png}" class="fbList-card-img" alt="기본 이미지">
                            <div class="fbList-content">
                                <h3 class="fbList-title">
                                    <!-- 게시글 상세 링크 -->
                                    <a class="fbList-title-link"
                                        th:href="@{/board/freeboard/{no}(no=${freeboard.boardNo}, cp=${pagination.currentPage})}"
                                        th:text="${freeboard.boardTitle}">제목</a>
                                </h3>
                                <p class="fbList-text" th:text="${freeboard.boardContent}">내용</p>
                            </div>
                        </div>
                    </th:block>

                    

                <!-- 페이지네이션 -->
                <div class="pagination">

                    <ul th:unless ="${param.query}" class="pagination">
                        <li><a th:href="@{/board/freeboard(cp=1) }" class="arr left">&lt;&lt;</a></li>
                        <li><a th:href="@{/board/freeboard(cp=${pagination.prevPage} ) }" class="page-btn previous">&lt;</a></li>
                        <th:block th:each="i : ${#numbers.sequence(pagination.startPage, pagination.endPage, 1)}">
                            <!-- 현재 보고있는 페이지 -->
                            <li th:if="${pagination.currentPage == i}">
                                <a class="page-btn active" th:text="${i}">현재 페이지</a>
                            </li>
                             
                            <!-- 현재 페이지를 제외한 나머지 -->
                            <li th:unless="${pagination.currentPage == i}">
                                <a th:href="@{/board/freeboard( cp=${i}) }" class="page-btn" th:text="${i}"></a>
                            </li>
                        </th:block>
                        <li><a th:href="@{/board/freeboard( cp=${pagination.nextPage} ) }" class="page-btn next">&gt;</a></li>
                        <li><a th:href="@{/board/freeboard( cp=${pagination.maxPage} ) }" class="arr right">&gt;&gt;</a></li>

                    </ul>
                </div>

            </div>
        </div>


        <!--  ###################################################### -->
        <!--  <footer class="main-footer">footer</footer> -->
        <!-- footer.html 추가 -->
        <!-- <th:block th:replace="~{common/footer}">footer.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/footer :: footer"></div>
		
    </main>

    <!-- 알림창 띄우기 -->
    <script th:inline="javascript"> 
        const message = /*[[${message}]]*/ "전달 받은 message";
        if(message != null) alert(message); // message12가 없으면 null값
    </script>
    
	<script th:src="@{/js/notification/noti.js}"></script>
    <!-- freeboardList.js 추가 -->
    <script th:src="@{/js/board/freeboard/freeboardList.js}"></script>
</body>
</html>




/* 기본 설정 */
body {
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
    /* background-color: #f6f6f6; */
    background-color: #ffffff;    
    margin: 0;
}

/* header와의 간격벌리기 */
.top-space-bw-header{
    width: 10px;
    height: 10px;
    background-color: white;
    margin-bottom: 150px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

/* 상단 타이틀 바 */
.title-main {
    background: linear-gradient(
        to right,
        rgba(241, 198, 231, 1) 0%,       /* #F1C6E7 불투명도 100% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치도 불투명도 75% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치 투명도 75% */
        rgba(241, 198, 231, 0.5) 100%    /* 100% 위치 투명도 50% */
    );    
    padding: 22px 22px 22px 120px;
    /*border-radius: 6px;*/
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #000;
    font-size: 36px;
    font-weight: bolder;
    margin-bottom: 25px;
}

.container {
    width: 70%;
    margin: 0 auto;
    padding: 30px 0;
}

/* 글쓰기 버튼 */
div.write-btn-box {
    /* width: 100%; */
    width: 1210px; /* 1210px 고정 */
    text-align: right;
    margin-top: 60px;
    margin-bottom: 60px;
    
}

.write-btn {
    width:180px; /* 180px 고정 */
    background-color: #BD83CE;
    border: none;
    padding: 10px 20px;
    color: white;
    font-weight: regular;
    border-radius: 6px;
    font-size: 35px;
    cursor: pointer;
    margin-right: 100px;
}

.write-btn:hover {
    background-color: #E5B0EA;
}

/* 카드 리스트 */
.fbList-card {
    width: 1210px; /* 1210px 고정 */
    border: 1px solid #e6e6e6;

    display: flex;
    background-color: white;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.fbList-card-img {
    width: 160px;
    height: 160px;
    object-fit: cover;
    border-radius: 3px;
}

.fbList-content {
    margin-left: 15px;
}

.fbList-title {
    margin: 0;
    font-size: 24px;
    font-weight: bold;
}
.fbList-title-link {
    padding: 6px 0px;
    /* border: 1px solid #ccc; */
    margin: 0 2px;
    /* border-radius: 6px; */
    color: #000;
    text-decoration: none;
    font-size: 24px;
}
.fbList-title-link:hover{
    color: #BD83CE;
}

.fbList-text {
    margin-top: 8px;
    font-size: 16px;
    color: #757575;
}

/* 페이지네이션 */
.pagination {
    list-style: none;   /*  li 태그 dot 제거 */

    width: 1210px; /* 1210px 고정 */
    display: flex;
    justify-content: center;
    margin: 200px 0;
    align-items: center;
}

.page-btn {
    padding: 6px 12px;
    border: 1px solid #ccc;
    margin: 0 4px;
    border-radius: 6px;
    color: #000;
    text-decoration: none;
    font-size: 14px;
}

.page-btn:hover {
    background-color: #F1C6E7;
}

.page-btn.previous {
    border: 1px solid #fff;
}

.page-btn.next {
    border: 1px solid #fff;
}


.active {
    background-color: #BD83CE;
    color: white !important;
    border-color: #BD83CE;
}


.arr {
    font-size: 24px;
    text-decoration: none;
    color: #000;
}

.arr:hover {
    font-size: 24px;
    color: #BD83CE;
    cursor: pointer;
}

.next {
    font-size: 24px;
    text-decoration: none;
}

.next:hover {
    font-size: 24px;
    color: #BD83CE;
    cursor: pointer;
    background-color: #fff;
}

.previous {
    font-size: 24px;
    text-decoration: none;    
}

.previous:hover {
    font-size: 24px;
    color: #BD83CE;
    cursor: pointer;
    background-color: #fff;    
}




console.log("freeboardList.js loaded");
// 글쓰기 버튼 클릭 시 


document.getElementById("fbWriteBtn")?.addEventListener("click", ()=>{
    // JS BOM 객체 중 location
    console.log(location.pathname.split("/")); // location.pathname = "/board/freeboard"

    // location.href = '주소' : 해당 주소로 요청(GET 방식)
	location.href = `/board2/${location.pathname.split("/")[2]}/insert`; // => http://localhost:8880/board2/freeboard/insert
	
});


<!DOCTYPE html>
<html lang="ko" xmlns="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>자유게시판 - 상세보기</title>

    <link rel="stylesheet" th:href="@{/css/common/font.css}">
    <link rel="stylesheet" th:href="@{/css/common/common.css}" />
    <link rel="stylesheet" th:href="@{/css/common/notification.css}" />
    <link rel="stylesheet" th:href="@{/css/board/freeboard/freeboardDetail.css}">
    <link rel="stylesheet" th:href="@{/css/board/freeboard/comments.css}">
    <link rel="stylesheet" th:href="@{/css/common/report.css}">
</head>
<body>
    <!-- <p th:text="${freeboard}" th:if="${freeboard != null}"></p>     -->
    <!-- <p th:text="${session.loginMember}"></p>  -->
    <main>

        <!-- 헤더 -->
        <!-- <header class="main-header">header</header> -->
        <!-- header.html (fragment) 추가 -->
        <!-- <th:block th:replace="~{/common/header}">header.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/header :: header"></div>
        <script th:src="@{/js/common/header.js}"></script>

        <!-- 네비게이션 -->
        <nav class="main-nav"></nav>
        <!--  ###################################################### -->        

        <div class="container-wrapper">
            <div class="top-space-bw-header"> </div>
            <!-- 상단 제목 -->
            <h2 class="title-main fw-800">자유게시판</h2>
            <div class="container">

                <!-- 글 제목 -->
                <div class="post-title" th:text="${freeboard.boardTitle}">상세 게시글 제목</div>

                <!-- 작성정보 -->
                <div class="post-info-area">
                    <!-- 대표 이미지 -->
                    <div class="main-image-box">
                        <img th:if="${freeboard.thumbnail}" th:src="${freeboard.thumbnail}" class="main-img" th:alt="${freeboard.boardTitle}">
                        <img th:unless="${freeboard.thumbnail}" th:src="@{/images/logo.png}" class="main-img" alt="기본 이미지">
                    </div>

                    <div class="post-info-box">
                        <div class="info-text">
                            <div class="info-text-row"><span>작성일</span> <span class="info-text-row span"><p th:text="${freeboard.bCreateDate}" th:if="${freeboard.bCreateDate != null}">작성일</p></span></div>
                            <div class="info-text-row"><span>조회수</span> <span class="info-text-row span"><p th:text="${freeboard.boardCount}" th:if="${freeboard.boardCount != null}">조회수</p></span></div>
                            <div class="info-text-row"><span>작성자</span> <span class="info-text-row span"><p th:text="${freeboard.memberNickname}" th:if="${freeboard.memberNickname != null}">작성자</p></span></div>
                            <div class="heart info-text-row">
                                <span class="heart-like-img">

                                    <i class="like-icon" th:data-board-id="${freeboard.boardNo}" data-liked="false" th:unless="${likeCheck}">
                                        <img th:src="@{/images/board/freeboard/iconfy_red-heart_empty.png}" class="heart-like" alt="#">
                                    </i>
                                    <i class="like-icon" th:data-board-id="${freeboard.boardNo}" data-liked="true" th:if="${likeCheck}">
                                        <img th:src="@{/images/board/freeboard/iconfy_twemoji_red-heart_filled.png}" class="heart-like" alt="#">
                                    </i>

                                </span> 
                                <span class="info-text-row span"><p id="pTagLikeCount" th:text="${freeboard.likeCount}" >좋아요 수</p></span>
                            </div>
                            <div></div>
                        </div>
                    </div>
            
                    <!-- 신고 버튼 -->
                    <div class="report-box">
                        <th:block th:if="${session.loginMember != null}">          
                            <div  class="report-btn" id="reportBtn"
                                    th:onclick="|openReportModal(${freeboard.memberNo}, ${freeboard.boardNo})|">
                                <div>게시글신고</div>
                                <img th:src="@{/images/board/freeboard/report_icon.png}" class="report-img" alt="#">
                            </div>
                        </th:block>
                    </div>
            

                </div>

                <!-- 이미지가 1개 이상 있을 경우 -->
                <th:block th:if="${#lists.size(freeboard.imageList) > 1 }">
                    <!-- 작은 이미지들 : imageList에서 thumbnail 이외의 것들 여기에 출력-->
                    <div class="sub-image-box" >
                        <!--                                     start,        end,                   step -->
                        <th:block th:each="i : ${#numbers.sequence(1, #lists.size(freeboard.imageList)-1, 1)}">
                            <div class="boardImg" th:with="path=|${freeboard.imageList[i].imgPath}${freeboard.imageList[i].imgRename}|"> 
                                <img th:src="${path}" class="sub-img" alt="#">
                            </div>
                        </th:block>
                    </div>

                </th:block>

                <!-- 본문 내용 -->
                <div class="content" th:text="${freeboard.boardContent}">상세 게시글 내용
                </div>

                <!-- 하단 버튼 -->
                <div class="bottom-btn-box">
                    <!-- <th:block th:if="${session.loginMember?.memberAdmin == T(com.devlog.project.member.enums.Status).Y
                                        or session.loginMember?.memberNo == freeboard.memberNo}"> -->
                    <th:block th:if="${session.loginMember != null 
                                        and (session.loginMember.memberNo == freeboard.memberNo 
                                            or session.loginMember.role == 'ROLE_ADMIN')}">
                        <button class="bottom-btn" id="updateBtn">수정</button>
                        <button class="bottom-btn" id="deleteBtn">삭제</button>
                    </th:block>
                    
                    <button class="bottom-btn" id="goToListBtn">목록으로</button>
                </div>

            </div>

        </div>
        
		<th:block th:replace="~{board/freeboard/comments}"></th:block>  
		   
        <!--  ###################################################### -->
        <!-- <footer class="main-footer">footer</footer> -->
        <!-- footer.html 추가 -->
        <!-- <th:block th:replace="~{common/footer}">footer.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/footer :: footer"></div>
        
    </main>

    <script th:inline="javascript"> // freeboardDetail.js처럼 JS에서 사용할 전역 변수들을 선언~~

        let loginMemberNo = /*[[${session.loginMember?.memberNo}]]*/ null; 
        let memberNickname = /*[[${session.loginMember?.memberNickname}]]*/ null;
        if(loginMemberNo === null) loginMemberNo = ""; // 들어가는 값이 없으면 대신 빈칸을 넣어준다 (아래 boardDetail.js, comment.js에서 ""로 받아서 처리)
        
        // 명시적으로 전역 등록
        window.loginMemberNo = loginMemberNo;
        window.memberNickname = memberNickname;        
        window.boardNo = /*[[${freeboard?.boardNo}]]*/ null;
        window.boardCode = /*[[${freeboard?.boardCode}]]*/ null;
        window.boardTitle = /*[[${freeboard?.boardTitle}]]*/ null;
        
    </script>
    
    <!-- 알림창 띄우기 -->
    <script th:inline="javascript"> 
        let message = /*[[${message}]]*/ null;
        if(message != null) alert(message); // message12가 없으면 null값
    </script>
    
    <!-- freeboardDetail.js 추가 -->
    <script th:src="@{/js/board/freeboard/freeboardDetail.js}"></script>    
    <!-- freeboardComment.js 추가 -->
    <script th:src="@{/js/board/freeboard/freeboardComment.js}"></script>     
    

    <!-- 모달 for 게시글 신고: 2026/01/05 -->
    <div id="modal-root"></div>
    <script th:src="@{/js/common/report.js}"></script> 
</body>
</html>

/* section, div{ border : 1px solid black;}  */
/* ========================= */
body {
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
    /* body 전체에 Pretendard Variable Font 적용*/    
    background-color: #ffffff;
    margin: 0;
}

.container-wrapper {
    margin: 0;
}

/* header와의 간격벌리기 */
.top-space-bw-header{
    width: 10px;
    height: 10px;
    background-color: white;
    margin-bottom: 150px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

/* 상단 타이틀 */
.title-main {
    /*background-color: #F1C6E7;*/
    /*background: linear-gradient(to right, #F1C6E7 50%, #FFF 100%);*/
    background: linear-gradient(
        to right,
        rgba(241, 198, 231, 1) 0%,       /* #F1C6E7 불투명도 100% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치도 불투명도 75% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치 투명도 75% */
        rgba(241, 198, 231, 0.5) 100%    /* 100% 위치 투명도 50% */
    );    
    /* padding: 12px 12px 12px 120px; */
    padding: 22px 22px 22px 120px;
    /*border-radius: 6px;*/
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #000;
    font-size: 36px;
    font-weight: bolder;
    margin-bottom: 25px;
}

.container {
    /* width: 900px;
    margin: 40px auto; */
    width: 70%;
    margin: 0 auto;
    padding: 30px 0;    
}

/* .board-title {
    background-color: #f8d4e3;
    padding: 12px 16px;
    border-radius: 4px;
    font-size: 18px;
    font-weight: 700;
    margin: 0;
} */

/* 글 제목 */
.post-title {
    font-size: 40px;
    font-weight: 800;
    /* margin-top: 20px; */
    margin-top: 100px;
    margin-bottom: 60px;
}

/* 메인 이미지 + 작성정보 박스 +  작은 이미지 영역 */
.post-info-area{
    display: flex;
    /* justify-content: start; */
    flex-direction: row;
    justify-content: space-between;
    align-items: start;

    padding-left: 60px; /* 큰이미지 왼쪽에서 60px 띄어서 표시 */
}

/* 메인 이미지 */
.main-image-box {
    text-align: center;
    /* margin-top: 30px; */
    /* margin-left: 60px; */
}

.main-img {
    width: 330px;
    height: 330px;
    object-fit: cover;
    border-radius: 6px;
} 

/* 작성정보 박스 */
.post-info-box {
    display: flex;
    /* justify-content: flex-end; */
    flex-direction: column;
    justify-content: start;
    align-items: flex-start;

    /* width:600 px;     */
}

.info-text {
    /* width:100%; */
    width: 300px;
    text-align: right;
    /* margin-right: 25px; */
    /* font-size: 24px; */
    font-size: 22px;
    line-height: 1.6;


    display: flex;
    flex-direction: column;
    /* justify-content: start; */
    /* justify-content: space-evenly; */
    /* justify-content: space-between; */
    justify-content: start;
    align-items: center;    /* 텍스트 행들 (horizontal-alignment) column 중앙으로 */
}

.info-text-row {
    width: 70%; /* 작성정보 박스에 텍스트 영역 % */
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: start;    
    width:600 px;    

    margin: 4px 0px 4px 0px; /* [M1]margin top/bottom으로 row의 행간 조정 by M1+M2+M3 */   
}
.info-text-row.span{
    margin: 0px 0px 0px 0px; /* [M2] p-tag의 기본 top/bottom 마진 24px -> 4px로: row의 행간 조정 by M1+M2+M3 */
}

.info-text-row.span p {
    margin: 0px 0px 0px 20px; /* [M3] p-tag의 기본 top/bottom 마진 24px -> 4px로: row의 행간 조정 by M1+M2+M3 */
}

.heart-like-img {
/* .heart.info-text-row { */
    display: flex;
    justify-content: center;
    flex-direction: row;
    align-items: center; 
}

/* .heart-like {
    text-align: center;
    width: 25px;
    height: 25px;
    padding: 7px 0px 7px 15px;
} */

.heart-like {
    margin-top:5px;
    margin-left:15px;
    text-align: center;
    width: 25px;
    height: 25px;
    padding: 0;  /* 기존 padding 제거해서 정확한 중앙 정렬 */
    display: block;
}

/* .heart {
    font-size: 24px;
} */


/* 신고 버튼 */
.report-box {
    text-align: right;
    margin-top: 0px;
}

.report-btn {
    background: #fff;
    color: #000;
    padding: 8px 18px;
    border: none;
    border-radius: 6px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;

    display: flex;
    justify-content: space-around; 
    flex-direction: row;
    align-items: center;  

}
.report-btn:hover {
    background: #F7E8F6;
}
.report-img {
    margin-left:10px;
}

/* 작은 이미지 영역 */
.sub-image-box {
    display: flex;
    /* justify-content: center; */
    justify-content: start;
    margin-top: 20px;
    /* gap: 20px; */

    padding-left: 60px; /* 작은이미지 왼쪽에서 60px 띄어서 표시 */
}

.sub-img {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 6px;
    
    margin-right: 10px;
}

/* 본문 */
.content {
    margin: 50px 0px 140px 0px;
    font-size: 30px;
    line-height: 1.8;
    white-space: pre-line;
    color: #444;
}

/* 하단 버튼 */
.bottom-btn-box {
    margin-top: 40px;
    text-align: center;

    display: flex;
    justify-content: end; /* 버튼 우측 끝선에 맞춰지도록 */
    flex-direction: row;
    align-items: center;      
}

.bottom-btn {
    background: #BD83CE;
    color: white;
    padding: 10px 40px;
    font-size: 35px;
    border: none;
    margin: 0 10px;
    border-radius: 6px;
    cursor: pointer;
}
.bottom-btn:hover {
    background: #E5B0EA;
}

/* 좋아요 하트 클릭 */
.like-icon {
    display: inline-block;
    cursor: pointer;
}

.like-icon img {
    width: 24px;
    height: 24px;
    transition: transform 0.15s ease, opacity 0.15s ease;
}

/* hover 효과 */
.like-icon:hover img {
    transform: scale(1.15);
    opacity: 0.8;
}

/* 클릭 애니메이션 */
.like-icon.active img {
    transform: scale(1.2);
}


console.log("freeboardDetail.js loaded");
// 글쓰기 버튼 클릭 시 

console.log("loginMemberNo =", loginMemberNo);
// 또는
console.log("loginMemberNo =", window.loginMemberNo);

const likeIcon = document.querySelector(".like-icon");
const img = likeIcon.querySelector("img");

const HEART_EMPTY = "../../../images/board/freeboard/iconfy_red-heart_empty.png";
const HEART_FILLED = "../../../images/board/freeboard/iconfy_twemoji_red-heart_filled.png";

const pTagLikeCount = document.getElementById("pTagLikeCount"); // 좋아요 수 표시 tag업데이트

likeIcon.addEventListener("click", async () => {
    const boardNo = likeIcon.dataset.boardId;
    const liked = likeIcon.dataset.liked === "true"; // DB에서 현 loginMember가 이 boardNo에 좋아요 한적 있는지 체크해서 업데이트 해줘야 함

    // 로그인 X
    //if(loginMemberNo == null) { // 
    if(loginMemberNo == "") { // loginMemberNo를 여기서 쓰려고 boardDetail.jsp에서 전역변수로 선언해놓았다 
        alert("로그인 후 이용해 주세요");
        return;   // 아래는 확인 필요 없음 
    }

    try {

        // ajax로 서버에 제출할 파라미터를 모아둔 JS 객체
        const data = {  memberNo : loginMemberNo,
                        'boardNo': Number(boardNo),
                        "check"  : Number(liked) //  DB에서 현 loginMember가 이 boardNo에 좋아요 한적 있는지 체크해서 업데이트 해줘야 함
                    };                    
        
        console.log(data);

        if (!liked) {
        // 좋아요 추가
        await fetch("/board/freeboard/like", {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
            },
            
            body: JSON.stringify(data)
        })
        .then(resp => resp.text())
        .then(count => {
            // 파싱된 데이터를 받아서 처리하는 코드 작성
            console.log("count : " + count); // -1이면 SQL실패

            // INSERT, DELETE실패 시 (좋아요 조회 실패시 FreeboardServiceImpl에서 -1 반환)
            if (count == -1) { // 
                alert("좋아요 추가 처리 실패.");
                return;
            }

            pTagLikeCount.innerText = count;

        });


        img.src = HEART_FILLED;
        likeIcon.dataset.liked = "true";
        likeIcon.classList.add("active");

        } else {
        // 좋아요 삭제
            await fetch("/board/freeboard/like", {
                // method: "DELETE",
                method: "POST",
                headers: {
                "Content-Type": "application/json"
                },
                //body: JSON.stringify({ boardNo })
                body: JSON.stringify(data)
            })
            .then(resp => resp.text())
            .then(count => {
                // 파싱된 데이터를 받아서 처리하는 코드 작성
                console.log("count : " + count); // -1이면 SQL실패

                // INSERT, DELETE실패 시 (좋아요 조회 실패시 FreeboardServiceImpl에서 -1 반환)
                if (count == -1) { // 
                    alert("좋아요 삭제 처리 실패.");
                    return;
                }

                pTagLikeCount.innerText = count;

            });

            img.src = HEART_EMPTY;
            likeIcon.dataset.liked = "false";
            likeIcon.classList.remove("active");
        }

    } catch (e) {
        alert("좋아요 처리 중 오류가 발생했습니다.");
        console.error(e);
    }
});


// ----------------------------------
// 게시글 수정
//
// 게시글 버튼 수정 클릭시
if (document.getElementById("updateBtn") != null){ // 로그인 안했으면 수정버튼 안보임 => null처리 필요
    document.getElementById("updateBtn").addEventListener("click", ()=>{
    
        location.href = location.pathname.replace('board/', 'board2/') + '/update' + location.search; // location.search = '?cp=1'
        // eg: '/board2/freeboard/5/update?cp=1'
    
    })
}


// ---------------------------------
// 게시글 삭제 버튼이 클릭 되었을 때
//
 // 로그인 안했으면 삭제버튼 안보임 => null처리 필요 => 옵셔날 체이닝으로 처리
document.getElementById("deleteBtn")?.addEventListener("click", ()=>{

    console.log(location.pathname.replace('board/', 'board2/') + "/delete");
    if(confirm("정말 삭제 하시겠습니까?")) {

        location.href = location.pathname.replace('board/', 'board2/') + "/delete"; // -> 게시글 삭제 처리하는 controller 만들어야 한다.
        // http://localhost/board2/freeboard/5/delete

    }
})


// -----------------------------------------------------------
// 목록으로
const goToListBtn = document.getElementById("goToListBtn");

goToListBtn.addEventListener("click", ()=>{
    // location.href = location.pathname.split("/").slice(0, -1).join('/') + location.search; 
    // URL 내장 객체 : 주소 관련 정보를 나타내는 객체
    // URL.searchParams : 쿼리스트링만 별도 객체로 반환
    console.log("goToListBtn clicked... ")
    
    const params = new URL(location.href).searchParams;
    console.log("params : " + params);

    let url;
    if (params.get("key") == 'all') { // header의 통합 검색 일때 (Not used here)
        url = "/board/search";
    } else {
        url = '/board/freeboard'; // 목록으로; boardCode=3는 전역변수
    }

    location.href = url + location.search;

})

function openReportModal(targetMemberNo, targetNo) {  //<--------------------------- 함수 호출 시 타겟 회원 번호 넣어서 호출
    console.log("openReportModal함수 실행...")
    
    console.log("before Number() conversion: ")
    console.log(targetMemberNo, typeof targetMemberNo)
    console.log(targetNo, typeof targetNo)  
    
    targetMemberNo = Number(targetMemberNo);
    targetNo = Number(targetNo);
    console.log("after Number() conversion: ")
    console.log(targetMemberNo, typeof targetMemberNo)
    console.log(targetNo, typeof targetNo)

    fetch(`/report/modal?memberNo=${targetMemberNo}`) //<------------------------------------------- 타켓 대상 회원 번호 넣어주셔야 합니다.
        .then((res) => res.text())
        .then((html) => {
            console.log("받아온 html: ")
            console.log(html); // 뭘 받아오나 보자

            const root = document.getElementById("modal-root"); // freeboardDetail.html에 <div id="modal-root"></div> 태그 필요
            root.innerHTML = html;
            const modal = root.querySelector("#reportModal");
            modal.classList.remove("display-none");

            modal.dataset.targetType = "BOARD"; //<-------------------------- 이 부분은 게시판이신 분들은 BOARD로 바꿔주세요
            modal.dataset.targetNo = targetNo; //<-------------------------- 게시글 번호도 이런 식으로 넘겨주세요
            bindReportModalEvents();
        });
}


function scrollToHashIfExists() {
  const hash = location.hash; // 예: "#comment-6"
  if (!hash) return;

  const target = document.querySelector(hash);
  if (target) {
    target.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

const reportBtn = document.getElementById("reportBtn");
// 좋아요 버튼이 클릭 되었을 때
reportBtn.addEventListener("click", (e) => {
  // 로그인 X
  if (!loginMemberNo || loginMemberNo === "") {
    alert("로그인 후 이용해주세요.");
    location.href  = "/board/freeboard";
    return;
  }
})




이제 2-B단계에서는 새 게시글 삽입(freeboardWrite.html, freeboardWrite.css, freeboardWrite.js), 상세게시글 수정/삭제(freeboardUpdate.html, freeboardUpdate.css, freeboardUpdate.js) 기능을  porting 하자. 아래 이번 단계 해당 파일들을  첨부 할께,  이것들 모두 FastAPI와 native JS 기반 프론트엔드에 맞게 바꿔줘. 참고로 자유게시판 게시글 상세조회에서는 조회수와 좋아요 기능이 구현되어 있고, 게시글 신고기능과 자유게시판 새 게시글 삽입과 상세 게시글 수정에서 사용할 수 있는 챗봇기능은 추후에 따로 porting하도록 할께. 이 모든 것들을 네가 이미 작성해준 main.html과 main.css,main.js들, 그리고 위의 2-A단계에서 작성해준 html, css, js 파일들과  잘 integrated되게 작성해줘.



<!DOCTYPE html>
<html lang="ko" xmlns="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>자유게시판 글쓰기</title>
    <link rel="stylesheet" th:href="@{/css/board/freeboard/freeboardWrite.css}">
    <link rel="stylesheet" th:href="@{/css/common/font.css}">
    <link rel="stylesheet" th:href="@{/css/common/common.css}" />
    <link rel="stylesheet" th:href="@{/css/common/notification.css}" />
        
</head>

<body>
    <!-- <p th:text="${freeboard}" th:if="${freeboard != null}"></p>     -->
    <main>
        
        <!-- 헤더 -->
        <!-- <header class="main-header">header</header> -->
        <!-- header.html (fragment) 추가 -->
        <!-- <th:block th:replace="~{/common/header}">header.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/header :: header"></div>
        <script th:src="@{/js/common/header.js}"></script>

        <!-- 네비게이션 -->
        <nav class="main-nav"></nav>
        <!--  ###################################################### -->  

		<div class="top-space-bw-header"> </div>
        <!-- 상단 타이틀 바 -->
        <h2 class="title-main fw-800">자유게시판</h2>  
        <div class="container">
    
            <!-- 글작성 도우미 -->
            <div class="helper-box">
                <button class="helper-btn" onclick="openHelper()">글작성 도우미</button>
    
                <div class="select-box">
                    <select class="ai-select" id="helperType">
                        <!--<option class="sel-ai" value="ai">AI</option> -->
                        <option class="sel-chatbot" value="chatbot">챗봇</option>
                    </select>
                </div>
            </div>
    
            <!-- 작성 폼 -->
            <form th:action="@{/board2/freeboard/insert}" method="post" enctype="multipart/form-data"
                    class="board-write" id="boardWriteFrm">            

                <!-- 제목 입력 -->
                <input type="text" id="titleInput" name="boardTitle" class="title-input" placeholder="   제목을 입력해주세요."  maxlength="300" required>
        
                <!-- 사진 등록 -->
                <div class="photo-header">
                    <span class="photo-title">사진 등록 <p>썸네일(대표) 이미지는 첫 사진입니다.</p></span>
                    <span class="photo-max">최대 5장</span>
                </div>
        
                <!-- 이미지 업로드 박스 -->
                <div class="photo-section">
                    <div class="photo-upload-area">
                        <!-- 미리보기 영역 -->
                        <div id="photoPreview" class="photo-preview"></div>
                        <!-- + 버튼 -->
                        <label for="photoInput" class="photo-upload">
                            <span class="plus">+</span>
                        </label>
                        <!-- 실제 파일 input (숨김) -->
                        <input type="file" id="photoInput" name="images" multiple accept="image/*" hidden />
                    </div>
                </div>

                <p class="image-warning">
                    본 사이트 약관/정책을 위반하는 이미지는 안내 없이 삭제 될 수 있습니다.
                </p>
        
                <!-- 내용 입력 -->
                <textarea id="contentInput" name="boardContent" minlength="10" maxlength="4000" 
                        class="content-box" placeholder="내용을 입력해 주세요.
        악의적인 비난/광고성 글은 검토 후 경고/삭제 조치될 수 있습니다." required></textarea>
        
                <div class="text-limit">최소 10자, 최대 4000자 (<span id="charCount">0</span> / 4000자)</div>
                <!-- <div class="char-count">
                    <span id="charCount">0</span> / 4000자
                </div> -->
                <!-- 버튼 -->
                <div class="button-box">
                    <button type="submit" id="submitBtn" class="submit-btn">새글 등록</button>
                    <button type="button" class="cancel-btn"
                    th:onclick="|location.href='@{/board/freeboard}'|">취소</button>
                </div>

            </form>

        </div>

        <!--  ###################################################### -->
        <!-- <footer class="main-footer">footer</footer> -->
        <!-- footer.html 추가 -->
        <!-- <th:block th:replace="~{common/footer}">footer.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/footer :: footer"></div>

    </main>

    <!-- 알림창 띄우기 -->
    <script th:inline="javascript"> 
        const message = /*[[${message}]]*/ "전달 받은 message";
        if(message != null) alert(message); // message12가 없으면 null값
    </script>

    <!-- freeboardWrite.js 추가 -->
    <script th:src="@{/js/board/freeboard/freeboardWrite.js}"></script>    

</body>
</html>


/* 기본 설정 */
body {
    /* background: #fafafa; */
    background-color: #ffffff;  
    margin: 0;
    padding: 0;
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
}

/* header와의 간격벌리기 */
.top-space-bw-header{
    width: 10px;
    height: 10px;
    background-color: white;
    margin-bottom: 150px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

/* 상단 타이틀 바 */
.title-main {
    background: linear-gradient(
        to right,
        rgba(241, 198, 231, 1) 0%,       /* #F1C6E7 불투명도 100% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치도 불투명도 75% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치 투명도 75% */
        rgba(241, 198, 231, 0.5) 100%    /* 100% 위치 투명도 50% */
    );    
    padding: 22px 22px 22px 120px;
    /*border-radius: 6px;*/
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #000;
    font-size: 36px;
    font-weight: bolder;
    margin-bottom: 25px;
}

/* 전체 컨테이너 */
.container {
    max-width: 1440px; /* 내용 길이 1440px */
    margin: 30px auto;
    padding: 0 10px;
}

/* 글작성 도우미 */
.helper-box {
    display: flex;
    align-items: center;
    margin-top: 60px;
    margin-bottom: 100px;
    padding: 0px 50px;
}

.helper-btn {
    width: 260;
    height: 60;
    background: #BD83CE;
    border: 1px solid #BD83CE;
    border-radius: 6px;
    color: white;
    font-size: 36px;
    padding: 1px 20px;
    margin-right: 20px;
    cursor: pointer;
}
.helper-btn:hover {
    background-color: #E5B0EA;
    border: 1px solid #E5B0EA;
}

/* .ai-select {
    width: 260;
    height: 60;    
    margin-left: 15px;

    background: #F7E8F6;
    padding: 7px 20px;
    border: 1px solid #000;
    border-radius: 6px;
    font-size: 32px;
    font-weight: bolder;
} */
.select-box {
    position: relative;
    width: 260;
    /* height: 60;   */

}
.select-box select {
    width: 100%;
    padding:10px 70px 10px 10px;

    background: #F7E8F6;
    /* padding: 10px 6px; */
    border-radius: 6px;
    /*  */
    font-size: 32px;
    font-weight: bolder;
    /* margin-left: 15px;     */

    appearance: none; /* 기본화살표 숨기기 */
    -webkit-appearance: none;
    -moz-appearance: none;
}
/* 커스텀 화살표 */
.select-box::after { /* .select-box 요소 뒤에 가상의 요소로 커스텀 화살표 생성: 실제 HTML에는 없지만 화면에는 보임*/
    content: "";
    position: absolute;
    right: 0px;
    top: 52%;
    transform: translateY(-50%);

    width: 60px;          /* 화살표-png 크기 */
    height: 60px;
    background-image: url("../../../images/board/freeboard/fb_select_SortDown3.png");
    background-repeat: no-repeat;
    background-size: contain; /* 또는 cover */
    pointer-events: none;
}


/* 제목 입력 */
.title-input {
    height: 127px;
    width: 80%; /* 내용 길이 1440px의 80% */
    margin-left: 110px;
    padding: 15px 0px 15px 20px;
    border: 1px solid #CFCFCF;
    border-radius: 20px;
    font-size: 36px;
    /* color: #B4B4B4; */
    margin-bottom: 60px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* 사진 영역 */
.photo-header {
    width: 80%;
    margin-left: 130px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.photo-title {
    font-weight: bold;
    font-size: 36px;
}

.photo-max {
    font-size: 36px;
    color: #B4B4B4;
    margin-right:90px;
}

/* 사진 업로드 박스 */
/* 사진 */

.photo-upload {
    /* width: 200px;
    height: 200px; */
    width: 175px;
    height: 175px;    
    /* margin-left: 130px; */
    /* margin-top: 20px;    */
    border: 1px solid #ccc;
    background: #fbfbfb;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    /* flex: 1 0 auto;  //flex: <flex-grow> <flex-shrink> <flex-basis>; */
    /* flex-grow: 1;   남으면 늘어남 */
    flex-shrink: 0; /* 부모 컨테이너 공간이 부족해도 이 요소는 크기를 줄이지 않는다 (스크롤 생김)*/
    /* flex-basis: auto 기본 크기는 원래 크기대로 설정된 width가 있으면 그걸 사용 */
    /* *****
    flex: 1 1 0; // 가장유연
    flex: 0 0 auto // 완전고정
    flex: 1 0 auto //콘텐츠 보호 + 가변 레이아웃 
    ***** */
}
.photo-upload:hover {
    background-color: #F7E8F6;
}

.plus {
    font-size: 50px;
    font-weight: 100;
    color: #8E8E8E;
}

.image-warning {
    font-size: 36px;
    margin-left: 130px;   
    margin-top: 35px;
    color: #B4B4B4;
}

/* ===== 사진 업로드 박스: 추가 ===== */
/* 썸네일 지정 알림 텍스트 */
.photo-title p{ 
    color: #B4B4B4;
    font-size: 24px;
    padding-left: 40px;
}

.photo-section {
    width: 100%;
    margin-top: 30px;
}

.photo-upload-area {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-left: 130px;
    margin-bottom: 10px;
}


.photo-preview {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: flex-start;
}

.preview-img-container {
    position: relative;
    /* width: 200px;
    height: 200px; */
    width: 175px;
    height: 175px;      
    /*  */
    /* display: flex;
    align-items: center;
    justify-content: center; */
}

.preview-img {
    /* width: 200px;
    height: 200px; */
    width: 175px;
    height: 175px;       
    object-fit: cover;
    border-radius: 6px;
    
    /*  */
    display: flex;
    align-items: center;
    justify-content: center;
}

/* .preview-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 6px;
} */

.preview-remove {
    position: absolute;

    top: -8px;
    right: -8px;
    width: 24px;
    height: 24px;
    background-color: #f74c3c;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 14px;
    font-weight: bold;
    transition: background-color 0.2s;
}

.preview-remove:hover {
    background-color: #80392b;
}

/* 썸네일(대표) 이미지 강조 */
.preview-img-container.thumbnail {
    outline: 4px solid #F7A1C4;
}

.thumbnail-badge {
    position: absolute;
    bottom: 8px;
    left: 8px;
    background-color: #F7A1C4;
    color: white;
    font-size: 12px;
    padding: 4px 6px;
    border-radius: 4px;
    font-weight: bold;
}

/* 게시글 내용 입력 */
.content-box {
    /* width: 100%; */
    height: 463px;
    width: 80%;
    margin-left: 110px;    
    margin-top: 0px;
    /* padding: 15px; */
    padding: 15px 10px;
    resize: none;
    border: 1px solid #B4B4B4;
    border-radius: 20px;
    font-size: 36px;
    line-height: 1.4;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.text-limit {
    width: 80%;
    margin-left: 70px;  
    margin-right: 40px;

    text-align: right;
    margin-top: 5px;
    font-size: 36px;
    color: #B4B4B4;
}
/* 입력 글자수 카운트 */
/* .char-count {
    width: 80%;
    margin-right: 40px;    
    text-align: right;  
    margin-top: 5px;
    font-size: 24px;
    color: #B4B4B4;
} */

/* 버튼 영역 */
.button-box {
    width: 82%;
    margin-left: 110px;       
    /* margin-right: 80px;     */
    text-align: right;
    margin-top: 100px;
    margin-bottom: 200px;
}

.submit-btn {
    width: 180px;
    height: 60px;
    background: #BD83CE;
    color: white;
    padding: 0px 2px;
    border: none;
    border-radius: 6px;
    font-size: 35px;
    cursor: pointer;
}
.submit-btn:hover {
    background: #E5B0EA;
}

.cancel-btn {
    width: 180px;
    height: 60px;    
    background: #BD83CE;
    color: white;
    padding: 0px 2px;
    border: none;
    border-radius: 6px;
    font-size: 35px;
    margin-left: 5px;
    /* margin-right: 120px; */
    cursor: pointer;
}
.cancel-btn:hover {
    background: #E5B0EA;
}

console.log("freeboardWrite.js loaded");



document.addEventListener("DOMContentLoaded", () => {
    
    /** 글자 수 카운트 **/
    const textarea = document.getElementById("contentInput");
    const charCount = document.getElementById("charCount");

    textarea.addEventListener("input", () => {
        const length = textarea.value.length;
        charCount.textContent = length;
        if (length > 4000) {
        textarea.value = textarea.value.substring(0, 4000);
        charCount.textContent = 4000;
        }
    });

    /** 이미지 미리보기 **/
    const photoInput = document.getElementById("photoInput");
    const photoPreview = document.getElementById("photoPreview");

    let selectedFiles = []; // 🔹 선택된 파일 누적 관리(JS 에서 파일 상태 직접 관리)

    photoInput.addEventListener("change", (e) => {
        const files = Array.from(e.target.files);
        //photoPreview.innerHTML = ""; // 기존 미리보기 초기화(누적 불가)

        // 최대 5장 제한
        if (selectedFiles.length + files.length > 5) {
        alert("사진은 최대 5장까지만 등록 가능합니다.");
        photoInput.value = "";
        return;
        }

        files.forEach((file) => {
        if (!file.type.startsWith("image/")) return;

        selectedFiles.push(file);

        const reader = new FileReader();
        reader.onload = (event) => {
            // 이미지 컨테이너
            const container = document.createElement("div");
            container.className = "preview-img-container";

            // 이미지
            const img = document.createElement("img");
            img.src = event.target.result;
            img.alt = "사진 미리보기";
            img.className = "preview-img";

            // 삭제 버튼
            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.className = "preview-remove";
            removeBtn.textContent = "×";

            removeBtn.addEventListener("click", () => {
                const index = Array.from(photoPreview.children).indexOf(container);
                selectedFiles.splice(index, 1);
                container.remove();

                /////
                refreshThumbnail();
            });

            container.appendChild(img);
            container.appendChild(removeBtn);
            photoPreview.appendChild(container);

            /////
            refreshThumbnail();
        };

        reader.readAsDataURL(file);
        });

    // 같은 파일 다시 선택 가능하게 초기화
    photoInput.value = "";
    });

    // 썸네일(대표) 이미지 갱신 (항상 첫 번째)
    function refreshThumbnail() {
        Array.from(photoPreview.children).forEach((container, index) => {
            container.classList.remove("thumbnail");

            const badge = container.querySelector(".thumbnail-badge");
            if (badge) badge.remove();

            if (index === 0) {
            container.classList.add("thumbnail");

            const badgeEl = document.createElement("div");
            badgeEl.className = "thumbnail-badge";
            badgeEl.textContent = "대표";

            container.appendChild(badgeEl);
            }
        });
    }


    const form = document.querySelector("form");
    //form.addEventListener("submit", (e) => {
    const submitBtn = document.getElementById('submitBtn'); //###LKSIURI
    submitBtn.addEventListener("click", (e) => {  //###LKSIURI
        e.preventDefault(); // 기본 submit 막기

        //  등록 확인 알림
        const ok = confirm("작성글을 등록하시겠습니까?");
        if (!ok) {
            return; // 취소 → submit 중단
        }
        /** 유효성 검사 **/
        const title = document.getElementById("titleInput").value.trim();
        const content = textarea.value.trim();

        if (title.length === 0) {
        alert("제목을 입력해주세요.");
        // e.preventDefault();
        return;
        }

        if (content.length < 10) {
        alert("내용은 최소 10자 이상 입력해주세요.");
        // e.preventDefault();
        return;
        }


        /**  FormData 생성 **/
        const formData = new FormData(form);

         formData.append("boardTitle", title); // ###LKSIURI
         formData.append("boardContent", content); // ###LKSIURI

        // 기존 images 제거 (중복 방지)
        formData.delete("images");

        // JS에서 관리하던 파일을 다시 넣는다
        selectedFiles.forEach((file) => {
            formData.append("images", file);
        });

        /** 서버 전송 **/
        //fetch(form.action, {
        fetch('/board2/freeboard/insert', { //###LKSIURI
            method: "POST",
            body: formData
        })
        .then(res => res.json()) // JSON을 JS 객체로
        .then(data => {
            alert(data.message); // 알림창 메세지

            if (data.success && data.redirectUrl) {
                //window.location.href = data.redirectUrl;
                location.href = data.redirectUrl; // JSON을 JS 객체로 // ###LKSIURI
            }
        })
        .catch(err => {
            console.error(err);
            alert("서버 통신 중 오류가 발생했습니다.")
        });
    });


});

// chatbot 팝업창 열기
function openHelper() {
    const select = document.getElementById("helperType");
    const selectedValue = select.value;

    let url = "";
    let pWinName = "";

    if (selectedValue === "ai") {
        url = "/api/ai/freeboard/page";
        pWinName = "ai";
    } else if (selectedValue === "chatbot") {
        url = "/api/chatbot/freeboard/popupBasicChatbot";
        pWinName ="chatbot";
    }

    if (!url) return;

    // // 부모(수정화면창) → 자식 팝업(챗봇 basic 팝업창)으로 전역 변수 전달하기 위함
    // window.globalData = {
    //     boardNo: window.boardNo,
    //     loginMemberNo: window.loginMemberNo
    //     // more variables
    // };  

    window.open(
        url,
        //"helper", // 창이름 (같은이름의 창존재-> 기존 창 재사용, 없으면 새 창 생성)
        pWinName,
        "width=520,height=760"
    );
}


<!DOCTYPE html>
<html lang="ko" xmlns="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>게시글 수정</title>
    <link rel="stylesheet" th:href="@{/css/board/freeboard/freeboardUpdate.css}">
    <link rel="stylesheet" th:href="@{/css/common/font.css}">
    <link rel="stylesheet" th:href="@{/css/common/common.css}" />
    <link rel="stylesheet" th:href="@{/css/common/notification.css}" />
        
</head>

<body>
    <!-- <p th:text="${freeboard}" th:if="${freeboard != null}"></p>    -->
    <main>
        
        <!-- 헤더 -->
        <!-- <header class="main-header">header</header> -->
        <!-- header.html (fragment) 추가 -->
        <!-- <th:block th:replace="~{/common/header}">header.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/header :: header"></div>
        <script th:src="@{/js/common/header.js}"></script>
        
        <!-- 네비게이션 -->
        <nav class="main-nav"></nav>
        <!--  ###################################################### -->  
        
        <div class="top-space-bw-header"> </div>
        
        <!-- <p th:text="${freeboard}" th:if="${freeboard != null}"></p>    -->

        <!-- 상단 타이틀 바 -->
        <h2 class="title-main fw-800">자유게시판</h2>
        <div class="container">

            <!-- 글작성 도우미 -->
            <div class="helper-box">
                <button class="helper-btn" onclick="openHelper()">글수정 도우미</button>

                <div class="select-box">
                    <select class="ai-select" id="helperType">
                        <!-- <option class="sel-ai" value="ai">AI</option> -->
                        <option class="sel-chatbot" value="chatbot">챗봇</option>
                    </select>
                </div>
            </div>


            <!-- 작성 폼 -->  
            <form th:action="@{update}" method="post" enctype="multipart/form-data"
                    class="board-write" id="boardWriteFrm">     

                <!-- 제목 입력 -->
                <p id="updateText">게시글 제목 수정</p>
                <input type="text" id="titleInput" name="boardTitle" class="title-input" th:value="${freeboard.boardTitle}" maxlength="300" required>

                <!-- 사진 등록 -->
                <div class="photo-header">
                    <!-- <span class="photo-title-spaceholder"></span> -->
                    <span class="photo-title">등록 사진 수정 <p>썸네일(대표) 이미지는 첫 사진입니다.</p></span>
                    <span class="photo-max">최대 5장</span>
                </div>

                <!-- 미리보기 이미지 + 업로드 박스 -->
                <!-- <div class="photo-row"> -->
                <div class="photo-section">      
                    <div class="photo-upload-area">
                        <!-- 미리보기 영역 -->
                        <div id="photoPreview" class="photo-preview">
                            <th:block th:if="${#lists.size(freeboard.imageList) > 0 }"> 
                                <!--                                     start,        end,                     step -->
                                <th:block th:each="i : ${#numbers.sequence(0, #lists.size(freeboard.imageList)-1, 1)}">
                                        <div class="preview-img-container"  th:with="path=|${freeboard.imageList[i].imgPath}${freeboard.imageList[i].imgRename}|"
                                                                            th:data-img-no="${freeboard.imageList[i].imgNo}" > 
                                                                            <!-- 변수에 담아두고 div태그 안에서 쓴다; data-img-no는 기존이미지 인지 판별의 핵심  -->
                                            <img th:src="${path}" class="preview-img" alt="사진 미리보기">
                                            <button type="button" class="preview-remove">&times;</button>
                                        </div>
                                </th:block>
                            </th:block>
                        </div>
                        <!-- + 버튼 -->
                        <label for="photoInput" class="photo-upload">
                            <span class="plus">+</span>
                        </label>
                        <!-- 실제 파일 input (숨김) -->
                        <input type="file" id="photoInput" name="images" multiple accept="image/*" hidden />
                    </div>
                </div>

                <p class="image-warning">
                    본 사이트 약관/정책을 위반하는 이미지는 안내 없이 삭제 될 수 있습니다.
                </p>

                <!-- 내용 입력 -->
                <p id="updateText">게시글 내용 수정</p>
                <textarea id="contentInput" name="boardContent" minlength="10" maxlength="4000" 
                        class="content-box" th:text="${freeboard.boardContent}">수정할 게시글 내용
                </textarea>

                <div class="text-limit">최소 10자, 최대 4000자 (<span id="charCount">0</span> / 4000자)</div>

                <!-- 버튼 -->
                <div class="button-box">
                    <button type="submit" id="submitBtn" class="submit-btn">수정 완료</button>
                    <button type="button" class="cancel-btn"
                    th:onclick="|location.href='@{/board/freeboard/}${boardNo}'|">취소</button>
                </div>


                 <input type="hidden" name="deleteList" value=""> 
                <!-- <input type="hidden" name="deleteList" value="1,2,3" if used> -->                

                <input type="hidden" name="cp" th:value="${param.cp}">                
            </form>

        </div>

        <!--  ###################################################### -->
        <!-- <footer class="main-footer">footer</footer> -->
        <!-- footer.html 추가 -->
        <!-- <th:block th:replace="~{common/footer}">footer.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/footer :: footer"></div>

    </main>

    <script th:inline="javascript"> // freeboardDetail.js처럼 JS에서 사용할 전역 변수들을 선언~~

        let loginMemberNo = /*[[${session.loginMember?.memberNo}]]*/ null; 
        let memberNickname = /*[[${session.loginMember?.memberNickname}]]*/ null;
        if(loginMemberNo === null) loginMemberNo = ""; // 들어가는 값이 없으면 대신 빈칸을 넣어준다 (아래 boardDetail.js, comment.js에서 ""로 받아서 처리)
        
        // 명시적으로 전역 등록
        window.loginMemberNo = loginMemberNo;
        window.memberNickname = memberNickname;        
        window.boardNo = /*[[${freeboard?.boardNo}]]*/ null;
        window.boardCode = /*[[${freeboard?.boardCode}]]*/ null;
        window.boardTitle = /*[[${freeboard?.boardTitle}]]*/ null;
        
        console.log("window.boardNo = ", window.boardNo);
    </script>    

    <!-- 알림창 띄우기 -->
    <script th:inline="javascript"> 
        const message = /*[[${message}]]*/ "전달 받은 message";
        if(message != null) alert(message); // message12가 없으면 null값
    </script>
        
    <!-- freeboardUpdate.js 추가 -->
    <script th:src="@{/js/board/freeboard/freeboardUpdate.js}"></script>    

</body>

</html>


/* 기본 설정 */
body {
    /* background: #fafafa; */
    background-color: #ffffff;  
    margin: 0;
    padding: 0;
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
}

/* header와의 간격벌리기 */
.top-space-bw-header{
    width: 10px;
    height: 10px;
    background-color: white;
    margin-bottom: 150px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

/* 상단 타이틀 바 */
.title-main {
    background: linear-gradient(
        to right,
        rgba(241, 198, 231, 1) 0%,       /* #F1C6E7 불투명도 100% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치도 불투명도 75% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치 투명도 75% */
        rgba(241, 198, 231, 0.5) 100%    /* 100% 위치 투명도 50% */
    );    
    padding: 22px 22px 22px 120px;
    /*border-radius: 6px;*/
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #000;
    font-size: 36px;
    font-weight: bolder;
    margin-bottom: 25px;
}

/* 전체 컨테이너 */
.container {
    max-width: 1440px; /* 내용 길이 1440px */
    margin: 30px auto;
    padding: 0 10px;
}

/* 글작성 도우미 */
.helper-box {
    display: flex;
    align-items: center;
    margin-top: 60px;
    margin-bottom: 100px;
    padding: 0px 50px;
}

.helper-btn {
    width: 260;
    height: 60;
    background: #BD83CE;
    border: 1px solid #BD83CE;
    border-radius: 6px;
    color: white;
    font-size: 36px;
    padding: 1px 20px;
    margin-right: 20px;
    cursor: pointer;    
}
.helper-btn:hover {
    background-color: #E5B0EA;
    border: 1px solid #E5B0EA;
}

/* .ai-select {
    margin-left: 10px;
    padding: 8px 10px;
    border-radius: 10px;
    border: 1px solid #dcdcdc;
    font-size: 14px;
} */

.select-box {
    position: relative;
    width: 260;
    /* height: 60;   */

}
.select-box select {
    width: 100%;
    padding:10px 70px 10px 10px;

    background: #F7E8F6;
    /* padding: 10px 6px; */
    border-radius: 6px;
    /*  */
    font-size: 32px;
    font-weight: bolder;
    /* margin-left: 15px;     */

    appearance: none; /* 기본화살표 숨기기 */
    -webkit-appearance: none;
    -moz-appearance: none;
}
/* 커스텀 화살표 */
.select-box::after { /* .select-box 요소 뒤에 가상의 요소로 커스텀 화살표 생성: 실제 HTML에는 없지만 화면에는 보임*/
    content: "";
    position: absolute;
    right: 0px;
    top: 51%;
    transform: translateY(-50%);

    width: 60px;          /* 화살표-png 크기 */
    height: 60px;
    background-image: url("../../../images/board/freeboard/fb_select_SortDown3.png");
    background-repeat: no-repeat;
    background-size: contain; /* 또는 cover */
    pointer-events: none;
}


/* 제목 입력 */
.title-input {
    /* width: 100%;
    height: 55px;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dcdcdc;
    font-size: 15px;
    background: #ffffff; */

    height: 127px;
    width: 80%; /* 내용 길이 1440px의 80% */
    margin-left: 110px;
    padding: 15px 0px 15px 20px;
    border: 1px solid #CFCFCF;
    border-radius: 20px;
    font-size: 36px;
    /* color: #B4B4B4; */
    margin-bottom: 60px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* 사진 영역 */
.photo-header {
    /* display: flex;
    justify-content: space-between;
    margin-top: 20px; */

    width: 80%;
    margin-left: 130px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;    
}

.photo-title-spaceholder{
    width: 600px; /* (preview-img 크기: 200px  ) x preview-img갯수  */
}

.photo-title {
    /* font-size: 15px;
    font-weight: 600; */
    font-weight: bold;
    font-size: 36px;    

}
.photo-max {
    /* font-size: 12px;
    color: #777; */
    font-size: 36px;
    color: #B4B4B4;
    margin-right:90px;    
}


/* 사진 업로드 박스 */
/* 사진 */
.photo-upload {

    /* width: 200px;
    height: 200px; */
    width: 175px;
    height: 175px;
    /* margin-left: 10px;
    margin-top: 20px;    */
    border: 1px solid #ccc;
    background: #fbfbfb;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;    

    flex-shrink: 0; /* 부모 컨테이너 공간이 부족해도 이 요소는 크기를 줄이지 않는다 (스크롤 생김)*/
}

/* .photo-upload:hover {
    background-color: #F7E8F6;
} */

.plus {
    font-size: 50px;
    font-weight: 100;
    color: #8E8E8E;
}

/* 이미지 경고글 */
.image-warning {
    font-size: 36px;
    margin-left: 130px;   
    margin-top: 35px;
    color: #B4B4B4;

}

/* 이미지 미리보기(preview-img) + 업로드(photo-upload) */
/* photo-row vs. photo-section */
.photo-row { 
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
    flex-wrap: wrap;
    padding-left: 120px;
}


/* .preview-img {
    object-fit: cover;
    border-radius: 6px;

    width: 175px;
    height: 175px;    
    margin-left: 10px;
    margin-top: 20px;   

    border-radius: 0px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;      
} */

/* ===== 사진 업로드 박스: 추가 ===== */
/* 썸네일 지정 알림 텍스트 */
.photo-title p{ 
    color: #B4B4B4;
    font-size: 24px;
    padding-left: 40px;
}

.photo-section {
    width: 100%;
    margin-top: 30px;
}

.photo-upload-area {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-left: 130px;
    margin-bottom: 10px;
}


.photo-preview {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: flex-start;
}

.preview-img-container {
    position: relative;
    /* width: 200px;
    height: 200px; */
    width: 175px;
    height: 175px;    
    /*  */
    /* display: flex;
    align-items: center;
    justify-content: center; */
}

.preview-img {
    /* width: 200px;
    height: 200px; */
    width: 175px;
    height: 175px;    
    object-fit: cover;
    border-radius: 6px;
    
    /*  */
    display: flex;
    align-items: center;
    justify-content: center;
}

/* .preview-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 6px;
} */

.preview-remove {
    position: absolute;

    top: -8px;
    right: -8px;
    width: 24px;
    height: 24px;
    background-color: #f74c3c;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 14px;
    font-weight: bold;
    transition: background-color 0.2s;
}

.preview-remove:hover {
    background-color: #80392b;
}

/* 썸네일(대표) 이미지 강조 */
.preview-img-container.thumbnail {
    outline: 4px solid #F7A1C4;
}

.thumbnail-badge {
    position: absolute;
    bottom: 8px;
    left: 8px;
    background-color: #F7A1C4;
    color: white;
    font-size: 12px;
    padding: 4px 6px;
    border-radius: 4px;
    font-weight: bold;
}



/* 본문 내용: 게시글 내용 입력  */
.content-box {

    /* width: 100%; */
    height: 463px;
    width: 80%;
    margin-left: 110px;    
    margin-top: 0px;
    /* padding: 15px; */
    padding: 15px 10px;
    resize: none;
    border: 1px solid #B4B4B4;
    border-radius: 20px;
    font-size: 30px;
    line-height: 1.4;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);    
}

/* 글자수 안내 */
.text-limit {
    width: 80%;
    margin-left: 70px;  
    margin-right: 40px;        
    text-align: right;
    margin-top: 5px;
    font-size: 36px;
    color: #B4B4B4;    
}

/* 버튼 */
.button-box {
    width: 82%;
    margin-left: 110px;       
    /* margin-right: 80px;     */
    text-align: right;
    margin-top: 100px;
    margin-bottom: 200px;
}

.submit-btn {
    width: 180px;
    height: 60px;
    background: #BD83CE;
    color: white;
    padding: 0px 2px;
    border: none;
    border-radius: 6px;
    font-size: 35px;
    cursor: pointer;    
}
.submit-btn:hover {
    background: #E5B0EA;
}

.cancel-btn {
    width: 180px;
    height: 60px;    
    background: #BD83CE;
    color: white;
    padding: 0px 2px;
    border: none;
    border-radius: 6px;
    font-size: 35px;
    margin-left: 5px;
    /* margin-right: 120px; */
    cursor: pointer;
}
.cancel-btn:hover {
    background: #E5B0EA;
}


#updateText {
    font-weight: bold;
    font-size: 36px;
    margin-left: 130px;    
}


console.log("freeboardUpdate.js v2 (fixed) loaded");

const deleteSet = new Set();

let photoPreview;
let selectedFiles = []; // 전역 변수로 파일 상태 관리

document.addEventListener("DOMContentLoaded", () => {

    photoPreview = document.getElementById("photoPreview");

    if (!photoPreview) {
        console.log("photoPreview 없음 -> 이미지 없는 수정 페이지");
        return;
    }

    /** DOM에 이미 그려진 이미지 -> selectedFiles로 옮기기 **/
    initExistingImages();    
    /** 기존 이미지 이벤트 바인딩 함수 추가 **/
    bindExistingRemoveButtons();  

    /** 글자 수 카운트 **/
    const textarea = document.getElementById("contentInput");
    const charCount = document.getElementById("charCount");

    textarea.addEventListener("input", () => {
        const length = textarea.value.length;
        charCount.textContent = length;
        if (length > 4000) {
            textarea.value = textarea.value.substring(0, 4000);
            charCount.textContent = 4000;
        }
    });

    /** 이미지 미리보기 **/
    const photoInput = document.getElementById("photoInput");

    photoInput.addEventListener("change", (e) => {
        const files = Array.from(e.target.files);

        // 최대 5장 제한
        if (selectedFiles.length + files.length > 5) {
            alert("사진은 최대 5장까지만 등록 가능합니다.");
            return;
        }

        // placeholder 컨테이너를 미리 순서대로 DOM에 추가
        files.forEach((file) => {
            if (!file.type.startsWith("image/")) return;

            // selectedFiles에 새 이미지 추가
            selectedFiles.push({
                type: "NEW",
                file: file
            });

            // placeholder 컨테이너 미리 생성 및 DOM에 추가
            const container = document.createElement("div");
            container.className = "preview-img-container";
            photoPreview.appendChild(container);

            // 비동기로 이미지 로드
            const reader = new FileReader();
            reader.onload = (event) => {
                // 이미지
                const img = document.createElement("img");
                img.src = event.target.result;
                img.alt = "사진 미리보기";
                img.className = "preview-img";

                // 삭제 버튼
                const removeBtn = document.createElement("button");
                removeBtn.type = "button";
                removeBtn.className = "preview-remove";
                removeBtn.textContent = "×";

                removeBtn.addEventListener("click", () => {
                    handleRemove(container);
                });

                // 이미 DOM에 추가된 container에 내용만 채움
                container.appendChild(img);
                container.appendChild(removeBtn);

                // 썸네일 갱신
                refreshThumbnail();
            };

            reader.readAsDataURL(file);
        });

        // 같은 파일 다시 선택 가능하게 초기화
        photoInput.value = "";
    });


    // submit 시 FormData 구성
    const form = document.querySelector("form");
    //form.addEventListener("submit", (e) => {
    const submitBtn = document.getElementById('submitBtn'); // ###LKSIURI
    submitBtn.addEventListener("click", (e) => {  // ###LKSIURI	
        e.preventDefault();

        const ok = confirm("작성글을 수정하시겠습니까?");
        if (!ok) {
            return;
        }

        /** 유효성 검사 **/
        const title = document.getElementById("titleInput").value.trim();
        const content = textarea.value.trim();

        if (title.length === 0) {
            alert("제목을 입력해주세요.");
            return;
        }

        if (content.length < 10) {
            alert("내용은 최소 10자 이상 입력해주세요.");
            return;
        }

        /**  FormData 생성 **/
        const formData = new FormData(form);

        formData.append("boardTitle", title); // ###LKSIURI
        formData.append("boardContent", content); // ###LKSIURI
        
        // 기존 images 제거 (중복 방지)
        formData.delete("images");

        // 새 이미지만 images로 전송
        selectedFiles
            .filter(item => item.type === "NEW")
            .forEach(item => {
                formData.append("images", item.file);
            });

        // 유지할 기존 이미지 PK + 순서
        const existingImgNos = selectedFiles
            .filter(item => item.type === "EXISTING")
            .map(item => item.imgNo);

        formData.append(
            "existingImgNos",
            JSON.stringify(existingImgNos)
        );

        console.log("=== V2 전송 데이터 확인 ===");
        console.log("selectedFiles:", selectedFiles);
        console.log("새 이미지 개수:", formData.getAll("images").length);
        console.log("기존 이미지 번호:", existingImgNos);

        /** 서버 전송 **/
        ////fetch(form.action, { //  <form th:action="@{update}" method="post" enctype="multipart/form-data"></form>
		////fetch('/board2/freeboard/update', { // ###LKSIURI - 1th (initial: redirection issue)
		//fetch('/board2/freeboard/insert', { // ###LKSIURI-monkeyPatch - 2nd  (monkeyPatch: insert + del까지만)
        // ##### 원래 게시글 수정으로 복귀 - 3rd (이제 유효한 update로 복귀)
        const origBoardNo = parseInt(window.boardNo);
        const addrUpdate3rd = '/board2/freeboard/'+ origBoardNo + '/update' ; 
        console.log("addrUpdate3rd = ", addrUpdate3rd);
        fetch(addrUpdate3rd, { // ##### 원래 게시글 수정으로 복귀 - 3rd (이제 유효한 update로 복귀)
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {


            if (data.success) { // ##### 원래 게시글 수정으로 복귀 - 3rd (이제 유효한 update로 복귀)
                alert(data.message);
                //window.location.href = data.redirectUrl;
                location.href = data.redirectUrl; // JSON을 JS 객체로 // ###LKSIURI
            } else {
                alert(data.message);
            }


        })
        .catch(err => {
            console.error(err);
            alert("오류가 발생했습니다.");
        });







    });

});

// chatbot 팝업창 열기
function openHelper() {
    const select = document.getElementById("helperType");
    const selectedValue = select.value;

    let url = "";
    let pWinName = "";

    if (selectedValue === "ai") {
        url = "/api/ai/freeboard/page";
        pWinName = "ai";
    } else if (selectedValue === "chatbot") {
        url = "/api/chatbot/freeboard/popupBasicChatbot";
        pWinName ="chatbot";
    }

    if (!url) return;
    
    // 부모(수정화면창) → 자식 팝업(챗봇 basic 팝업창)으로 전역 변수 전달하기 위함
    window.globalData = {
        boardNoGlobal: window.boardNo,
        loginMemberNoGlobal: window.loginMemberNo
        // more variables
    };

    window.open(
        url,
        pWinName,
        "width=520,height=760"
    );
}

// 썸네일(대표) 이미지 갱신 (항상 첫 번째)
function refreshThumbnail() {
    if (!photoPreview) return;

    const containers = photoPreview.querySelectorAll(".preview-img-container");

    containers.forEach((container, index) => {
        container.classList.remove("thumbnail");

        const badge = container.querySelector(".thumbnail-badge");
        if (badge) badge.remove();

        // DOM에서 첫 번째가 대표
        if (index === 0) {
            container.classList.add("thumbnail");

            const badgeEl = document.createElement("div");
            badgeEl.className = "thumbnail-badge";
            badgeEl.textContent = "대표";
            container.appendChild(badgeEl);
        }
    });
}

// DOM에 이미 그려진 이미지 → selectedFiles로 옮기기
function initExistingImages() {
    if (!photoPreview) return;

    const containers = document.querySelectorAll(
        "#photoPreview .preview-img-container"
    );

    containers.forEach(container => {
        const imgNo = container.dataset.imgNo;

        selectedFiles.push({
            type: "EXISTING",
            imgNo: imgNo
        });
    });

    refreshThumbnail();
}

// 기존 이미지 vs 새 이미지 구분해서 삭제
function handleRemove(container) {
    const index = Array.from(photoPreview.children).indexOf(container);
    const fileInfo = selectedFiles[index];

    console.log("=== 삭제 시작 ===");
    console.log("삭제 인덱스:", index);
    console.log("삭제 대상:", fileInfo);
    console.log("삭제 전 selectedFiles:", [...selectedFiles]);

    // 마지막 이미지 삭제 방지
    if (selectedFiles.length === 1) {
        alert("최소 1장의 이미지는 반드시 필요합니다.");
        return;
    }

    // 대표 이미지 삭제 경고
    if (index === 0) {
        const ok = confirm(
            "대표 이미지입니다.\n삭제 시 다음 이미지가 대표로 지정됩니다.\n삭제하시겠습니까?"
        );
        if (!ok) return;
    }    

    // 기존 이미지인 경우
    if (fileInfo.type === "EXISTING") {
        const imgNo = fileInfo.imgNo;

        if (!confirm("이미지를 삭제하시겠습니까?")) return;

        fetch(`/board2/freeboard/deleteImage/${imgNo}`, {
            method: "DELETE"    
        })
        .then(res => {
            if (!res.ok) throw new Error("삭제 실패");
            return res.json();
        })
        .then(data => {
            // 서버 삭제 성공 시
            selectedFiles.splice(index, 1);
            container.remove();
            console.log("=== 삭제 완료 ===");
            console.log("삭제 후 selectedFiles:", [...selectedFiles]);
            console.log("삭제 후 DOM 개수:", photoPreview.children.length);
            refreshThumbnail();
        })
        .catch(err => {
            alert("이미지 삭제 중 오류가 발생했습니다.");
            console.error(err);
        });

    } else {
        // 새 이미지인 경우 (서버 요청 X)
        selectedFiles.splice(index, 1);
        container.remove();
        console.log("=== 삭제 완료 (새 이미지) ===");
        console.log("삭제 후 selectedFiles:", [...selectedFiles]);
        console.log("삭제 후 DOM 개수:", photoPreview.children.length);
        refreshThumbnail();
    }
}

// 기존 이미지 이벤트 바인딩 함수
function bindExistingRemoveButtons() {
    const containers = document.querySelectorAll(
        "#photoPreview .preview-img-container"
    );

    containers.forEach(container => {
        const removeBtn = container.querySelector(".preview-remove");

        if (!removeBtn) return;

        removeBtn.addEventListener("click", () => {
            handleRemove(container);
        });
    });
}






이제 2번의 마지막 2-C단계에서는 댓글 목록조회, 상세조회, 수정/삭제기능에 대한 frontend 파일들 comment.html, comment.css, freeboardComment.js을 porting하도록 하자.  아래 이번 단계 해당 파일들을  첨부 할께,  이것들 모두 FastAPI와 native JS 기반 프론트엔드에 맞게 바꿔줘. 이 모든 것들을 네가 이미 작성해준 main.html과 main.css,main.js들, 그리고 위의 2-A & 2-B단계에서 작성해준 html, css, js 파일들과  잘 integrated되게 작성해줘.


<div class="container">

    <!-- 상단 라인 -->
    <div class="fb-line"></div>

    <div id="commentTitle">
        <h3 class="title">댓글</h3>
    </div>

    <div class="fb-line"></div>


    <!-- 댓글 영역: [A] 달린 댓글(리스트) + [B] 댓글 창 -->
    <div id="commentArea">

        <!-- [A] 달린 댓글 목록 -->
        <div class="comment-list-area">
            <ul id="commentList">
                <!-- 댓글 1 -->
                <li class="comment-row" th:each="comment : ${commentList}"
                    th:classappend="${comment.parentCommentNo != 0} ? 'reply'" th:data-comment-id="${comment.commentNo}">
                    <div class="comment-item">
                        <!-- 작성자 프로필 이미지 -->
                        <img 
                            th:if="${comment.profileImg != null}"
                            th:src="@{${comment.profileImg}}" 
                            class="profile-img"/>
                        <img 
                            th:unless="${comment.profileImg != null}"
                            th:src="@{/images/user.png}" 
                            class="profile-img"/>

                        <!-- 작성자 닉네임 + 작성 답글 -->
                        <div class="comment-info">
                            <div>
                                <div class="comment-nickname" th:text="${comment.memberNickname}">답글작성자닉네임</div>
                                <div class="comment-date" th:text="${comment.cCreateDate}" >답글작성일</div>
                            </div>
                            <div class="comment-content"  th:text="${comment.commentContent}">답글 내용</div>
                        </div>
                        <!-- 수정/삭제버튼, 로그인회원==작성자 -->
                        <th:block
                        th:if="${session.loginMember != null and session.loginMember.memberNo == comment.memberNo}"
                        >
                            <div class="comment-actions">
                                <button class="action-btn" th:onclick="|showUpdateComment(${comment.commentNo}, this)|">수정</button>
                                <button class="action-btn" th:onclick="|deleteComment(${comment.commentNo})|">삭제</button>
                            </div>
                        </th:block>
                    </div>

                </li>

            </ul>
        </div>

        <!-- [B] 댓글 작성: (로그인 회원만, 비회원처리?) -->            
        <div class="comment-write-wrapper">
            <!-- 입력 박스 -->
            <textarea id="commentContent" class="comment-input" placeholder="댓글을 입력하세요"></textarea>
            <!-- 등록 버튼 -->
            <button id="addComment" class="submit-btn">댓글등록</button>

        </div>

    </div>

</div>



/* section, div{ border : 1px solid black;}  */

/* === 전체 초기화 및 공통 설정 === */
*,
*::before,
*::after {
    box-sizing: border-box;
    font-family: 'Pretendard Variable', sans-serif;
}

body {
    margin: 0;
    padding: 0;
}

html, body {
    height: 100%;
}

/* 기본 설정 */
body {
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
}

/* 전체 컨테이너 */
.container {
    max-width: 1440px; /* 내용 길이 1440px */
    margin: 30px auto;
    padding: 0 10px;
}

/* 구분선 */
/* <!-- <hr class="fb-line"> --> 일때 */
/* .fb-line {
    border: none;
    border-top: 4px solid #000;
    margin: 20px 0;
} */

/* <div class="fb-line"></div>  일때 */
.fb-line {
    border: none;
    border-top: 4px solid #000;
    margin: 20px 0;
}

/* 댓글 제목 */
.title {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    margin: 0;
}

/* 댓글 아이템 */
.comment-item {
    display: flex;
    align-items: flex-start;
    border-bottom: 1px solid #e5e5e5;
    padding: 15px 0;
}

/* 프로필 이미지 */
.profile-img {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 12px;
}

/* 댓글 내용 */
.comment-info {
    flex-grow: 1;
}

.comment-nickname {
    font-weight: 700;
    font-size: 32px;
}

.comment-content {
    font-size: 32px;
    color: #000;
}

/* 수정/삭제 버튼 */
.comment-actions {
    text-align: right;
    min-width: 80px;
}

.action-btn {
    margin-left: 10px;
    margin-right: 25px;
    font-size: 25px;
    color: #777;
    cursor: pointer;
    border: none;
    background-color: white;
}

.action-btn:hover {
    color: #BD83CE;
}


/* 입력 박스 영역 */
/* textarea + 버튼 정렬 */
.comment-write-wrapper{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

/* 댓글 입력 박스: 상세화면 댓글 textarea */
.comment-input {
    width:85%;
    border: 2px solid #ccc;
    padding: 18px;
    font-size: 32px;
    line-height: 1.7;
    border-radius: 6px;
    color: #000;
    margin-top: 35px;
}

/* 댓글 수정 입력 박스: 수정버튼 클릭시 생성되는 수정 댓글 textarea */
.update-textarea {
    width:65%;
    border: 2px solid #ccc;
    padding: 9px;
    font-size: 16px;
    line-height: 1.7;
    border-radius: 6px;
    color: #000;
}

.submit-btn {
    background: #BD83CE;
    color: white;
    padding: 10px 22px;
    font-size: 35px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-left: 10px;

    flex-shrink: 0; 
}

.submit-btn:hover {
    background: #E5B0EA;
}

.comment-date {
    font-size: 20px;
    color: #999;
    margin-left: 8px;
}

.comment-info > div:first-child {
    display: flex;
    align-items: center;
}

.comment-row {
    list-style: none;
}


console.log("freeboardComment.js loaded");


console.log("loginMemberNo:", loginMemberNo); // 로그인 회원번호 (비회원은 "")
console.log("boardNo:", boardNo); //  freeboard boardNo

// 댓글 목록 조회
function selectCommentList() {
    fetch("/board/freeboard/comment?boardNo=" + boardNo)
        .then((resp) => resp.json())
        .then((cList) => {
        console.log(cList);

        const commentList = document.getElementById("commentList"); // comment 담든 ul
        commentList.innerHTML = "";

        for (let comment of cList) {
            const commentRow = document.createElement("li"); // ul밑에 각 comment담는 li
            commentRow.classList.add("comment-row");

            // 작성자
            const commentItem = document.createElement("div");
            commentItem.classList.add("comment-item");

            // 프로필 이미지
            const profileImage = document.createElement("img");
            profileImage.classList.add("profile-img");
            if (comment.profileImg != null) {
                profileImage.setAttribute("src", comment.profileImg);
            } else {
                profileImage.setAttribute("src", "/images/user.png");
            }

            // 작성자 닉네임 + 작성 시간 + 답글 내용 container
            const commentInfo = document.createElement("div");
            commentInfo.classList.add("comment-info");

            const wrapperNicknameDate = document.createElement("div")
            // 작성자 닉네임
            const memberNickname = document.createElement("div");
            memberNickname.classList.add("comment-nickname")
            memberNickname.innerText = comment.memberNickname;
            // 작성일
            const commentDate = document.createElement("div");
            commentDate.classList.add("comment-date");
            commentDate.innerText = "(" + comment.cCreateDate + ")";
            wrapperNicknameDate.append(memberNickname, commentDate)


            // 댓글 내용
            const commentContent = document.createElement("div");
            commentContent.classList.add("comment-content");
            commentContent.innerText = comment.commentContent;

            commentInfo.append(wrapperNicknameDate, commentContent)

            // 여기까지 만든거 우선 commentItem에 담자.
            commentItem.append(profileImage, commentInfo)


            // 로그인한 회원번호와 댓글 작성자의 회원번호가 같을 때만 버튼 추가
            if (loginMemberNo && loginMemberNo == comment.memberNo) {
                const commentBtnArea = document.createElement("div");
                commentBtnArea.classList.add("comment-actions");

                // 수정 버튼
                const updateBtn = document.createElement("button");
                updateBtn.innerText = "수정";
                updateBtn.classList.add("action-btn")
                updateBtn.setAttribute(
                    "onclick",
                    "showUpdateComment(" + comment.commentNo + ", this)"


                );
                // 삭제 버튼
                const deleteBtn = document.createElement("button");
                deleteBtn.innerText = "삭제";
                deleteBtn.classList.add("action-btn")
                deleteBtn.setAttribute(
                    "onclick",
                    "deleteComment(" + comment.commentNo + ")"
                );


                commentBtnArea.append(updateBtn, deleteBtn);
                
                // 로그인한 회원번호와 댓글 작성자의 회원번호가 같을 때만 버튼 추가
                commentItem.append(commentBtnArea);
                
            }

            /////
            commentRow.append(commentItem);

            commentList.append(commentRow);
        }
        })
        .catch((err) => console.log(err));
}

// 댓글 등록
const addComment = document.getElementById("addComment");
const commentContent = document.getElementById("commentContent");

addComment.addEventListener("click", (e) => {
    console.log("댓글 등록 버튼 클릭");
    console.log("현재 loginMemberNo:", loginMemberNo);
    console.log("loginMemberNo 타입:", typeof loginMemberNo);

    // 로그인 체크
    if (!loginMemberNo || loginMemberNo == 0) {
        alert("로그인 후 이용해주세요.");
        return;
    }

    // 댓글 내용 체크
    if (commentContent.value.trim().length == 0) {
        alert("댓글을 작성한 후 버튼을 클릭해주세요.");
        commentContent.value = "";
        commentContent.focus();
        return;
    }

    // 비동기 요청을 통한 댓글 등록
    const data = {
        commentContent: commentContent.value,
        memberNo: loginMemberNo,
        boardNo: boardNo,
    };

    //fetch("/comment", {
    fetch("/board/freeboard/comment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
        .then((resp) => resp.text())
        .then((commentNo) => {
            if (commentNo > 0) {
                alert("댓글이 등록되었습니다.");
                console.log(commentNo);
                
                commentContent.value = "";

                // 댓글 목록 다시 불러와서 새로 등록된 댓글 보여주기 (화면새로고침)
                selectCommentList();
                
                // selectCommentList(); // 알림 요청
                // sendNotification(
                //     "insertComment",
                //     location.pathname + "?cn=" + commentNo, 
                //     boardNo,
                //      `<strong>${memberNickname}</strong>님이 <strong>${boardTitle}</strong> 게시글에 댓글을 작성했습니다.`

                // );
            } else {
                alert("댓글 등록에 실패했습니다...");
            }
        })
        .catch((err) => console.log(err));
});

// 댓글 삭제
function deleteComment(commentNo) {
    if (confirm("정말로 삭제 하시겠습니까?")) {
        const data = { commentNo: commentNo };

        fetch("/board/freeboard/comment", {
        method: "DELETE",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(data),
        })
        .then((resp) => resp.text())
        .then((result) => {
            if (result > 0) {
            alert("삭제되었습니다");
            selectCommentList();
            } else {
            alert("삭제 실패");
            }
        })
        .catch((err) => console.log(err));
    }
}

// 댓글 수정
let beforeCommentRow; // 수정할 댓글 (수정취소하면 이걸로 원복)

function showUpdateComment(commentNo, btn) {
    const temp = document.getElementsByClassName("update-textarea"); // 댓글 수정을 위해 생성되는 textarea입력 박스

    if (temp.length > 0) {
        if (confirm("다른 댓글이 수정 중입니다. 현재 댓글을 수정 하시겠습니까?")) {
            temp[0].parentElement.innerHTML = beforeCommentRow;
            // textarea의 parentElement가  commentRow임
        } else {
        return;
        }
    }

    const commentRow = btn.parentElement.parentElement.parentElement; // 클릭한 수정버튼을 포함하고 있는 댓글
    beforeCommentRow = commentRow.innerHTML; 

    let beforeContent = commentRow.children[0].children[1].children[1].innerHTML; // 수정할 댓글 내용

    commentRow.innerHTML = "";

    const textarea = document.createElement("textarea"); // 수정할 내용 입력할 textarea입력박스 생성
    textarea.classList.add("update-textarea");

    // XSS 방지 처리 해제
    beforeContent = beforeContent.replaceAll("&amp;", "&");
    beforeContent = beforeContent.replaceAll("&lt;", "<");
    beforeContent = beforeContent.replaceAll("&gt;", ">");
    beforeContent = beforeContent.replaceAll("&quot;", '"');

    textarea.value = beforeContent;
    commentRow.append(textarea); // 즉 현재 댓글 자리에 textarea 입력박스 생성

    ////////////////
    const commentBtnArea = document.createElement("div");
    commentBtnArea.classList.add("comment-actions");

    const updateBtn = document.createElement("button");
    updateBtn.innerText = "수정";
    updateBtn.classList.add("action-btn")
    updateBtn.setAttribute("onclick", "updateComment(" + commentNo + ", this)");

    const cancelBtn = document.createElement("button");
    cancelBtn.innerText = "취소";
    cancelBtn.classList.add("action-btn")
    cancelBtn.setAttribute("onclick", "updateCancel(this)");

    commentBtnArea.append(updateBtn, cancelBtn);
    commentRow.append(commentBtnArea);
}

// 댓글 수정 취소
function updateCancel(btn) {
    if (confirm("댓글 수정을 취소하시겠습니까?")) {
        btn.parentElement.parentElement.parentElement.innerHTML = beforeCommentRow; // 원래 댓글로 원복
        // 
        selectCommentList();
    }
}

// 댓글 수정
function updateComment(commentNo, btn) {
    const commentContent = btn.parentElement.previousElementSibling.value; //showUpdateComment()에서 더해준대로

    console.log("수정하는 댓글 내용:")
    console.log(commentContent);

    fetch("/board/freeboard/comment", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        commentNo: commentNo,
        commentContent: commentContent,
        }),
    })
        .then((resp) => resp.text())
        .then((result) => {
        if (result > 0) {
            alert("댓글이 수정되었습니다.");
            selectCommentList();
        } else {
            alert("댓글 수정 실패");
        }
        })
        .catch((err) => console.log(err));
}

document.addEventListener("DOMContentLoaded", () => {
    selectCommentList();
});




 3. 끝으로 첨부한 spring boot controller 로직을 위에 1번에서 첨부한 DTO들과 맞추어서 이들을 FastAPI 코드로 맞게 바꿔주고,  이번 단계에서  네가 바꿔준 자유게시판 기능 실행을 확인할 수 있도록 Dockerfile & docker-compose.yml을 변경/추가가 필요한 부분이 있다면 추가해서 수정해주고, 실제 동작을 테스트/확인하는 절차도 자세히 알려줘.
 
 
 package com.devlog.project.board.freeboard.controller;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Map;
import java.util.Date;
import java.util.HashMap;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.SessionAttribute;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.devlog.project.board.freeboard.model.dto.Freeboard;
import com.devlog.project.board.freeboard.model.service.FreeboardService;
import com.devlog.project.member.model.dto.MemberLoginResponseDTO;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Controller
@RequestMapping("/board")  
@RequiredArgsConstructor
public class FreeboardController {

	private final FreeboardService freeboardService;
	
	// 게시글 목록조회
	@GetMapping("/freeboard")   
	public String selectFreeboardList(
			@RequestParam(value="cp", required=false, defaultValue ="1") int cp 
			, Model model 
			, @RequestParam Map<String, Object> paramMap 
			, HttpSession session //// session에 담긴 "loginMember" 꺼내오기용
			) {  
		int boardCode = 3; // boardCode = 3:  freeboard in BoardType 테이블
		
		log.info("[ FreeboardController ] boardCode: {}, cp: {}", boardCode, cp); 			
		
		// 게시글 목록 조회 서비스 호출
		Map<String, Object> map = freeboardService.selectFreeboardList(boardCode, cp);		
		
		//log.info("Freeboard DB 목록조회, map.pagination, map.freeboardList : {}", map);
		
		// 조회 결과를 request scope에 세팅 후 forward
		model.addAttribute("map", map); //model : spring에서 사용하는 데이터 전달 객체 => js에서 이걸 받아 사용 (@PathVariable에 담긴 boardCode와 cp도 담겨져 넘어감)
				
		return "board/freeboard/freeboardList"; 
	}	
	
	
	// 게시글 상세조회
	@GetMapping("/freeboard/{boardNo}")
	public String selectFreeboardDetail( 
			//@PathVariable("boardNo") int boardNo
			@PathVariable("boardNo") Long boardNo
			, Model model 
			, RedirectAttributes ra 
			, @SessionAttribute(value = "loginMember", required=false) MemberLoginResponseDTO loginMember
			, HttpServletRequest req
			, HttpServletResponse resp
			) throws ParseException {
		
		int boardCode = 3; //  boardCode = 3 for freeboard
		Map<String, Object> map = new HashMap<String, Object>(); 
		log.info("Freeboard detail boardCode: {}", boardCode); 
		log.info("Freeboard detail boardNo: {}", boardNo);
		
		map.put("boardCode", boardCode);
		map.put("boardNo", boardNo);
			
		// 게시글 상세 조회 서비스 호출
		Freeboard freeboard = freeboardService.selectFreeboardDetail(map); 
		log.info("Freeboard detail (boardNo= {}): {}", boardNo, freeboard);
		model.addAttribute("freeboard", freeboard); 
		
		
		String path = null;
		if(freeboard != null) {  // boardNo의 게시글 존재하는 경우

			// 1) 현재 로그인한 상태인 경우
			// 로그인한 회원이 해당 게시글에 좋아요를 눌렀는지 확인
			if (loginMember != null) { // boardNo, memberNo
				// 회원 번호를 기존에 만들어둔 map에 추가
				map.put("memberNo", loginMember.getMemberNo()); // 담아 가서 필요없으면 않쓰면 됨
				
				// 좋아요 여부 확인 서비스 호출
				int result = freeboardService.boardLikeCheck(map);
				
				// 좋아요를 누른 적이 있을 경우
				if(result > 0) { // 화면에 하트 보여주기위해 누른적 있는지 알려주기 위해 Model 전달객체 사용
					model.addAttribute("likeCheck", "yes");
				}
			}

			// 2) 쿠키를 이용한 조회수 증가 
			//
			// 1) 비회원 또는 로그인한 회원의 글이 아닌 경우
			if(loginMember == null || 
				loginMember.getMemberNo() != freeboard.getMemberNo()) {
				
				// 2) 쿠키 얻어오기
				Cookie c = null;
				
				// 요청에 담겨있는 모든 쿠키 얻어오기
				Cookie[] cookies = req.getCookies();
				
				// 쿠키가 존재하는 경우
				if(cookies != null) {
					
					// 쿠키 중 "readBoardNo" 이름을 가진 쿠키를 찾아서 c에 대입
					for (Cookie cookie : cookies) {
						if(cookie.getName().equals("readBoardNo")) {
							c = cookie; // 기존에 쿠키가 존재 하면 그거 그냥 가져다 쓴다.
							break;
						}
					}
				} 
				
				// 3) 기존에 쿠키가 없거나
				//    존재는 하지만 현재 게시글 번호가 쿠기에 저장되지 않은 경우
				//    (오늘 해당 게시글을 본적이 없는 경우)
				
				int result = 0; // 결과값 저장 변수
				
				if (c==null) {
					// 쿠키 존재 X -> 하나 새로 생성
					c = new Cookie("readBoardNo", "|" + boardNo + "|");   
					
					// 조회수 증가 서비스 호출
					result = freeboardService.updateBoardCount(boardNo);
					
				} else { // 쿠키가 존재 O : 위에서 찾아 c에 담아 놓은 쿠키
					// 현재 게시글 번호가 있는지 확인
					// cookie.getValue() : 쿠키에 저장된 모든 값을 읽어와서 String으로 반환
					
					// String.indexOf("문자열")
					// -> 찾는 문자열이 몇번 째 인덱스에 존재하는지 반환
					//    단, 없는 경우 -1 반환
					
					if(c.getValue().indexOf("|" + boardNo + "|") == -1) {
						// 쿠키에 현재 게시글 번호가 없다면					
						// 기존 쿠키 값에 게시글 번호를 추가해서 다시 세팅
						c.setValue(c.getValue() + "|" + boardNo + "|");
						
						// 조회수 증가 서비스 호출
						result = freeboardService.updateBoardCount(boardNo);
					}
				}
				
				// 4) 조회수 증가 성공 시 ( readCount 업데이트 필요)
				//    쿠키가 적용되는 경로, 수명(당일 23시 59분 59초) 지정
				if (result != 0 ) {
					// 조회된 board의 조회수와 DB의 조회수 동기화 
					freeboard.setBoardCount(freeboard.getBoardCount() + 1);
					
					// [ 쿠키 적용 경로 설정 ]
					c.setPath("/"); // "/" 이하 경로 요청 시 쿠키 서버로 전달 (모든 요청할 때 마다 쿠키가 담긴다)
					
					// [ 쿠키 수명 지정 (Date보다 Calendar가 개선된 시간관련 클래스) ]
					Calendar cal = Calendar.getInstance();  // 클래스명.메소드명 -> static 메소드
															
					cal.add(Calendar.DATE, 1); // 1일
					
					// 날짜 표기법 변경 객체
					SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
					
					// java.util.Date
					Date current = new Date(); // 현재 시간
					
					Date temp = new Date(cal.getTimeInMillis()); 
					
					Date tmr = sdf.parse(sdf.format(temp)); // temp를 "yyyy-MM-dd" 형식
					 
					// 내일 0시 0분 0초 - 현재 시간 -> 쿠키 수명
					long diff = (tmr.getTime() - current.getTime()) / 1000; // .getTime() 반환형이 long 타입
					
					c.setMaxAge((int)diff); //.setMaxAge 파라미터는 int이므로 강제 형변환
					
					// [ 쿠키를 resp에 담아서 보낸다 ]
					resp.addCookie(c); // 응답 객체를 이용하여 클라이언트에게 전달
					
				}
				
			}
			
			//---------------------------------------------------------
			path = "board/freeboard/freeboardDetail";
			
			
		} else { // boardNo의 게시글 없는 경우
			path = "redirect:/board/freeboard"; // ==> 게시글 목록조회 로  
			ra.addFlashAttribute("message",  "해당 게시글이 존재하지 않습니다." ); 
		}
		
		return path;
	}	
	
	
	
	// 좋아요 처리
	@PostMapping("/freeboard/like")
	@ResponseBody // 반환되는 값이 비동기 요청한 곳으로 돌아가게 함; AJAX 처리
	public int like(@RequestBody Map<String, Integer> paramMap) { // Map<k, v> Object대신 Integer로 받으면 down-casting해줄 필요 없음
		System.out.println(paramMap); // {memberNo=1, boardNo=7, check=0}
		
		return freeboardService.like(paramMap);
	}		
	
	
}

package com.devlog.project.board.freeboard.model.service;


import java.util.List;
import java.util.Map;

import com.devlog.project.board.freeboard.model.dto.Freeboard;

public interface FreeboardService {

	/** 게시판 종류 조회
	 * @return boardTypeList
	 * 
	 */
	List<Map<String, Object>> selectBoardTypeList();


	/** 게시글 목록조회 (boardCode=3 자유 게시판)
	 * @param boardCode
	 * @param cp
	 * @return map
	 */
	Map<String, Object> selectFreeboardList(int boardCode, int cp);


	/** 게시글 상세조회 (boardCode=3 자유 게시판)
	 * @param map (여기에 boardCode, boardNo 담겨있음)
	 * @return Freeboard DTO
	 */
	Freeboard selectFreeboardDetail(Map<String, Object> map);

	
	/** 조회수 증가
	 * @param boardNo
	 * @return count
	 */
	//int updateBoardCount(int boardNo);
	int updateBoardCount(Long boardNo);

	
	/** 좋아요 여부 확인
	 * @param map
	 * @return result
	 */
	int boardLikeCheck(Map<String, Object> map);


	/** 좋아요 처리 서비스
	 * @param paramMap
	 * @return count
	 */
	int like(Map<String, Integer> paramMap);
}


package com.devlog.project.board.freeboard.model.service;


import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.RowBounds;
import org.springframework.stereotype.Service;

import com.devlog.project.board.freeboard.model.dto.Freeboard;
import com.devlog.project.board.freeboard.model.dto.PaginationFB;
import com.devlog.project.board.freeboard.model.mapper.FreeboardMapper;
import com.devlog.project.notification.NotiEnums;
import com.devlog.project.notification.dto.NotifiactionDTO;
import com.devlog.project.notification.service.NotificationService;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class FreeboardServiceImpl implements FreeboardService {

	private final FreeboardMapper mapper;
	private final NotificationService notiService;
	
	@Override
	public List<Map<String, Object>> selectBoardTypeList() {
		return mapper.selectBoardTypeList();
	}
	
	// 게시글 목록 조회	
	@Override                  
	public Map<String, Object> selectFreeboardList(int boardCode, int cp) {
		// 1. 특정 게시판의 삭제되지 않은 게시글 수 조회
		int listCount = mapper.getFreeboardListCount(boardCode);
		
		
	    // 2. 1번의 조회 결과 + cp를 이용해서 Pagination 객체 생성
	    PaginationFB pagination = new PaginationFB(cp, listCount);

	    // 3. 특정 게시판에서 현재 페이지에 해당하는 부분에 대한 게시글 목록 조회
	    // -> 어떤 게시판(boardCode)에서
	    //    몇 페이지(pagination.currentPage)에 대한
	    //    게시글 몇 개 (pagination.limit) 조회

	    // 1) offset 계산
	    int offset = (pagination.getCurrentPage() - 1) * pagination.getLimit();

	    // 2) RowBounds 객체 생성
	    RowBounds rowBounds = new RowBounds(offset, pagination.getLimit());

	    List<Freeboard> freeboardList = mapper.selectFreeboardList(boardCode, rowBounds); 

	    // 4. pagination, boardList를 Map에 담아서 반환
	    Map<String, Object> map = new HashMap<String, Object>();
	    map.put("pagination", pagination);
	    map.put("freeboardList", freeboardList);
	    
	    return map;
	}


	// 게시글 상세 조회	
	@Override
	public Freeboard selectFreeboardDetail(Map<String, Object> map) {
		
	    return mapper.selectFreeboardDetail(map);
	}

	// 조회수 증가
	@Override
	//public int updateBoardCount(int boardNo) {
	public int updateBoardCount(Long boardNo) {
		return mapper.updateBoardCount(boardNo);
	}	
	
	// 상세 게시글 좋아요 여부 확인
	@Override
	public int boardLikeCheck(Map<String, Object> map) {
		return mapper.boardLikeCheck(map);
	}

	// 상세 게시글 좋아요 처리 서비스
	@Override
	public int like(Map<String, Integer> paramMap) {
		int result = 0;

		if(paramMap.get("check") == 0) { // 좋아요 X 상태
			// BOARD_LIKE 테이블 INSERT
			result = mapper.insertBoardLike(paramMap);
			
			// 본인 게시글 좋아요 아닐 경우에 알림
			Long receiver = mapper.selectReceiverNo(paramMap.get("boardNo"));
			Long sender = ((Number)paramMap.get("memberNo")).longValue();
			if(result != 0 && !sender.equals(receiver)) {
				
				String boardTitle = mapper.selectBoardTitle(paramMap.get("boardNo"));
				
				
				String memberNickname = mapper.selectMemberNickname(receiver);
				
				NotifiactionDTO notification = NotifiactionDTO.builder()
						.sender(((Number)paramMap.get("memberNo")).longValue())
						.receiver(receiver)
						.content(memberNickname +"님이 회원님의 게시글에 좋아요를 눌렀습니다.")
						.preview(boardTitle)
						.type(NotiEnums.NotiType.LIKE)
						.targetType(NotiEnums.TargetType.BOARD)
						.targetId(((Number)paramMap.get("boardNo")).longValue())
						.build();
				
				notiService.sendNotification(notification);
			}
			
			

		} else { // 좋아요 O 상태
			// BOARD_LIKE 테이블 DELETE
			result = mapper.deleteBoardLike(paramMap);
		}

		// SQL 수행 결과가 0 == DB 또는 파라미터에 문제가 있음
		// -> 에러를 나타내는 임의의 값을 반환(-1)
		if(result == 0) return -1;

		// 현재 게시글의 좋아요 개수 조회
		return mapper.countBoardLike(paramMap.get("boardNo"));
	}
	
}






package com.devlog.project.board.freeboard.controller;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.devlog.project.board.freeboard.model.dto.Freeboard;
import com.devlog.project.board.freeboard.model.service.FreeboardService;
import com.devlog.project.board.freeboard.model.service.FreeboardService2;
import com.devlog.project.member.model.dto.MemberLoginResponseDTO;

import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Controller
@RequestMapping("/board2")
@RequiredArgsConstructor
public class FreeboardController2 {
	
	private final FreeboardService freeboardService;
	
	private final FreeboardService2 service;
	
	// [A] 게시글 작성 화면 전환(GetMapping())
	@GetMapping("/freeboard/insert") 
	public String freeboardInsert( //@PathVariable("boardCode") int boardCode
			 HttpSession session // 
			) {
		
		
		int boardCode = 3; // for freeboard
		Map<String, Object> map = new HashMap<String, Object>(); 
		log.info("Freeboard Insert boardCode: {}", boardCode); 	
		map.put("boardCode", boardCode);	
		
		return "board/freeboard/freeboardWrite";  // forward하겠다. (리다이렉트는 "redirect:board/freeboard/freeboardWrite"로 해야함)
	}
		
	
	// [B] 게시글 작성 (작성완료 버튼 클릭시)(PostMapping())
	@PostMapping("/freeboard/insert")
	@ResponseBody
	public Map<String, Object> boardInsert(
			Freeboard freeboard // 커맨드 객체
			, @RequestParam(value="images", required=false) List<MultipartFile> images 
			, HttpSession session // 파일 저장 경로
			, RedirectAttributes ra
			) throws IllegalStateException, IOException {

		log.info("[ FreeboardController ] freeboard =  {}", freeboard); 
		//log.info("[ FreeboardController ] images.size() =  {}", images.size()); // images.size() null 방어필요
		
		MemberLoginResponseDTO loginMember = (MemberLoginResponseDTO) session.getAttribute("loginMember");
		log.info("loginMember from session.getAttribute(): {}", loginMember); 
		
		// 1. 로그인한 회원번호와 boardCode를 board에 세팅
		int boardCode = 3; // for freeboard
		freeboard.setBoardCode(boardCode);
		freeboard.setMemberNo(loginMember.getMemberNo());
		

		// 2. 게시글 삽입 서비스 호출 후 게시글 번호 반환 받기
		Long boardNo = service.freeboardInsert(freeboard, images);

		
		// 4. 게시글 삽입 서비스 호출 결과 후처리
		String message = null;
		String redirectUrl = null;
		Map<String, Object> result = new HashMap<>();
		
		if (boardNo > 0) {
			redirectUrl = "/board/freeboard/" + boardNo; // "redirect:" 가 prefix로 있어야 redirect 된다.
			message = "게시글이 등록 되었습니다.";
			
	        // 저장
	        result.put("success", true);
	        result.put("message", message);
	        result.put("redirectUrl", redirectUrl);			
		} else {
			redirectUrl = "/board2/freeboard/insert";
			message = "게시글 등록 실패. 잠시후 다시 시도해 주세요.";
			
	        // 저장
	        result.put("success", false);
	        result.put("message", message);
	        result.put("redirectUrl", redirectUrl);					
		}
		
		ra.addFlashAttribute("message", message); // alert메시지 출력

		return result; //결과데이터 JSON형식 
	}	
	
	
	// [C] 게시글 수정 화면 전환(GetMapping())
	@GetMapping("/freeboard/{boardNo}/update") 
	public String freeboardUpdate(
			@PathVariable("boardNo") int boardNo 
			, Model model ) {
		
		int boardCode = 3; // for freeboard
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("boardCode", boardCode);
		map.put("boardNo", boardNo); 
		
		// 게시글 상세 조회 서비스 호출 
		Freeboard freeboard = freeboardService.selectFreeboardDetail(map); 										 
		log.info("[ FreeboardController: Update-GET ] map for .selecFreeboardDetail(map):{}", map);
		log.info("[ FreeboardController: Update-GET ] freeboard in freeboardUpdate-GET:{}", freeboard); 
		model.addAttribute("freeboard", freeboard); 
		
		return "board/freeboard/freeboardUpdate"; 
	}	
	
	// [D] 게시글 수정중 기존이미지 삭제, AJAX 
	@DeleteMapping("/freeboard/deleteImage/{imgNo}")
	@ResponseBody
	public Map<String, Object> deleteImage(@PathVariable("imgNo") Long imgNo) {
	    boolean success = service.deleteFreeboardImage(imgNo);
	    return Map.of(
	        "success", success
	    );
	}
	
	
	
	// [D] 게시글 수정 (수정완료 버튼 클릭시)(PostMapping())
	@PostMapping("/freeboard/{boardNo}/update")  
	@ResponseBody
	public  Map<String, Object> boardUpdate(
			@PathVariable("boardNo") Long boardNo,
			Freeboard freeboard, 
			@RequestParam(value="cp", required=false, defaultValue="1") String cp, 
			@RequestParam(value="deleteList", required=false) String deleteList, 
			@RequestParam(value="images", required=false) List<MultipartFile> images, 
			@RequestParam(value="existingImgNos", required=false) String existingImgNos, 
			RedirectAttributes ra, 
			HttpSession session 
			) throws IllegalStateException, IOException {

		log.info("[ FreeboardController: Update-POST ] cp for 목록으로 버튼 선택시 :{}", cp);
		log.info("[ FreeboardController: Update-POST ] deleteList in freeboardUpdate-POST:{}", deleteList); 		
		//log.info("[ FreeboardController: Update-POST ] images.size() in freeboardUpdate-POST:{}", images.size()); 		
		if (images != null && images.size() > 0) {	// null-방어
			log.info("[ FreeboardController: Update-POST ] images.size() in freeboardUpdate-POST:{} for new images attached", images.size()); 					
		} else {
			log.info("[ FreeboardController: Update-POST ] images.size() in freeboardUpdate-POST == 0; no-new image attached"); 								
		}		
		log.info("[ FreeboardController: Update-POST ] existingImgNos in freeboardUpdate-POST:{}", existingImgNos); 		
			
		
		// 1. boardNo를 커맨드 객체에 세팅
		freeboard.setBoardNo(boardNo);
		
		// 2. 게시글 수정 서비스 호출 (제목/내용수정:BOARD + 이미지수정:BOARD_IMG)
		int rowCount = service.freeboardUpdate(freeboard, images, existingImgNos);
		
		// 3. 결과에 따라 message, path 설정
		String message = null;
		String redirectUrl = null;
		Map<String, Object> result = new HashMap<>();
		
		if(rowCount > 0) { // 게시글 수정 성공 시
			message = "게시글이 수정되었습니다";
			redirectUrl = "/board/freeboard/" + boardNo + "?cp=" + cp; //  boardCode, boardNo -> 
			
	        result.put("success", true);
	        result.put("message", message);
	        result.put("redirectUrl", redirectUrl);					
			
		} else { // 실패 시
			message = "게시글 수정 실패. 잠시후 다시 시도해 주세요.";
			redirectUrl = "/board2/freeboard/" + boardNo + "/update"+ "?cp=" + cp; 
			
	        result.put("success", false);
	        result.put("message", message);
	        result.put("redirectUrl", redirectUrl);					
		}
		
		ra.addFlashAttribute("message", message);
		
		return result;
	}

	// [E] 게시글 삭제 (GetMapping())
	@GetMapping("/freeboard/{boardNo}/delete") 
	public String boardDelete(
			@PathVariable("boardNo") Long boardNo 
			, @RequestParam(value="cp", required=false, defaultValue="1") String cp
			, RedirectAttributes ra 
			, @RequestHeader("referer") String referer // 이전 요청 주소
			) {
		
		log.info("[ FreeboardController: Delete-GET ] cp :{}", cp);
		log.info("[ FreeboardController: Delete-GET ] boardNo :{}", boardNo); 		
		log.info("[ FreeboardController: Delete-GET ] referer, 이전 요청 주소 :{}", referer); 		
			
		// 1. 게시글 삭제 서비스 호출
		int result = service.freeboardDelete(boardNo);
		
		// 2. 결과에 따라 message, path 설정
		String message = null;
		String path = "redirect:";
		
		if (result > 0) {
			
			message = "게시글이 삭제되었습니다.";
			path += "/board/" + "freeboard";
		} else {
			message = "게시글 삭제 실패. 잠시 후 다시 시도해 주세요.";
			path += referer; // 마찬가지
				
		}
		
		ra.addFlashAttribute("message", message);
		
		return path;
		
	}
	
	// [F] 게시글 삭제 (PostMapping())
	// /board2/freeboard/20/update/deletePOST
	@PostMapping("/freeboard/{boardNo}/update/deletePOST") // "/board2/freeboard/15" + "/deletePOST"
	@ResponseBody
	public Map<String, Object> deletePOST(@RequestBody Map<String, Object> data) {
	    // data.get("oldBoardNo")
		//Long oldBoardNo = (Long) data.get("oldBoardNo");
		//Long oldBoardNo = (Long) data.get("oldBoardNo");
		Long oldBoardNo =  ((Number) data.get("oldBoardNo")).longValue(); 
		//Long oldBoardNo = Long.valueOf( data.get("oldBoardNo"));
		// data.get("insertedBoardNo")
		//Long insertedBoardNo = (Long) data.get("insertedBoardNo");
		Long insertedBoardNo = ((Number) data.get("insertedBoardNo")).longValue(); 
	    // data.get("existingImgNos")
		
		log.info("받은 데이터 : {}", data );
		
		// 1. 게시글 삭제 서비스 호출 (해당 게시글 boardDelFl을 'Y'로 세팅)
		int res = service.setBoardNoDelFl(oldBoardNo);
		
		log.info("처리결과 res : {}", data );
		// 2. data.get("existingImgNos"): oldBoardNo 게시글의 이미지 작업은 future work

		
		// 3. 결과에 따라 message, path 설정
		String message = null;
		String redirectUrl = null;
		Map<String, Object> result = new HashMap<>();		
		if(res > 0) { // 게시글 삭제 성공 시
			message = "게시글이 삭제되었습니다";
			redirectUrl = "/board/freeboard/" + insertedBoardNo;  
			
	        result.put("success", true);
	        result.put("message", message);
	        result.put("redirectUrl", redirectUrl);					
			
		} else { // 실패 시
			message = "게시글 수정 실패. 잠시후 다시 시도해 주세요.";
			redirectUrl = "/board2/freeboard/" + oldBoardNo + "/update"; 
			
	        result.put("success", false);
	        result.put("message", message);
	        result.put("redirectUrl", redirectUrl);					
		}		
		
		return result;
	}
	
}



package com.devlog.project.board.freeboard.model.service;

import java.io.IOException;
import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import com.devlog.project.board.freeboard.model.dto.Freeboard;

public interface FreeboardService2 {


	/** 게시글 삽입
	 * @param freeboard
	 * @param images
	 * @return boardNo // insert하는 보드넘버
	 * @throws IllegalStateException
	 * @throws IOException
	 */
	Long freeboardInsert(Freeboard freeboard, List<MultipartFile> images) throws IllegalStateException, IOException;

	
	
	/** 게시글 수정에서 이미지삭제/추가에서 기존이미지 한개 삭제, AJAX
	 * @param imgNo
	 * @return 성공여부
	 */
	boolean deleteFreeboardImage(Long imgNo);


	/** 게시글 수정 
	 * @param freeboard
	 * @param images
	 * @param deleteList
	 * @return 성공한 행의 갯수
	 */
	int freeboardUpdate(Freeboard freeboard, List<MultipartFile> images, String existingImgNos) throws IllegalStateException, IOException;



	/** 게시글 삭제
	 * @param boardNo
	 * @return 성공한 행의 갯수
	 */
	int freeboardDelete(Long boardNo); 
	
	
	/** 게시글 삭제, monkey-patch
	 * @param boardNo
	 * @return 성공한 행의 갯수
	 */
	int setBoardNoDelFl(Long boardNo); 	
	
}


package com.devlog.project.board.freeboard.model.service;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import com.devlog.project.board.freeboard.model.dto.BoardImgDB;
import com.devlog.project.board.freeboard.model.dto.Freeboard;
import com.devlog.project.board.freeboard.model.mapper.FreeboardMapper;
import com.devlog.project.board.freeboard.model.mapper.FreeboardMapper2;
import com.devlog.project.common.exception.FileUploadException;
import com.devlog.project.common.exception.ImageDeleteException;
import com.devlog.project.common.utility.Util;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@PropertySource("classpath:/config.properties")
@RequiredArgsConstructor
public class FreeboardServiceImpl2 implements FreeboardService2 {

	@Value("${my.freeboard.webpath}") 
	private String webPath;
	
	@Value("${my.freeboard.location}")  
	private String filePath;
	
	private final FreeboardMapper mapperService; 
	
	private final FreeboardMapper2 mapper; 
	
	// 게시글 삽입
	@Transactional(rollbackFor = Exception.class)
	@Override
	public Long freeboardInsert(Freeboard freeboard, List<MultipartFile> images) throws IllegalStateException, IOException{
		
		// 0. XSS 방지 처리: <script> 집어넣을 경우 무력화 

		// 제목만 XSS 방지처리:
		freeboard.setBoardTitle(Util.XSSHandling(freeboard.getBoardTitle() ) ); // title 변환시킨후 DB에 저장 ==> 타이틀을 읽어야하는 태그가 BoardDetail.html에 있기 때문
		//freeboard.setBoardContent(Util.XSSHandling(freeboard.getBoardContent() ) ); // content 변환 시킨후 DB에 저장
		
		// 1.  따로 따로 insert
		// -> boardNo (시퀀스로 생성한 번호) 반환 받기
		Long boardNo = mapper.freeboardInsert(freeboard); 
		
		// 실패시 서비스 종료 (밑에 코드 수행할 필요 없다
		if (boardNo == 0) return Long.valueOf(0);
		
		// mapper.xml에서 selectKey 태그로 인해 boardNo에 세팅된 값
		boardNo = freeboard.getBoardNo();
		log.info("[ FreeboardServiceImpl ] Insertion boardNo: {}", boardNo); 	
		
		// 2. 게시글 삽입 성공 시
		if (boardNo != 0) {
			// 실제로 업로드된 파일의 정보를 기록할 List
			List<BoardImgDB> uploadList = new ArrayList<BoardImgDB>();
			
			if (images != null && images.size() > 0) {	// null-방어
				log.info("[ FreeboardServiceImpl ] images.size() =  {}", images.size()); 
				
				for(int i=0; i<images.size(); i++) { // 이미지 파일 있으나 없으나, images.size()=5가 기본 ==> devlog는 추가한 것만큼만 js에서 동적으로 만듦 (즉, 모두 images.get(i).getSize() > 0)
					log.info("[ FreeboardServiceImpl ] images.get({}).getSize() =  {}", i, images.get(i).getSize()); 
					// i번째 요소에 업로드한 파일이 있다면
					if (images.get(i).getSize() > 0) { // 업로드한 이미지 있다.
						// img에 파일 정보를 담아서 uploadList에 추가
						BoardImgDB img = new BoardImgDB();
						
						img.setImgPath(webPath); // 웹 접근 경로
						
						// 파일 원본명
						String fileName = images.get(i).getOriginalFilename(); // 파일 원본명 from 리스트
						log.info("[ FreeboardServiceImpl ] 원본 파일명 fileName =  {}", fileName); 
						
						// 파일 변경명 img에 세팅
						img.setImgRename(Util.fileRename(fileName));
						
						// 파일 원본명 img에 세팅
						img.setImgOrig(fileName);
						
						// 다른 필요한 값들 img에 세팅
						img.setImgOrder(i); 	 // 이미지 순서
						img.setBoardNo(boardNo); // 게시글 번호
						
						uploadList.add(img);
						
					}
					
				} // 분류 for문 종료 
				log.info("[ FreeboardServiceImpl ] uploadList.size() =  {}", uploadList.size()); 
				
				// 분류 작업 후 uploadList가 비어있지 않은 경우
				// == 업로드한 파일이 존재
				if(!uploadList.isEmpty()) {
					
					// BOARD_IMG 테이블에 insert 하기
					int result = mapper.insertImageList(uploadList); // 이것까지 성공해야 commit by @Transactional()
					// result == 성공한 행의 개수
					//
					// 삽입된 행의 갯수(result)와 uploadList의 개수(uploadList.size())가 같다면
					// == 전체 insert 성공
					if (result == uploadList.size()) { // 전체 성공 or 부분 성공/전체 실패
						
						for (int i=0; i<uploadList.size(); i++) {
							// 이미지 순서
							int index = uploadList.get(i).getImgOrder(); //
							
							// 변경명
							String rename = uploadList.get(i).getImgRename();
							images.get(index).transferTo(new File(filePath + rename));  // index에 해당하는 images[index]만 서버로 옮겨준다(서버에 저장한다)
							
							
						}
						
						
						
					} else { // 일부 또는 전체 insert 실패
						// * 웹 서비스 수행 중 1개라도 실패하면 전체 실패 *
						// -> rollback 필요 (but, @Transactional rollback은 exception이 발생해야만 rollback진행
						// @Transactional (rollbackFor = Exception.class)
						// -> 예외가 발생해야만 롤백한다.
						// -> 사용자 정의 예외 (강제)생성 by "throw"
						throw new FileUploadException(); // 강제 예외 발생 시키는 구문 -> 이제 @Transactional에서 rollback한다.
						
					}
					
				}
			}//
		}

		//return 0;
		return boardNo;
	}

	// 게시글의 이미지 삭제: 게시글 수정에서 이미지삭제/추가에서 기존이미지 한개 삭제 (Ajax)
	@Override
	@Transactional(rollbackFor = Exception.class)
	public boolean deleteFreeboardImage(Long imgNo) {
	    BoardImgDB img = mapperService.selectImageByImgNo(imgNo); // 먼저 삭제할 이미지가 데이터베이스에 존재하는지 확인
	    if (img == null) return false;

	    // DB 삭제
	    int result = 0;
	    try {
	    	result = mapper.deleteImageByImgNo(imgNo); // 데이터베이스에 존재 확인된 이미지 삭제
	    } catch (Exception e) {
	    	log.info("error duging image deletion:{}", e);
	    	throw new ImageDeleteException(e.getMessage()); 
	    }

	    // 파일 삭제
	    if (result > 0) {
	        Path path = Paths.get(
	            img.getImgPath(),
	            img.getImgRename()
	        );

	        try {
	            Files.deleteIfExists(path);
	        } catch (IOException e) {
	            throw new RuntimeException(e);
	        }
	    }

	    return result > 0;
	}

	
	
	// 게시글 수정: 게시글과 게시글 이미지의 업데이트 둘다 성공해야 commit
	@Transactional(rollbackFor = Exception.class)
	@Override	
	public int freeboardUpdate(Freeboard freeboard, List<MultipartFile> images, String existingImgNos)
			throws IllegalStateException, IOException {
		// 0. XSS 방지 처리: <script> 집어넣을 경우 무력화 (게시글 작성때와 마찬가지)
		freeboard.setBoardTitle(Util.XSSHandling(freeboard.getBoardTitle() ) ); // title 변환시킨후 DB에 저장
		//freeboard.setBoardContent(Util.XSSHandling(freeboard.getBoardContent() ) ); // content 변환 시킨후 DB에 저장
		
		// 1. 게시글 제목/내용만 수정
		int rowCount = mapper.freeboardUpdate(freeboard);
		
		
		// 2. 게시글 수정 성공시
        if (rowCount > 0) {
            
            // 2. 기존 이미지 처리
            List<Long> keepImgNos = new ArrayList<>();
            
            if (existingImgNos != null && !existingImgNos.isEmpty()) { //null-방어
                // JSON 파싱: "[88,89,90]" -> List<Long>
                keepImgNos = parseExistingImgNos(existingImgNos);
                
                log.info("[ FreeboardServiceImpl:수정CC ]유지할 기존 이미지 번호들: {}", keepImgNos);
                
                // 2-1. 이 게시글의 기존 이미지 중 keepImgNos에 없는 것들 삭제
                if (!keepImgNos.isEmpty()) {
                    mapper.deleteImagesNotInList(freeboard.getBoardNo(), keepImgNos);
                }
                
                // 2-2. 유지할 기존 이미지들의 순서(IMG_ORDER) 업데이트
                for (int i = 0; i < keepImgNos.size(); i++) {
                    Map<String, Object> orderMap = new HashMap<>();
                    orderMap.put("imgNo", keepImgNos.get(i));
                    orderMap.put("imgOrder", i);
                    mapper.updateImageOrder(orderMap);
                }
            } else {
                // existingImgNos가 null이거나 빈 문자열이면 모든 기존 이미지 삭제
                mapper.deleteAllImagesByBoardNo(freeboard.getBoardNo());
            }
            
            // 3. 새 이미지 추가
            if (images != null && !images.isEmpty()) { // null-방어
                
                // 새 이미지의 시작 순서 = 기존 이미지 개수
                int startOrder = keepImgNos.size();
                
                // 실제로 업로드된 파일만 저장할 리스트
                List<BoardImgDB> uploadList = new ArrayList<>();
                
                for (int i = 0; i < images.size(); i++) {
                    MultipartFile image = images.get(i);
                    
                    // 실제로 업로드된 파일인 경우
                    if (image.getSize() > 0) {
                        
                        // 파일명 생성
                        String originalFilename = image.getOriginalFilename();
                        String rename = Util.fileRename(originalFilename);
                        
                        // BoardImgDB 객체 생성
                        BoardImgDB img = new BoardImgDB();
                        img.setImgPath(webPath);
                        img.setImgRename(rename);
                        img.setImgOrig(originalFilename);
                        img.setImgOrder(startOrder + i);
                        img.setBoardNo(freeboard.getBoardNo());
                        
                        uploadList.add(img);
                        
                        // DB에 이미지 정보 삽입
                        rowCount = mapper.imageInsert(img);
                        
                        if (rowCount == 0) {
                            throw new RuntimeException("이미지 삽입 실패");
                        }
                    }
                }
                
                // 4. 서버에 실제 파일 저장
                if (!uploadList.isEmpty()) {
                    for (int i = 0; i < uploadList.size(); i++) {
                        int index = uploadList.get(i).getImgOrder() - startOrder;
                        String rename = uploadList.get(i).getImgRename();
                        
                        // 실제 파일 저장
                        images.get(index).transferTo(new File(filePath + rename));
                    }
                }
            }
        }
        
        return rowCount;
	}	
	
	
    /**
     * JSON 문자열을 Long 리스트로 파싱
     * @param existingImgNos "[88,89,90]" 형태의 JSON 문자열
     * @return List<Long>
     */
    private List<Long> parseExistingImgNos(String existingImgNos) {
        List<Long> result = new ArrayList<>();
        
        try {
            // JSON 파싱
            ObjectMapper mapper = new ObjectMapper();
            result = mapper.readValue(existingImgNos, new TypeReference<List<Long>>(){});
        } catch (Exception e) {
            log.error("existingImgNos 파싱 실패: {}", existingImgNos, e);
        }
        
        return result;
    }	
	
	// 게시글 삭제
	@Override
	public int freeboardDelete(Long boardNo) {
		// 
		return mapper.freeboardDelete(boardNo);
	}

	@Override
	public int setBoardNoDelFl(Long boardNo) {
		return mapper.freeboardDelete(boardNo);
	}   
    
}



package com.devlog.project.board.freeboard.controller;


import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.devlog.project.board.freeboard.model.dto.CommentFB;
import com.devlog.project.board.freeboard.model.service.FbCommentService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController 
@RequiredArgsConstructor
public class FbCommentController { 

	private final FbCommentService service;
	
	// 댓글 목록 조회
	@GetMapping(value = "/board/freeboard/comment", produces="application/json; charset=UTF-8") 
	public List<CommentFB> select(Long boardNo ) { 
		return service.select(boardNo); 
	}
	
	
	// 댓글 삽입(INSERT) 
	@PostMapping("/board/freeboard/comment")
	public Long insert(@RequestBody CommentFB comment) { 
		return service.insert(comment);
	}
	
	
	// 댓글 삭제 (DELETE, but 내부적으로는 UPDATE)
	@DeleteMapping("/board/freeboard/comment")
	public int delete(@RequestBody CommentFB comment) {
		return service.delete(comment);
	}
	
	// 댓글 수정 (UPDATE)
	@PutMapping("/board/freeboard/comment")
	public int update(@RequestBody CommentFB comment) {
		return service.update(comment);
	}
	
}


package com.devlog.project.board.freeboard.model.service;


import com.devlog.project.board.freeboard.model.dto.CommentFB;

import java.util.List;

public interface FbCommentService {

	/** 댓글 목록 조회
	 * @param boardNo
	 * @return List<CommentDB>
	 */
	List<CommentFB> select(Long boardNo);

	
	/** 댓글 삽입
	 * @param comment
	 * @return result :성공한 경우 commentNo
	 */
	Long insert(CommentFB comment);


	/** 댓글 삭제
	 * @return result: 성공한 행의 갯수
	 */
	int delete(CommentFB comment);


	/** 댓글 수정
	 * @param comment
	 * @return result: 성공한 행의 갯수
	 */
	int update(CommentFB comment); 
}


package com.devlog.project.board.freeboard.model.service;

import java.util.List;
import org.springframework.stereotype.Service;

import com.devlog.project.board.freeboard.model.dto.CommentFB;
import com.devlog.project.board.freeboard.model.mapper.FbCommentMapper;
import com.devlog.project.common.utility.Util;
import com.devlog.project.notification.NotiEnums;
import com.devlog.project.notification.dto.NotifiactionDTO;
import com.devlog.project.notification.service.NotificationService;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class FbCommentServiceImpl implements FbCommentService {

	private final FbCommentMapper mapper; 
	
	private final NotificationService notiService;
	
	// 댓글 목록 조회
	@Override
	public List<CommentFB> select(Long boardNo) {
		return mapper.select(boardNo);
	}


	// 댓글 삽입
	@Override
	public Long insert(CommentFB comment) {
		// XSS 방지 처리
		comment.setCommentContent(Util.XSSHandling(comment.getCommentContent()));
		// 
		Long result = mapper.insert(comment);
				
		// 댓글 삽입 성공 시 댓글 번호 반환
		if(result > 0) result = comment.getCommentNo();
		
		 // 댓글 알림 생성 
	    if(result > 0 ) {
	    	
	    	int boardMemberNo = mapper.getBoardMemberNo(comment.getBoardNo());
	    	
	    	
	    	if(boardMemberNo != comment.getMemberNo()) {
	    		
	    		String memberNickname = mapper.selectMemberNickname(comment.getMemberNo());
	    		
	    		NotifiactionDTO notification = NotifiactionDTO.builder()
						.sender((long) comment.getMemberNo())
						.receiver((long) boardMemberNo)
						.content(memberNickname +"님이 회원님의 게시글에 댓글을 남겼습니다.")
						.preview(comment.getCommentContent())
						.type(NotiEnums.NotiType.COMMENT)
						.targetType(NotiEnums.TargetType.BOARD)
						.targetId(comment.getCommentNo())
						.build();
	    		
	    		notiService.sendNotification(notification);
	    		
	    		
	    	}
	    }
		
		
		return result;
	}


	// 댓글 삭제
	@Override
	public int delete(CommentFB comment) {
		// 
		return mapper.delete(comment);
	}


	// 댓글 수정
	@Override
	public int update(CommentFB comment) {
		// XSS 방지 처리
		comment.setCommentContent(Util.XSSHandling(comment.getCommentContent()));
		
		return mapper.update(comment);
	}

}


package com.devlog.project.board.freeboard.model.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class BoardTypeDB {
    // 게시판코드 
    private Integer boardCode;

    // 게시판이름 
    private String boardName;

    // 부모 게시판 코드 
    private Integer parentsBoardCode;
}


package com.devlog.project.board.freeboard.model.dto;


import java.util.ArrayList;
import java.util.List; 

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class Freeboard {
	private Long boardNo;
	private String boardTitle;
	private String boardContent;
	private String bCreateDate; // LocalDateTime?
	private String bUpdateDate; // LocalDateTime?
	private int boardCount; // 조회수, readCount
	private String boardDelFl;
	private int boardCode; // 3:자유게시판
	
	
	// 서브쿼리 (상세 페이지용 추가 필드)
	private int likeCount;         // 좋아요 개수
	private int commentCount;      // 댓글 개수	
	
	
	// 회원 join
	private Long memberNo;
	private String memberNickname; 
	private String profileImg;
	private String thumbnail;
	
	// 이미지 목록
	private List<BoardImgDB> imageList;

	// 댓글 목록
	private List<CommentDB> commentList;
	
	// null 방어, 2026/01/09
	public void setImageList(List<BoardImgDB> imageList) {
	    this.imageList = (imageList == null)
	        ? new ArrayList <>()
	        : imageList;
	}	
	
	//
	public void setCommnetList(List<CommentDB> commentList) {
	    this.commentList = (commentList == null)
	        ? new ArrayList <>()
	        : commentList;
	}		
}


package com.devlog.project.board.freeboard.model.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class BoardImgDB {
	
    private Long imgNo;
    private String imgPath;
    private String imgOrig;
    private String imgRename;
    private int imgOrder;
    private Long boardNo;
}


package com.devlog.project.board.freeboard.model.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class BoardLikeDB {

    private Long boardNo;
    private Long memberNo;
}


package com.devlog.project.board.freeboard.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class CommentFB {

	@JsonProperty("commentNo") 
	private Long commentNo;
	
	@JsonProperty("memberNo")
	private Long memberNo;
	
	@JsonProperty("boardNo")
	private Long boardNo;
	
	@JsonProperty("parentsCommentNo")
	private Long parentsCommentNo;
	
	@JsonProperty("cCreateDate")
	private String cCreateDate;
	
	@JsonProperty("commentContent")
	private String commentContent;
	
	@JsonProperty("commentDelFl")
	private String commentDelFl;
	
	@JsonProperty("secretYn")
	private String secretYn;
	
	@JsonProperty("modifyYn")
	private String modifyYn;
	
	@JsonProperty("memberNickname")
	private String memberNickname;
	
	@JsonProperty("profileImg")
	private String profileImg;
}


package com.devlog.project.board.freeboard.model.dto;

/*
프론트(JSP/Thymeleaf)에서 사용하는 값들(PaginationFB 으로 인해 바로 사용 가능)
pagination.currentPage
pagination.startPage
pagination.endPage
pagination.prevPage
pagination.nextPage
pagination.maxPage
 */

public class PaginationFB { //
	// 페이지네이션(페이징 처리)에 필요한 모든 값을 저장하고 있는 객체

	// fields
	private int currentPage;      // 현재 페이지 
	private int listCount;         // 전체 게시글 수 

	private int limit = 7;         // 한 페이지에 보여질 게시글 수, "고정"
	private int pageSize = 10;       // 목록 하단 페이지 번호의 노출 개수 

	
	private int maxPage;         // 제일 큰 페이지 번호 == 마지막 페이지 번호
	private int startPage;         // 목록 하단에 노출된 페이지의 시작 번호
	private int endPage;         // 목록 하단에 노출된 페이지의 끝 번호

	private int prevPage;         // 목록 하단에 노출된 번호의 이전 목록 끝 번호
	private int nextPage;         // 목록 하단에 노출된 번호의 다음 목록 시작 번호
	
	// 생성자
	public PaginationFB(int currentPage, int listCount) {
		this.currentPage = currentPage; // 현재 페이지
		this.listCount = listCount; // 전체 게시글 수
		
		calculatePagination(); // 계산 메소드 호출
	}

	public int getCurrentPage() {
		return currentPage;
	}

	public void setCurrentPage(int currentPage) {
		this.currentPage = currentPage;
		calculatePagination(); // 계산 메소드 호출 
	}

	public int getListCount() {
		return listCount;
	}

	public void setListCount(int listCount) {
		this.listCount = listCount;
		calculatePagination(); // 계산 메소드 호출
	}

	public int getLimit() {
		return limit;
	}

	public void setLimit(int limit) {
		this.limit = limit;
		calculatePagination(); // 계산 메소드 호출
	}

	public int getPageSize() {
		return pageSize;
	}

	public void setPageSize(int pageSize) {
		this.pageSize = pageSize;
		calculatePagination(); // 계산 메소드 호출
	}

	public int getMaxPage() {
		return maxPage;
	}

	public void setMaxPage(int maxPage) {
		this.maxPage = maxPage;
	}

	public int getStartPage() {
		return startPage;
	}

	public void setStartPage(int startPage) {
		this.startPage = startPage;
	}

	public int getEndPage() {
		return endPage;
	}

	public void setEndPage(int endPage) {
		this.endPage = endPage;
	}

	public int getPrevPage() {
		return prevPage;
	}

	public void setPrevPage(int prevPage) {
		this.prevPage = prevPage;
	}

	public int getNextPage() {
		return nextPage;
	}

	public void setNextPage(int nextPage) {
		this.nextPage = nextPage;
	}

	@Override
	public String toString() {
		return "Pagination [currentPage=" + currentPage + ", listCount=" + listCount + ", limit=" + limit
				+ ", pageSize=" + pageSize + ", maxPage=" + maxPage + ", startPage=" + startPage + ", endPage="
				+ endPage + ", prevPage=" + prevPage + ", nextPage=" + nextPage + "]";
	}

	// 페이징 처리에 필요한 값을 계산하는 메소드 (클래스 내부에서만 사용하는 메소드)
	private void calculatePagination() {
		maxPage = (int)Math.ceil( (double)listCount / limit); //(int)Math.ceil( (double)int / int)
		
		// * startPage : 목록 하단에 노출된 페이지의 시작 번호
		startPage = (currentPage - 1)/pageSize * pageSize + 1; 
		
		// * endPage : 목록 하단에 노출된 페이지의 끝 번호
		endPage = startPage + pageSize - 1;
		
		// 만약 endPage가 maxPage를 초과하는 경우
		if (endPage > maxPage) endPage =  maxPage;
		
		
		// ------------------------------------------------------
		//
		// * prevPage(<) : 목록하단에 노출된 번호의 이전 목록 끝번호
		// * nextPage(>) : 목록하단에 노출된 번호의 다음 목록 시작 번호
		
		// 현재 페이지가 1 ~ 10 인 경우 (case1)
		// < : 1 페이지
		// > : 11 페이지
		
		// 현재 페이지가 11 ~ 20 인 경우(case2)
		// < : 10 페이지
		// > : 21 페이지
		
		// 현재 페이지가 41 ~ 50 인 경우 (maxPage가 50) (case3)
		// < : 40 페이지
		// > : 50 페이지
		
		if(currentPage <= pageSize) prevPage = 1; // case1
		else prevPage = startPage - 1; // case2 & case3
		
		if(maxPage == endPage) { // case3
			nextPage = maxPage;
		} else {
			nextPage = endPage + 1; // case1&case2
		}
		
	}
}



