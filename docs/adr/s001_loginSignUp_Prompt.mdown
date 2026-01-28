 [ pyy prompt: java spring boot 웹앱을 python FastAPI 앱으로 porting하기 ]

 java version 17 기반 Spring Boot 웹앱을 만들었는데 환경은 spring boot 3.5.7 + sts4 IDE + gradle + jpa-hibernate(회원가입/로그인/카카오 소셜로그인) + myBatis(자유게시판) + oracle database + elasticsearch(docker로 elasticsearch + kibana + logstash) + spring-security 이야. 여러 구성부분이 있는데 내가 담당했던 회원가입, 로그인, 카카오 소셜로그인, 자유게시판(게시글 CRUD + 댓글 CRUD + 좋아요 + 조회수 기능), 그리고 게시글 삽입/수정에서 사용하도록 제작된  spring ai + openAI API 기반 챗봇 기능을 python version 3.10 기반 FastAPI + Oracle + Elasticsearch + Docker Compose 로 완전 동작 가능한 Dockerfile & docker-compose.yml 풀셋으로 porting하고 싶어.
 (FastAPI 백엔드: 인증/인가 (JWT) + 회원관리 (Oracle) + 게시판 CRUD (Oracle) + 검색 API (Elasticsearch) + ORM(SQLAlchemy))

 단계적/순차적으로 옮겨오고 싶은데, 우선 회원가입, 로그인 기능을 FastAPI 기반으로 옮겨왔으면 좋겠어서, 아래 1, 2, 3번으로 이와 관련한 요청내용과 관련화일을 구성해 보았어.

 1. 로그인/회원가입에 필요한 오라클 DB의 해당 테이블은 다음과 같이 ERD에서 정의하고 MEMBER, LEVELS 테이블을 생성하고, 또 그에 맞는 jpa entity들 (Member, Auth)를 아래처럼 생성했는데, 이걸 FastAPI백엔드에 맞게 바꿔줘.

 CREATE TABLE "LEVELS" (
   "LEVEL_NO"   NUMBER      NOT NULL,
   "REQUIRED_TOTAL_EXP"   NUMBER      NOT NULL,
   "TITLE"   VARCHAR2(100)      NOT NULL
);
COMMENT ON COLUMN "LEVELS"."LEVEL_NO" IS 'LV1 ~ LV30 (SEQ_LEVEL_NO)';
COMMENT ON COLUMN "LEVELS"."REQUIRED_TOTAL_EXP" IS '레벨별 필요 누적 경험치';
COMMENT ON COLUMN "LEVELS"."TITLE" IS '레벨별 타이틀';
ALTER TABLE "LEVELS" ADD CONSTRAINT "PK_LEVELS" PRIMARY KEY (
   "LEVEL_NO"
);
ALTER TABLE "MEMBER" ADD CONSTRAINT "FK_LEVELS_TO_MEMBER_1" FOREIGN KEY (
   "MEMBER_LEVEL"
)
REFERENCES "LEVELS" (
   "LEVEL_NO"
);


CREATE TABLE "MEMBER" (
   "MEMBER_NO"   NUMBER      NOT NULL,
   "MEMBER_EMAIL"   VARCHAR2(30)      NOT NULL,
   "MEMBER_PW"   VARCHAR2(200)      NULL,
   "MEMBER_NAME"   VARCHAR2(30)      NOT NULL,
   "MEMBER_NICKNAME"   VARCHAR2(30)      NOT NULL,
   "MEMBER_TEL"   VARCHAR2(13)      NOT NULL,
   "MEMBER_CAREER"   VARCHAR2(50)      NOT NULL,
   "MEMBER_SUBSCRIBE"   CHAR(1)   DEFAULT 'N'   NOT NULL,
   "MEMBER_ADMIN"   CHAR(1)   DEFAULT 'N'   NOT NULL,
   "PROFILE_IMG"   VARCHAR2(300)      NULL,
   "MEMBER_DEL_FL"   CHAR(1)   DEFAULT 'N'   NOT NULL,
   "M_CREATE_DATE"   DATE   DEFAULT SYSDATE   NULL,
   "SUBSCRIPTION_PRICE"   NUMBER   DEFAULT 0   NOT NULL,
   "MY_INFO_INTRO"   VARCHAR2(2000)      NULL,
   "MY_INFO_GIT"   VARCHAR2(200)      NULL,
   "MY_INFO_HOMEPAGE"   VARCHAR2(200)      NULL,
   "BEANS_AMOUNT"   NUMBER   DEFAULT 0   NOT NULL,
   "CURRENT_EXP"   NUMBER   DEFAULT 0   NOT NULL,
   "MEMBER_LEVEL"   NUMBER      NOT NULL
);
COMMENT ON COLUMN "MEMBER"."MEMBER_NO" IS '회원번호(SEQ_MEMBER_NO)';
COMMENT ON COLUMN "MEMBER"."MEMBER_EMAIL" IS '회원이메일(아이디)';
COMMENT ON COLUMN "MEMBER"."MEMBER_PW" IS '회원비밀번호';
COMMENT ON COLUMN "MEMBER"."MEMBER_NAME" IS '회원이름';
COMMENT ON COLUMN "MEMBER"."MEMBER_NICKNAME" IS '회원닉네임';
COMMENT ON COLUMN "MEMBER"."MEMBER_TEL" IS '회원전화번호';
COMMENT ON COLUMN "MEMBER"."MEMBER_CAREER" IS '회원경력사항';
COMMENT ON COLUMN "MEMBER"."MEMBER_SUBSCRIBE" IS '회원전용메일수신동의';
COMMENT ON COLUMN "MEMBER"."MEMBER_ADMIN" IS '관리자계정여부(Y:관리자, N:일반회원)';
COMMENT ON COLUMN "MEMBER"."PROFILE_IMG" IS '프로필 이미지';
COMMENT ON COLUMN "MEMBER"."MEMBER_DEL_FL" IS '회원탈퇴여부';
COMMENT ON COLUMN "MEMBER"."M_CREATE_DATE" IS '회원가입일';
COMMENT ON COLUMN "MEMBER"."SUBSCRIPTION_PRICE" IS '나를구독하면 지불해야할금액: 초기값0원';
COMMENT ON COLUMN "MEMBER"."MY_INFO_INTRO" IS '내 소개글';
COMMENT ON COLUMN "MEMBER"."MY_INFO_GIT" IS '깃허브 주소';
COMMENT ON COLUMN "MEMBER"."MY_INFO_HOMEPAGE" IS '노션, 포트폴리오 등 주소';
COMMENT ON COLUMN "MEMBER"."BEANS_AMOUNT" IS '커피콩지갑';
COMMENT ON COLUMN "MEMBER"."CURRENT_EXP" IS '회원 현재 경험치';
COMMENT ON COLUMN "MEMBER"."MEMBER_LEVEL" IS 'LV1 ~ LV30';
ALTER TABLE "MEMBER" ADD CONSTRAINT "PK_MEMBER" PRIMARY KEY (
   "MEMBER_NO"
);
ALTER TABLE "MEMBER" ADD CONSTRAINT "FK_LEVELS_TO_MEMBER_1" FOREIGN KEY (
   "MEMBER_LEVEL"
)
REFERENCES "LEVELS" (
   "LEVEL_NO"
);


CREATE TABLE "AUTH" (
   "AUTH_NO"   NUMBER      NOT NULL,
   "CODE"   VARCHAR2(100)      NOT NULL,
   "EMAIL"   VARCHAR2(100)      NOT NULL,
   "CREATE_AT"   DATE   DEFAULT SYSDATE   NOT NULL
);
COMMENT ON COLUMN "AUTH"."AUTH_NO" IS '시퀀스번호';
COMMENT ON COLUMN "AUTH"."CODE" IS '인증키 코드';
COMMENT ON COLUMN "AUTH"."EMAIL" IS '이메일';
COMMENT ON COLUMN "AUTH"."CREATE_AT" IS '생성시간';
ALTER TABLE "AUTH" ADD CONSTRAINT "PK_AUTH" PRIMARY KEY (
   "AUTH_NO"
);




package com.devlog.project.member.model.entity;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "LEVELS")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
@Setter
public class Level {

    @Id
    @Column(name = "LEVEL_NO")
    private Integer levelNo;

    @Column(name = "REQUIRED_TOTAL_EXP", nullable = false)
    private Integer requiredTotalExp;

    @Column(name = "TITLE", nullable = false, length = 100)
    private String title;
}



package com.devlog.project.member.model.entity;


import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.hibernate.annotations.DynamicInsert;
import org.hibernate.annotations.DynamicUpdate;

import com.devlog.project.member.enums.CommonEnums;
import com.devlog.project.member.enums.CommonEnums.Status;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.PrePersist;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "MEMBER")
@Getter
@Setter
@ToString(exclude = {"memberLevel"})  // Level 필드 제외,  연관관계 모두 제외
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor // 시제 객체생성에 필요
public class Member {

	// PK
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "SEQ_MEMBER")
    @SequenceGenerator(
            name = "SEQ_MEMBER",
            sequenceName = "SEQ_MEMBER_NO",
            allocationSize = 1
    )
    @Column(name = "MEMBER_NO")
    private Long memberNo;

    // 로그인 정보
    @Column(name = "MEMBER_EMAIL", nullable = false, length = 30, unique = true)
    private String memberEmail;

    @Column(name = "MEMBER_PW", length = 200)
    private String memberPw;

    // 기본 정보
    @Column(name = "MEMBER_NAME", nullable = false, length = 30)
    private String memberName;

    @Column(name = "MEMBER_NICKNAME", nullable = false, length = 30)
    private String memberNickname;

    @Column(name = "MEMBER_TEL", nullable = false, length = 13)
    private String memberTel;

    @Column(name = "MEMBER_CAREER", nullable = false, length = 50)
    private String memberCareer;

    // 상태값 (ENUM)
    @Enumerated(EnumType.STRING)
    @Column(name = "MEMBER_SUBSCRIBE", nullable = false, length = 1)
    private Status memberSubscribe;

    @Enumerated(EnumType.STRING)
    @Column(name = "MEMBER_ADMIN", nullable = false, length = 1)
    private Status memberAdmin;

    @Enumerated(EnumType.STRING)
    @Column(name = "MEMBER_DEL_FL", nullable = false, length = 1)
    private Status memberDelFl;

    // 프로필
    @Column(name = "PROFILE_IMG", length = 300)
    private String profileImg;

    @Column(name = "MY_INFO_INTRO", length = 2000)
    private String myInfoIntro;

    @Column(name = "MY_INFO_GIT", length = 200)
    private String myInfoGit;

    @Column(name = "MY_INFO_HOMEPAGE", length = 200)
    private String myInfoHomepage;

    // 활동 정보
    @Column(name = "SUBSCRIPTION_PRICE", nullable = false)
    private Integer subscriptionPrice;

    @Column(name = "BEANS_AMOUNT", nullable = false)
    private Integer beansAmount;

    @Column(name = "CURRENT_EXP", nullable = false)
    private Integer currentExp;

    // 회원 가입 날짜
    @Column(name = "M_CREATE_DATE")
    private LocalDateTime mCreateDate;

    // 레벨 테이블키 참조 (FK)
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "MEMBER_LEVEL", nullable = false)
    private Level memberLevel;

    // 생성자 (회원가입용)
    @Builder // @Builder가 필드가 아닌 생성자에 붙어 있음 =>이 경우 생성자 파라미터 이름 기준으로 builder 메서드가 만들어짐
    public Member(String memberEmail, String memberPw, String memberName, String memberNickname,
                  String memberTel, String memberCareer,
                  Status memberAdmin, Status memberSubscribe,
                  Level memberLevel) {

        this.memberEmail = memberEmail;
        this.memberPw = memberPw;
        this.memberName = memberName;
        this.memberNickname = memberNickname;
        this.memberTel = memberTel;
        this.memberCareer = memberCareer;

        // 기본값 세팅
        this.memberSubscribe = memberSubscribe != null ? memberSubscribe : Status.N;
        this.memberAdmin = memberAdmin != null ? memberAdmin : Status.N;
        this.memberDelFl = Status.N;
        this.subscriptionPrice = 0;
        this.beansAmount = 0;
        this.currentExp = 0;
        this.mCreateDate = LocalDateTime.now();

        // FK (LEVEL 테이블)
        this.memberLevel = memberLevel;
    }

    // Member Entity 메서드
    // 비밀번호 변경
    public void changePassword(String encodedPw) {
        this.memberPw = encodedPw;
    }

    // 회원탈퇴
    public void withdraw() {
        this.memberDelFl = Status.Y;
    }

    // 일반회원 -> 관리자 변경
    public void promoteAdmin() {
        this.memberAdmin = Status.Y;
    }

	@PrePersist // 기본값 설정, JPA가 INSERT하기 전 자동 실행 메소드(위 Member생성자 기본값 설정의 double-check)
	public void prePersist() {
		this.mCreateDate = LocalDateTime.now(); // 디폴트값 지정이라고 봐라.
        this.subscriptionPrice = 0;
        this.beansAmount = 0;
        this.currentExp = 0;

		if(this.memberSubscribe == null) {
			this.memberSubscribe = CommonEnums.Status.N;
		}

		if(this.memberAdmin == null) {
			this.memberAdmin = CommonEnums.Status.N;
		}

		if(this.memberDelFl == null) {
			this.memberDelFl = CommonEnums.Status.N;
		}
	}

	// 회원 정보 수정 메소드: 닉네임 & 전화번호
	public void updateMemberInfo(String memberNickname, String memberTel) {
		this.memberNickname = memberNickname; // 필드값 세팅 -> 업데이트
		this.memberTel = memberTel;
	}


	// 회원 정보 수정 메소드 (회원 커피콩 잔액 수정)
	/**
	 * 커피콩 잔액 업데이트
	 * @param newAmount 새로운 커피콩 잔액
	 */
	public void updateBeansAmount(Integer newAmount) {
	    if(newAmount < 0) {
	        throw new IllegalArgumentException("커피콩 잔액은 음수일 수 없습니다.");
	    }
	    this.beansAmount = newAmount;
	}

	/**
	 * 커피콩 차감
	 * @param amount 차감할 커피콩 수
	 */
	public void deductBeans(Integer amount) {
	    if(this.beansAmount < amount) {
	        throw new IllegalStateException("커피콩 잔액이 부족합니다.");
	    }
	    this.beansAmount -= amount;
	}

	/**
	 * 커피콩 충전
	 * @param amount 충전할 커피콩 수
	 */
	public void chargeBeans(Integer amount) {
	    if(amount <= 0) {
	        throw new IllegalArgumentException("충전 금액은 0보다 커야 합니다.");
	    }
	    this.beansAmount += amount;
	}

}

package com.devlog.project.member.model.entity;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Entity
@Table(name="AUTH")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@ToString
public class Auth {

	// PK
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "SEQ_AUTH")
    @SequenceGenerator(
            name = "SEQ_AUTH",
            sequenceName = "SEQ_AUTH_NO",
            allocationSize = 1
    )
    @Column(name = "AUTH_NO")
    private Long authNo;


    // 이메일 인증 코드
    @Column(name = "CODE", nullable = false, length = 100)
    private String code;

    @Column(name = "EMAIL", nullable = false, length = 100, unique = true)
    private String email;

    // 이메일 인증 코드 발급 날짜
    @Column(name = "CREATE_AT", nullable = false)
    private LocalDateTime createAt;

    // 생성자 (이메일 인증 코드 발급용)
    @Builder //
    public Auth(String authKey, String email) {
        this.code = authKey;
        this.email = email;
        this.createAt = LocalDateTime.now(); // 생성 시점 초기화
    }

    // Auth Entity 메서드
    // 코드 변경
	public void setCode(String authKey) {
		this.code = authKey;
		this.createAt = LocalDateTime.now();
	}

}

package com.devlog.project.member.enums;

import com.fasterxml.jackson.annotation.JsonCreator;

public class CommonEnums {

	public enum Status {
		Y, N;

		@JsonCreator
		public static Status from(String value) {
			return value == null ? null : Status.valueOf(value.toUpperCase());
		}

	}

}

 2. 로그인과 회원 가입을위한 front는 첨부한 login.html, login.css, login.js, signUp.html, signUp.css, signUp.js는 spring boot의 thymeleaf를 사용하도록 작성된 건데, 이것도 FastAPI와 native JS 기반 프론트엔드에 맞게 바꿔줘. 그리고 여기서 main.html과 main.css,main.js를 네가 작성해 줬으면 좋겠는데, naviation bar를 기반으로 하는 일반적인 형태의 main으로 작성해 주면서 일단 navigation bar에 메뉴는 자유게시판, 모니터링 대쉬보드, 데이터 분석, ML/DL 모델링의 4 메뉴를 placeholder로 넣어줘. header, footer또한 네가 그에 맞춰 작성해주는데, header에는 앞에서 옮겨온 login 메뉴가 풀다운메뉴로 우측에 위치했으면 좋겠고, 그 옆에는 알림 메뉴가 위치하도록 했으면 좋겠어. main, header, footer는 첨부한 걸 한 예로 참조 해줘.


<!DOCTYPE html>
<html lang="ko" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>로그인</title>

    <link rel="stylesheet" th:href="@{/css/member/login.css}">
    <link rel="stylesheet" th:href="@{/css/common/font.css}">
    <link rel="stylesheet" th:href="@{/css/common/common.css}" />
    <link rel="stylesheet" th:href="@{/css/common/notification.css}" />

</head>

<body>


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


        <div class="container">
            <!-- session.loginMember 테스트 -->
            <!-- <p th:text="${session.loginMember}"></p> -->

            <!-- 로고 영역 -->
            <img th:src="@{/images/member/DevLog_logo.png}" class="logo" alt="logo">

            <div class="login-box">
                <form th:action="@{/member/login}" method="POST" id="loginFrm">

                    <!-- 아이디 -->
                    <input  type="text" name="memberEmail"
                            class="input" placeholder="아이디"
                            th:value="${cookie?.saveId?.value}"
                            required
                    />
                    <!-- cookie 는 Spring이 항상 넣어주는 객체가 아님: 쿠키가 하나도 없으면 cookie == null -->

                    <!-- 비밀번호 -->
                    <input  type="password" name="memberPw"
                            class="input" placeholder="비밀번호" required
                    />

                    <!-- 로그인 버튼 -->
                    <button type="submit" class="btn-login">로그인</button>

                    <div class="options">
                        <label class="checkbox">
                            <input  type="checkbox" name="saveId"
                                    id="saveId"
                                    th:checked="${cookie?.saveId?.value}"
                            />
                            아이디 저장
                        </label>

                        <a th:href="@{/member/signUp}" class="signUp">회원가입</a>
                    </div>

                    <!-- OR 구분선 -->
                    <div class="divider">OR</div>

                    <!-- 카카오 로그인 -->
                    <button type="button" class="btn-kakao" id="kakaoLoginBtn">
                        <img th:src="@{/images/member/topic_ballon.png}" class="kakao-icon" alt="">
                        카카오 로그인
                    </button>
                </form>
            </div>
        </div>


        <!--  ###################################################### -->
        <!-- <footer class="main-footer">footer</footer> -->
        <!-- footer.html 추가 -->
        <!-- <th:block th:replace="~{common/footer}">footer.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/footer :: footer"></div>

    </main>

    <!-- login.js 추가 -->
    <script th:src="@{/js/member/login.js}"></script>

</body>
</html>


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

/* === 전체 페이지 레이아웃 === */
.page-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f9f9f9;

}

.main-header,
.main-nav,
.main-footer {
    height: 60px;
    background-color: white;
    width: 100%;
    color: white;
}


/* ========================= */

/* @font-face {
    font-family: 'Pretendard';
    src: url('../font/PretendardVariable.ttf') format('truetype');
    font-weight: 45 920;
    font-style: normal;
    font-display: swap;
} */
/* Spring Boot 절대경로 => src: url('/font/PretendardVariable.ttf') format('truetype'); */
/* 상대경로 => src: url('../font/PretendardVariable.ttf') format('truetype'); */
/* Spring Security의 Security Config에 "/font/**" 로 폰트경로 허용 필요 */

body {
    margin: 0;
    background-color: #ffffff;
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
    /* body 전체에 Pretendard Variable Font 적용*/
}

.container {
    width: 100%;
    height: 100vh; /* 부모와 상관없이 항상 화면 높이(Viewport Height)기준: 브라우저 화면 전체 높이 100%*/
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.logo {
    width: 238px;
    margin-bottom: 2px;
}

/* 로그인 박스 */
.login-box {
    width: 360px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* 입력창 */
.input {
    width: 100%;
    padding: 12px;
    margin-bottom: 12px;
    border-radius: 6px;
    border: 2px solid #000;
    font-size: 20px;
    color: black;
    box-sizing: border-box;
}

/* 로그인 버튼 */
.btn-login {
    width: 100%;
    padding: 12px;
    background-color: #BD83CE;   /* DevLog 보라 */
    border: none;
    border-radius: 6px;
    font-size: 26px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    margin-top: 6px;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.btn-login:hover {
    background-color: #E5B0EA;
}

/* 아이디 저장 / 회원가입 */
.options {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;

}

.checkbox {
    display: flex;
    align-items: center;
    font-size: 16px;
    padding-left: 6px;
}

/*
.checkbox input[type="checkbox"] {
    margin-right: 10px;
    transform: scale(1.4);
    accent-color: #2563eb;
}*/

#saveId {
    appearance: none;
    -webkit-appearance: none;

    width: 20px;
    height: 20px;

    margin-right: 10px; /* '아이디저장' 들여쓰기 되도록 */

    border: 1px solid #999;
    border-radius: 0;

    background-color: #fff;   /* 필수 */
    cursor: pointer;
    position: relative;
}

#saveId:checked {
    background-color: #BD83CE;
    border-color: #BD83CE;
}

#saveId:checked::after {
    content: '';
    position: absolute;
    width: 8px;
    height: 10px;
    border: solid #fff;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
    top: 1px;
    left: 3px;
    bottom: 0px;
    margin-bottom: 1px;
    margin-left: 2px;
}


.signUp {
    text-decoration: none;
    color: #000;
    font-size: 20px;
}

.signUp:hover {
    text-decoration: underline;
}

/* OR Divider */
.divider {
    width: 100%;
    text-align: center;
    color: #000;

    margin-bottom: 20px;
    position: relative;
    font-size: 20px;
    /*font-weight: bold;*/
}

.divider::before,
.divider::after {
    content: "";
    width: 40%;
    height: 4px;
    background-color: #BD83CE;
    position: absolute;
    top: 50%;
}

.divider::before {
    left: 6px;
}

.divider::after {
    right: 6px;
}

/* 카카오 로그인 버튼 */
.btn-kakao {
    width: 100%;
    padding: 6px;
    background-color: #F2D51F;
    font-size: 20px;
    color: black;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.kakao-icon {
    width: 48px;
    margin-right: 28px;
}

.btn-kakao:hover {
    background-color: #FEE500;
}


console.log("login.js loaded...");



const loginFrm = document.getElementById("loginFrm");
const memberEmail = document.querySelector("input[name='memberEmail']");
const memberPw = document.getElementsByName("memberPw")[0];
const saveId = document.getElementById("saveId");

if (loginFrm != null) {
    loginFrm.addEventListener("submit", e => {
        // 기본 폼 제출 막기
        e.preventDefault();

        // 이메일 유효성 검사
        if (memberEmail.value.trim().length == 0) {
            alert("이메일을 입력해 주세요");
            memberEmail.focus();
            memberEmail.value = '';
            return;  // 이메일 미 입력시 무조건 return해야 아래 비밀번호 검사 안함
        }

        // 비밀번호 유효성 검사
        if (memberPw.value.trim().length == 0) {
            alert("비밀번호를 입력해 주세요");
            memberPw.focus();
            memberPw.value = '';
            return;
        }

        const formData = new URLSearchParams();
        formData.append("memberEmail", memberEmail.value.trim());
        formData.append("memberPw", memberPw.value);

        // 체크되어 있으면 saveId 전송
        if (saveId.checked) {
            formData.append("saveId", "on"); // 값은 아무 문자열이나 OK(null 만아니면됨)
        }

        // 디버깅
        console.log("saveId checked:", saveId.checked);
        console.log(formData.toString());

        fetch('/member/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        })
        .then(async response => {
            if (!response.ok) {
                // 실패 시 Body에서 메시지 추출
                const data = await response.json();
                if(data == null) {
                    console.log('data is null');
                }
                else {
                    console.log(data);
                }
                throw new Error(data.message || '로그인 실패');
            }
            return response.json();
        })
        .then(data => {
            console.log('로그인 성공:', data);
            // 메인 페이지로 이동
            window.location.href = '/'; //  브라우저가 해당 URL로 새로 요청 -> 현재 페이지에서 / 경로로 브라우저가 이동 (redirect)
            //window.location.href = '/member/login'; //  session.loginMember 갱신 테스트용
            // 클라이언트 측에서 페이지 이동이 일어나므로 redirect 동작
        })
        .catch(error => {
            console.error('로그인 오류:', error);
            alert(error.message); // 로그인 실패(401 Unauthorized) 또는 기타 서버 오류(500 INTERNAL_SERVER_ERROR)
            // 실패 시 비밀번호 초기화
            memberPw.value = '';
            memberPw.focus();
        });
    });
}


// 카카오 소셜로그인
const kakaoLoginBtn = document.getElementById("kakaoLoginBtn");

kakaoLoginBtn.addEventListener("click", function () {
            // DevLog 서비스 서버로 이동
            window.location.href = "/app/login/kakao";
});


// 자바스크립트 쿠키 얻어오기: key를 전달하면, value얻는 JS함수
function getCookie(key) {
    const cookies = document.cookie;
    // 현재 페이지에서 접근 가능한 모든 쿠키를 "문자열"로 가지고 옴(특정쿠키만 가져오는건 spring-boot version 3이상에서 않됨)

    console.log("inside getCookie() function: ");
    console.log(cookies);

    // saveId=user01@og.or.kr; test=123; temp=abc;
    // 배열.map() : 배열의 모든 요소에 순차 접근하여 함수 수행 후
    //             수행 결과를 이용해서 새로운 배열을 만드는 함수
    const cookieList = cookies.split("; ").map(cookie => cookie.split("="))
    // {saveId=user01@og.or.kr, test=123, temp=abc}
    //
    //console.log(cookieList); //

    // [[a, 1], [b, 1]]
    const obj = {}; // 비어있는 JS 객체 생성

    for(let i=0; i<cookieList.length; i++) {
        obj[cookieList[i][0]] = cookieList[i][1]; // K값에 V를 대입 형식으로 담겨지게 된다.
    } // obj = {a:1, b:1}

    return obj[key];
}


// 쿠키에 saveId가 있을 경우
if( document.getElementsByName("memberEmail")[0] != null ) {
    // 화면에 memberEmail이 있을 경우

    const saveId = getCookie("saveId");
    // 있으면 이메일, 없으면 undefined 나온다

    console.log("cookie(saveId) in current view by getCookie() 함수: ");
    console.log(saveId);

    if (saveId != undefined) { // 쿠키에 저장된 이메일이 있는 경우
        // memberEmail input에 값 세팅
        // document.getElementsByName("memberEmail")[0].value = saveId;
        document.querySelector("input[name='memberEmail'").value = saveId;
        // 아이디 저장 checkbox 체크하기
        // document.getElementsByName("saveId")[0].checked = true;
        document.querySelector("input[name='saveId']").checked = true;

    }
}




<!DOCTYPE html>
<html lang="ko" xmlns="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>회원가입</title>

    <link rel="stylesheet" th:href="@{/css/member/signUp.css}">
    <link rel="stylesheet" th:href="@{/css/common/font.css}">
    <link rel="stylesheet" th:href="@{/css/common/common.css}" />
    <link rel="stylesheet" th:href="@{/css/common/notification.css}" />

</head>

<body>

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
            <h2 class="title fw-800">회원가입</h2>
            <div class="container">
                <div class="signup-box">

                    <!-- <h2 class="title">회원가입</h2> -->

                    <form th:action="@{/member/signUp}" method="POST" name="signUpFrm" id="signUpFrm">

                        <!-- 이메일 -->
                        <label class="label" for="memberEmail">아이디(이메일) <span class="required">*</span></label>
                        <div class="row">
                            <input type="email" class="input" name="memberEmail" id="memberEmail"
                                placeholder="이메일을 입력해 주세요" maxlength="30" autocomplete="off">
                            <button id="sendAuthKeyBtn" type="button" class="btn-gray">인증 번호 받기</button>
                        </div>
                        <p class="desc" id="emailMessage">메일을 받을 수 있는 이메일을 입력해 주세요.</p>

                        <!-- 인증번호 -->
                        <label class="label" for="authKey">인증번호 <span class="required">*</span></label>
                        <div class="row">
                            <input type="text" name="authKey" id="authKey" class="input"
                                placeholder="이메일로 받은 인증번호 입력 후 인증하기 버튼을 클릭해 주세요">
                            <button id="checkAuthKeyBtn" type="button" class="btn-gray">인증 하기</button>
                        </div>
                        <p class="desc" id="authKeyMessage"></p>
                        <!-- 인증번호가 일치하지 않습니다 -->

                        <div class="spaceholder"><p><br></p></div>

                        <!-- 비밀번호 -->
                        <label class="label" for="memberPw">비밀번호 <span class="required">*</span></label>
                        <input type="password" name="memberPw" id="memberPw" class="input"
                            placeholder="비밀번호를 입력해주세요" maxlength="20">
                        <p class="desc" id="pwMessage">영어,숫자,특수문자(!,@,#,-,_) 6~20자로 사이로 입력해주세요.</p>

                        <!-- 비밀번호 확인 -->
                        <label class="label" for="memberPwConfirm">비밀번호 확인 <span class="required">*</span></label>
                        <input type="password" name="memberPwConfirm" id="memberPwConfirm" class="input"
                            placeholder="비밀번호 확인을 입력해주세요"  maxlength="20">
                        <p class="desc"id="pwCheckMessage">위에서 입력하신 비밀번호와 동일하게 입력해주세요.</p>

                        <!-- 이름 -->
                        <label class="label" for="memberName">이름 <span class="required">*</span></label>
                        <input type="text" name="memberName" id="memberName" class="input"
                            placeholder="이름을 입력해주세요" maxlength="10" >
                        <p class="desc" id="nameMessage">유효한 이름을 입력해주세요 (예시: 홍길동)</p>

                        <!-- 닉네임 -->
                        <label class="label" for="memberNickname">닉네임 <span class="required">*</span></label>
                        <input type="text" name="memberNickname" id="memberNickname" class="input"
                            placeholder="닉네임을 입력해주세요" maxlength="10" >
                        <p class="desc" id="nicknameMessage">한글, 영어, 숫자로만 2~10자</p>

                        <!-- 전화번호 -->
                        <label class="label" for="memberTel">전화번호 <span class="required">*</span></label>
                        <input type="text" name="memberTel" id="memberTel" class="input"
                            placeholder="(- 없이 숫자만 입력)" maxlength="11">
                        <p class="desc" id="telMessage">전화번호를 입력해주세요 (- 제외)</p>

                        <!-- 경력사항 -->
                        <label class="label" for="memberCareer">경력사항 <span class="required">*</span></label>
                        <input type="text" name="memberCareer" id="memberCareer" class="input"
                            placeholder="개발 경력(개발년차)를 입력해주세요">
                        <p class="desc" id="careerMessage">유효한 경력사항을 입력해주세요 (예시: 백엔드 3년차)</p>


                        <!-- 이메일 수신 -->
                        <label class="check fw-600" for="memberSubscribe">
                            <!-- 체크되면 브라우저는 무조건 "on" 을 전송함 => value="Y" 로 enums와 맞춰야함 -->
                            <input type="checkbox" name="memberSubscribe" id="memberSubscribe" value="Y">
                            이메일 수신동의 (회원 전용 정보 제공 메일 수신에 동의합니다)
                        </label>

                        <!-- 관리자 신청 -->
                        <div class="row admin-code">
                            <label class="check fw-600" for="memberAdmin">
                            <!-- 체크되면 브라우저는 무조건 "on" 을 전송함 => value="Y" 로 enums와 맞춰야함 -->
                                <input type="checkbox" name="memberAdmin" id="memberAdmin"  value="Y">
                                관리자 계정 신청
                            </label>
                            <div class="input-admin-code-wrapper">
                                <!-- <label for="adminCode"> </label> -->
                                <input type="text" name="adminCode" id="adminCode" class="input admin-code"
                                    placeholder="관리자 계정 승인코드 입력">
                                <p class="desc" id="adminCodeMessage"></p>
                            </div>
                        </div>


                        <div class="spaceholder"><p><br></p></div>

                        <!-- 가입 버튼 -->
                        <div class="btn-join-wrapper">
                            <button type="submit" id="signUpBtn" class="btn-join">가입 하기</button>
                        </div>


                    </form>
                </div>
            </div>
        </div>

        <!--  ###################################################### -->
        <!-- <footer class="main-footer">footer</footer> -->
        <!-- footer.html 추가 -->
        <!-- <th:block th:replace="~{common/footer}">footer.html</th:block> -->
        <!-- 또는 -->
        <div th:replace="common/footer :: footer"></div>

    </main>

    <!-- login.js 추가 -->
    <script th:src="@{/js/member/signUp.js}"></script>

</body>
</html>


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

/* === 전체 페이지 레이아웃 === */
.page-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f9f9f9;

}

.main-header,
.main-nav,
.main-footer {
    height: 60px;
    background-color: white;
    width: 100%;
    color: white;
}


/* ========================= */
body {
    margin: 0;
    background-color: #ffffff;
    font-family: 'Pretendard Variable', Arial, Helvetica, sans-serif;
    /* body 전체에 Pretendard Variable Font 적용*/
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


.title {
    background: linear-gradient(
        to right,
        rgba(241, 198, 231, 1) 0%,       /* #F1C6E7 불투명도 100% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치도 불투명도 75% */
        rgba(241, 198, 231, 0.75) 50%,   /* 50% 위치 투명도 75% */
        rgba(241, 198, 231, 0.5) 100%    /* 100% 위치 투명도 50% */
    );
    padding: 12px 12px 12px 120px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: #000;
    font-size: 30px;
    font-weight: bolder;
    margin-bottom: 25px;
}

.container {
    width: 100%;
    display: flex;
    padding: 10px 0;
    justify-content: center;
}

.signup-box {
    width: 1080px;
    background: #fff;
    padding: 30px 40px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}



.label {
    font-size: 30px;
    font-weight: bold;
    display: block;
    margin-top: 18px;
}

.required {
    color: red;
}

.input {
    width: 100%;
    margin-top: 6px;
    padding: 12px;
    border-radius: 4px;
    border: 1px solid #D9D9D9;
    font-size: 24px; /* placeholder 크기 */
    color:  #000;
    box-sizing: border-box;

}

/* 'signUp-message' == 'desc' */
.desc {
    font-size: 24px;
    color: #000;
    margin-top: 14px;
    padding-left: 30px; /* 설명 들여쓰기 */
}

.row {
    display: flex;
    gap: 1px; /* input과 인증번호 버튼간 간격 */
    margin-top: 6px;
}

/* :focus-within : 내부 input 요소에 포커스가 맞춰졌을 때 */
.row:focus-within{
    border-bottom-color: #BD83CE;
}

/* 메세지 색상 지정 */
.confirm{ color : green; }
.error{ color : red; }


.btn-gray {
    width: 200px;
    margin-top: 6px;
    padding: 12px 16px;
    background: #ffffff;
    border: 1px solid #000;
    cursor: pointer;
    border-radius: 0px;
    font-size: 24px;
    font-weight: bold;
    white-space: nowrap;
}

.btn-gray:hover {
    background: #BD83CE;
    color: white;
    border: 1px solid #BD83CE;
}

div.spaceholder{ /* 임의 행간격 삽입용*/
    margin: 30px;
}


/* 체크 박스 항목 */
.check {
    display: flex;
    align-items: center;
    margin-top: 40px;
    margin-bottom: 40px;
    font-size: 24px;
}

.check input[type="checkbox"] {
    margin-right: 10px;
    transform: scale(2.0);
    accent-color: #BD83CE;
    margin-right: 26px;
}

.row.admin-code {
    display: flex;
    justify-content: start;
    flex-direction: row;
    align-items: first baseline;
}


.input-admin-code-wrapper{
    display: flex;
    justify-content: start;
    flex-direction: column;
    align-items: center;
}

.input.admin-code {
    width: 80%;
    margin-top: 0px;
    margin-left: 76px;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #D9D9D9;
    font-size: 24px; /* placeholder 크기 */
    color:  #000;
    box-sizing: border-box;
}


/* 가입하기 버튼 */
.btn-join-wrapper{
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}

.btn-join {
    width: 40%;
    margin-top: 25px;
    margin-bottom: 100px;
    padding: 14px;

    background-color: #BD83CE;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 36px;
    cursor: pointer;
}

.btn-join:hover {
    background-color: #E5B0EA;
}


console.log('signUp.js loaded ...')


// 유효성 검사 진행 여부 확인 객체
const checkObj = {
    'memberEmail' : false,
    'memberPw' : false,
    'memberPwConfirm' : false,
    'memberName' : false,
    'memberNickname' : false,
    'memberTel' : false,
    'memberCareer' : false,
    'memberSubscribe': true, // 필수아님
    'memberAdmin': true, // 필수아니나, 체크시 유효성검사필요 (관리자 계정 승인 코드 체크필수)
    'authKey' : false  // 이메일 인증에서 사용
}

// 이메일 유효성 검사
const memberEmail = document.getElementById("memberEmail");
const emailMessage = document.getElementById("emailMessage")

memberEmail.addEventListener("input", function(){

    // 입력된 이메일이 없을 경우 : "메일을 받을 수 있는 이메일을 입력해주세요." 까만글씨
    // 1) 이메일 미작성시
    if(memberEmail.value == ""){
        emailMessage.innerText = "메일을 받을 수 있는 이메일을 입력해주세요.";
        //emailMessage.style.color = "black";
        emailMessage.classList.remove("confirm", "error");

        checkObj.memberEmail = false;

        return;
    }

    // 입력된 이메일이 있는 경우 정규식 일치 여부 판별
    // 영어, 숫자, -, _ 4글자 이상 @ 영어.영어.영어 || 영어.영어
    const regExp = /^[\w\_\.]{4,}@[a-z]+(\.[a-z]+){1,2}$/; //"id는 4글자 이상" //



    //

    // 유효한 경우 : 유효한 이메일 형식 입니다. 초록글씨
    if (regExp.test(memberEmail.value)) { // input 창에서 입력받은 이메일
        // 유효한 경우
        console.log(memberEmail.value);

        // ***********************************
        // fetch() API를 이용한 ajax

        // Get 방식 ajax 요청(쿼리스트링으로 파라미터 전달 : ?키=값&키=값)
        fetch("/dupCheck/email?email=" + memberEmail.value) // 띄어쓰기 없어야함
        .then(resp => resp.text()) // 조회된 회원수 count이므로 단순 text
        .then(count => {
            console.log("public int dupCheckEmail(String email) 리턴값:") // public int dupCheckEmail(String email)
            console.log(count);
            // count : 중복이면 1, 아니면 0
            if (count==1){
                // 유효한 경우, 중북이메일 인 경우
                emailMessage.innerText = "이미 사용중인 이메일 입니다.";
                emailMessage.classList.remove("confirm");
                emailMessage.classList.add("error");

                checkObj.memberEmail = false;
            } else {
                // 유효한 경우, 중북이메일이 아닌 경우
                emailMessage.innerText = "사용 가능한 이메일입니다.";
                emailMessage.classList.remove("error");
                emailMessage.classList.add("confirm");

                checkObj.memberEmail = true;

            }
        })
        .catch(err => console.log(err))  // 예외처리

        // 유효한 경우
        emailMessage.innerText = "유효한 이메일 형식 입니다.";
        emailMessage.classList.add("confirm");
        emailMessage.classList.remove("error");

        checkObj.memberEmail = true;

    } else {
        // 유효하지 않은 경우 : 이메일 형식이 유효하지 않습니다. 빨간 글씨
        emailMessage.innerText = "이메일 형식이 유효하지 않습니다.";
        emailMessage.classList.add("error");
        emailMessage.classList.remove("confirm");

        checkObj.memberEmail = false;

    }

})


//---------------------------------------------------------------------------
// 이메일 인증
//
// 인증번호 발송
const sendAuthKeyBtn = document.getElementById("sendAuthKeyBtn");
const authKeyMessage = document.getElementById("authKeyMessage");
let authTimer;
let authMin = 4;
let authSec = 59;


// 인증번호를 발송한 이메일 저장
let tempEmail = "";


if (authTimer == undefined){
    console.log("tempEmail = " + tempEmail);
    console.log("authTimer = " + authTimer);
    sendAuthKeyBtn.disabled = false;

    sendAuthKeyBtn.addEventListener("click", function(){
        authMin = 4;
        authSec = 59;


        checkObj.authKey = false;


        if(checkObj.memberEmail){ // 유효하고, 중복이 아닌 이메일인 경우

            /* fetch() API 방식 ajax */
            fetch("/sendEmail/signUp?email="+memberEmail.value) // GET방식, key값은 email
            .then(resp => resp.text()) // text로 parsing
            .then(result => {  // result변수로 text값 받아온다.
                if(result > 0){
                    console.log("인증 번호가 발송되었습니다.")
                    tempEmail = memberEmail.value;
                }else{
                    console.log("인증번호 발송 실패")
                }
            })
            .catch(err => {
                console.log("이메일 발송 중 에러 발생");
                console.log(err);
            });

            alert("인증번호가 발송 되었습니다."); // 비동기 통신처리중 띄워주는 메시지

            authKeyMessage.innerText = "05:00"; // timer시작 (5분)
            authKeyMessage.classList.remove("confirm");
            clearInterval(authTimer); // 기존 것 지우고 다시시작 해라!

            //if (authTimer == 2){
                authTimer = window.setInterval(()=>{
                console.log("authTimer gen = " + authTimer);
                                                //                                    04  또는       14
                    authKeyMessage.innerText = "0" + authMin + ":" + (authSec<10 ? "0" + authSec : authSec);

                    // 남은 시간이 0분 0초인 경우
                    if(authMin == 0 && authSec == 0){
                        checkObj.authKey = false; // 인증 번호 유효성 검사만 무효화

                        clearInterval(authTimer);
                        return;
                    }

                    // 0초인 경우
                    if(authSec == 0){
                        authSec = 60;
                        authMin--;
                    }

                    authSec--; // 1초 감소

                }, 1000)
            //}


        } else{
            alert("중복되지 않은 이메일을 작성해주세요.");
            memberEmail.focus();
        }


    });

} else { //authTimer != undefined 인 경우
    console.log("tempEmail = " + tempEmail);
    console.log("authTimer = " + authTimer);
    sendAuthKeyBtn.disabled = true;
}




// 인증 확인
const authKey = document.getElementById("authKey");
const checkAuthKeyBtn = document.getElementById("checkAuthKeyBtn");


checkAuthKeyBtn.addEventListener("click", function(){

    if(authMin > 0 || authSec > 0){ // 시간 제한이 지나지 않은 경우에만 인증번호 검사 진행
        /* fetch API */
        const obj = {"inputKey":authKey.value, "email":tempEmail}
        const query = new URLSearchParams(obj).toString()
        // ?inputKey=123456&email=user01@og.or.kr 로 바뀐다 by URLSearchParams(obj).toString()

        fetch("/sendEmail/checkAuthKey?" + query) // 비동기 통신 보낸다
        .then(resp => resp.text())
        .then(result => {
            if(result > 0){
                clearInterval(authTimer);
                authKeyMessage.innerText = "인증되었습니다.";
                authKeyMessage.classList.add("confirm");
                checkObj.authKey = true;


            } else{
                alert("인증번호가 일치하지 않습니다.")
                checkObj.authKey = false;
            }
        })
        .catch(err => console.log(err));

    } else{
        alert("인증 시간이 만료되었습니다. 다시 시도해주세요.")
    }


});





// --------------------------------------------------------------------------

// 비밀번호/비밀번호 확인 유효성 검사
// checkPw() 함수로 만들어 해봐라(숙제)

const memberPw = document.getElementById("memberPw");
const memberPwConfirm = document.getElementById("memberPwConfirm");
const pwMessage = document.getElementById("pwMessage");

memberPw.addEventListener("input", function(){
    // 비밀번호를 입력할 때 마다 검사 진행

    // 비밀번호 미 작성 시
    // 영어, 숫자, 특수문자(!, @, #, -, _) 6~20글자 사이로 입력해 주세요. 까만 글씨
    if (memberPw.value.trim().length == 0) {
        memberPw.innerText = "영어, 숫자, 특수문자(!, @, #, -, _) 6~20글자 사이로 입력해 주세요.";
        memberPw.classList.remove("confirm", "error");
        checkObj.memberPw = false;
        return;
    }

    // 비밀번호 입력시

    // 비밀번호 유효성 검사: 영어 대/소문자, 숫자, !, @, #, -, _ 포함한 6~20 글자 사이 (\w에 _ 포함되어있다)
    const regExp = /^[\w!@#\-_]{6,20}$/;

    if (regExp.test(memberPw.value)) {
        // 유효한 경우 : 사용 가능한 비밀번호 입니다. 초록 글씨
        checkObj.memberPw = true;

        // 비밀번호가 유효한 상태에서 비밀번호 확인이 입력되지 않은 경우
        if ( memberPwConfirm.value == "") {
            pwMessage.innerText = "사용가능한 비밀번호 입니다.";
            pwMessage.classList.add("confirm");
            pwMessage.classList.remove("error");

        } else { // 비밀번호 확인이 입력되어 있는 경우

            // 비밀번호와 비밀번호 확인이 같을 경우
            if (memberPw.value == memberPwConfirm.value) {
                pwMessage.innerText = "비밀번호가 일치합니다.";
                pwMessage.classList.add("confirm");
                pwMessage.classList.remove('error');
                checkObj.memberPwConfirm = true;
            } else {
                // 다를 경우
                pwMessage.innerText = "비밀번호가 일치하지 않습니다.";
                pwMessage.classList.add("error");
                pwMessage.classList.remove('confirm');
                checkObj.memberPwConfirm = false;
            }

        }


    } else {
        // 유효하지 않은 경우 : 사용 불가능한 비밀번호 입니다. 빨간 글씨
        pwMessage.innerText = "사용 불가능한 비밀번호 입니다.";
        pwMessage.classList.add("error");
        pwMessage.classList.remove("confirm");
        checkObj.memberPw = false;
    }

})


// 비밀번호 확인 유효성 검사
memberPwConfirm.addEventListener("input", () => {

    // 비밀번호가 입력되지 않은 경우
    if (memberPw.value == ""){
         alert("비밀번호를 입력해주세요.");
         memberPwConfirm.value = ""; // 남아있는값 지우기
         memberPw.focus();
         return;
    }

    // 비밀번호가 유효한 경우
    if (checkObj.memberPw) {
        if (memberPw.value == memberPwConfirm.value){
            // 비밃번호와 비밀번호 확인이 같을 경우
            pwMessage.innerText = "비밀번호가 일치합니다.";
            pwMessage.classList.add("confirm");
            pwMessage.classList.remove("error");

            checkObj.memberPwConfirm = true;

        } else {
            // 다를 경우
            pwMessage.innerText = "비밀번호가 일치하지 않습니다.";
            pwMessage.classList.add("error");
            pwMessage.classList.remove("confirm");

            checkObj.memberPwConfirm = false;

        }



    } else {
        // 비밀번호가 유효하지 않은 경우, 자동으로 memberPwConfirm false
        checkObj.memberPwConfirm = false;
    }

})


// 이름 유효성 검사
const memberName = document.getElementById("memberName");
const nameMessage = document.getElementById("nameMessage");

memberName.addEventListener("input", () =>{
    // 입력된 이름이 없을 경우
    if (memberName == ""){
        nameMessage.innerText = "유효한 한글 이름 입력해 주세요"
        nameMessage.classList.remove("confirm", "error");
        checkObj.memberName = false;
        return;
    }

    // 입력된 이름이 있을 경우
    // 이름 작성시, 유효성 검사: 한글 2~15글자
    const regEx = /^[가-힣]{2,15}$/; //"한글2~15글자 사이"

    if (regEx.test(memberName.value)) {
        // 유효한 경우
        nameMessage.innerText = "유효한 한글 이름입니다."
        nameMessage.classList.add("confirm");
        nameMessage.classList.remove("error");
        checkObj.memberName = true;

    } else {
        // 유효하지 않은 경우
        nameMessage.innerText = "유효하지 않은 한글이름입니다.  한글로만 2~15글자를 넣어주세요."
        nameMessage.classList.add("error");
        nameMessage.classList.remove("confirm");
        checkObj.memberName = false;
    }

})

// 닉네임 유효성 검사
const memberNickname = document.getElementById("memberNickname");
const nicknameMessage = document.getElementById("nicknameMessage");

memberNickname.addEventListener("input", ()=> {

    // 입력된 닉네임이 없을 경우
    if (memberNickname == ""){
        nicknameMessage.innerText = "한글,영어,숫자로만 2~10글자로 입력해 주세요"
        nicknameMessage.classList.remove("confirm", "error");
        checkObj.memberNickname = false;
        return;
    }

    // 입력된 닉네임이 있을 경우
    // 닉네임 작성시, 유효성 검사: 한글,영어,숫자로만 2~10글자
    const regEx = /^[가-힣a-zA-Z0-9]{2,10}$/; //"영어/숫자/한글2~10글자 사이"

    if (regEx.test(memberNickname.value)) {
        // 유효한 경우

        //******************************************* */
        // fetch() API를 이용한 ajax
        // console.log("test : " + memberNickname.value)
        //console.log(memberNickname.value);

        // 요청주소 : /dupCheck/nickname
        // 중복인 경우 : "이미 사용 중인 닉네임입니다." 빨간 글씨
        // 중복이 아닌 경우 : "사용 가능한 닉네임입니다." 초록글씨
        fetch("/dupCheck/nickname?nickname=" + memberNickname.value)
        .then(resp => resp.text()) // 0 or 1이므로 text로: 응답객체 -> 파싱(parsing, 데이터 형태 변환)
        .then(count => {
            // count : 중복1, 아니면 0
            console.log(count);

            //if (count == 1){
            if (count != 0) {
                nicknameMessage.innerText = "이미 사용 중인 닉네임입니다."
                nicknameMessage.classList.add("error");
                nicknameMessage.classList.remove("confirm");
                checkObj.memberNickname = false;
            } else {
                nicknameMessage.innerText = "사용 가능한 닉네임입니다."
                nicknameMessage.classList.add("confirm");
                nicknameMessage.classList.remove("error");
                checkObj.memberNickname = true;
            }
        })
        .catch(err => console.log(err)) // 예외처리

    } else {
        // 유효하지 않은 경우
        nicknameMessage.innerText = "유효하지 않은 닉네임입니다.  한글,영어,숫자로만 2~10글자를 넣어주세요."
        nicknameMessage.classList.add("error");
        nicknameMessage.classList.remove("confirm");
        checkObj.memberNickname = false;
    }

})



// 전화번호 유효성 검사
const memberTel = document.getElementById("memberTel");
const telMessage = document.getElementById("telMessage");

memberTel.addEventListener("input", ()=>{

    // 전화번호 미 입력시
    if(memberTel.value == ""){
        telMessage.innerText = "전화번호를 입력해 주세요.";
        telMessage.classList.remove("confirm", "error");
        checkObj.memberTel = false;
        return;
    }

    // 전화번호 입력시, 유효성 검사: 전화번호를 입력해주세요.(- 제외)
    const regEx = /^0(1[01]|2|[3-6][1-5]|70)\d{7,8}$/; //" 하이픈제외"

    if (regEx.test(memberTel.value)) {
        telMessage.innerText = "유효한 전화번호입니다.";
        telMessage.classList.add("confirm");
        telMessage.classList.remove("error");
        checkObj.memberTel = true;
    } else {
        telMessage.innerText = "존재하지 않은 전화 번호입니다.";
        telMessage.classList.add("error");
        telMessage.classList.remove("confirm");
        checkObj.memberTel = false;
    }

})

// 경력사항 유효성 검사
const memberCareer = document.getElementById("memberCareer");
const careerMessage = document.getElementById("careerMessage");


memberCareer.addEventListener("input", () =>{
    // 입력된 경력 사항이 없을 경우
    if (memberCareer == ""){
        careerMessage.innerText = "경력사항을 입력해 주세요(예시:벡엔드3년차)"
        careerMessage.classList.remove("confirm", "error");
        checkObj.memberCareer = false;
        return;
    }

    // 입력된 경력사항이 있을 경우
    // 경력사항 작성시, 유효성 검사: 한글 + 숫자 둘 다 반드시 포함 + 공백 허용 + 길이 2~40
    const regEx = /^(?=.*[가-힣])(?=.*[0-9])[가-힣0-9 ]{2,40}$/; //"경력(한글)과 년차(숫자)포함 2~40글자 사이"

    if (regEx.test(memberCareer.value)) {
        // 유효한 경우
        careerMessage.innerText = "유효한 경력사항입니다."
        careerMessage.classList.add("confirm");
        careerMessage.classList.remove("error");
        checkObj.memberCareer = true;

    } else {
        // 유효하지 않은 경우
        careerMessage.innerText = "유효하지 않은 경력사항입니다.  경력(한글)과 년차(숫자)포함 2~40글자를 넣어주세요."
        careerMessage.classList.add("error");
        careerMessage.classList.remove("confirm");
        checkObj.memberCareer = false;
    }

})

// 관리자 계정 신청시 관리자 승인코드 유효성 검사
const memberAdmin = document.getElementById("memberAdmin");

const adminCode = document.getElementById("adminCode");
const adminCodeMessage = document.getElementById("adminCodeMessage");

memberAdmin.addEventListener("change", () => {
    if (memberAdmin.checked) {
        console.log("관리자 계정 신청 체크됨");
        // 체크됐을 때 실행할 코드: 입력 adminCode유효성 검사
        checkObj.memberAdmin = false;

        adminCode.addEventListener("input", () => {
            if (adminCode.value == ""){
                adminCodeMessage.innerText = "발급된 관리자계정 승인코드 입력"
                adminCodeMessage.classList.remove("confirm", "error");
                checkObj.memberAdmin = false;
                return;
            }
            // 요청주소 : /checkCode/adminCode
            // 관리자승인코드 비유효 : "승인되지 않은 코드입니다." 빨간 글씨
            // 관리자승인 코드 유효 : "승인된 코드입니다." 초록글씨
            fetch("/checkCode/adminCode?adminCode=" + adminCode.value) // 입력파라미터명은 "adminCode"이 된다

            .then(resp => resp.text()) // 0 or 1이므로 text로: 응답객체 -> 파싱(parsing, 데이터 형태 변환)
            .then(result => {
                // result : 유효한 관리자 승인코드1, 아니면 0
                console.log("유효한 관리자승인코드 ? : " + result);

                //if (result == 1){
                if (result != 0) {
                    adminCodeMessage.innerText = "승인된 코드입니다."
                    adminCodeMessage.classList.add("confirm");
                    adminCodeMessage.classList.remove("error");
                    checkObj.memberAdmin = true;

                    console.log(" 지금까지 유효성 검사 결과: ")
                    console.log(checkObj)

                } else {
                    adminCodeMessage.innerText = "승인되지 않은 코드입니다."
                    adminCodeMessage.classList.add("error");
                    adminCodeMessage.classList.remove("confirm");
                    checkObj.memberAdmin = false;
                }
            })
            .catch(err => console.log(err)) // 예외처리
        })

    } else {
        console.log("관리자  계정 신청 체크 해제됨");
        // 해제됐을 때 실행할 코드
        adminCodeMessage.innerText = ""
        adminCodeMessage.classList.remove("confirm", "error");
        checkObj.memberAdmin = true;
    }
});

// 맨처음 로딩됬을때 상태 => 물론 아직 이벤트발생이 일어난적 없으니 모두 False 초기값임
console.log(" 초기 유효성 검사 상태: ")
console.log(checkObj)

document.getElementById("signUpFrm").addEventListener("submit", e => {

    // checkObj에 모든 value가 true인지 검사

    for (let key in checkObj) {
        console.log(key);

        console.log(checkObj[key]);

        if(!checkObj[key]){ // 유효하지 않은 경우

            switch(key) {

                case 'memberEmail': alert("이메일이 유효하지 않습니다."); break;
                case 'memberPw': alert("비밀번호가 유효하지 않습니다."); break;
                case 'memberPwConfirm': alert("비밀번호확인이 유효하지 않습니다."); break;
                case 'memberName': alert("이름이 유효하지 않습니다."); break;
                case 'memberNickname': alert("닉네임이 유효하지 않습니다."); break;
                case 'memberTel': alert("전화번호가 유효하지 않습니다."); break;
                case 'memberCareer': alert("경력사항이 유효하지 않습니다."); break;
                case 'memberSubscribe': alert("이메일 수신동의가 유효하지 않습니다."); break;
                case 'memberAdmin': alert("관리자 승인코드가 유효하지 않습니다."); break;
                case 'authKey': alert("이메일 인증 authKey가 유효하지 않습니다."); break;
            }

            // 유효하지 않은 input 태그 포커스
            // -> key와 input의 id가 똑같음
            document.getElementById(key).focus();

            // form태그 기본 이벤트 제거
            e.preventDefault(); // 기본이벤트 제거(form submit 방지)
            return; // 유효하지 않은것 확인했으므로 종료하고 더이상 진행않함
        }

    }

})



<!DOCTYPE html>
<html lang="ko" xmlns="http://www.thymeleaf.org"> <!-- 현재 HTML 문서에 타임리프 문법을 사용한다고 선언 -->
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>프로젝트</title>

</head>
<body>

    <main>

        <!-- header.html 추가(포함): 경로 = "common/header" -->
        <!-- th:block : html태그가 아닌 단순히 타임리프를 쓰기 위한 태그가 필요할 때 사용(thymeleaf에 유일한 태그)
             -> th:block은 타임리프 해석 시 다른 타임리프 수행 후(랜더링후) 사라짐

             th:replace="~{template 폴더 기준으로 접두사, 접미사 제외하고 작성}"
        -->
		<th:block th:replace="~{common/header}"></th:block>


        <section class="content">
            <section class="content-1">


                <!-- <p th:text="${name} ? true : false "></p> -->
                <!-- name : session.name alse "></p> -->
                <!-- ${name} 값이 있으면 true, 없으면 false -->

                <!-- <h3>삼항 연산자</h3>
                <p th:text="${name} ? ${name} : '이름 없음' "></p>
                <p th:text="${name2} ? ${name2} : '이름 없음' "></p>

                <h3>Elvis 연산자</h3>
                <p th:text="${name} ?: '이름 없음' "></p>
                <p th:text="${name2} ?: '이름 없음' "></p>

                <h3>No-Operation</h3>
                <p th:text="${name} ?:_">(태그에 작성)이름 없음</p>
                <p th:text="${name2} ?:_">(태그에 작성)이름 없음</p>


                ${sessionScope.loginMember} -->

                <hr>

                <h3>이메일이 일치하는 회원의 닉네임 조회</h3>
                email : <input type="text" value="user02@og.or.kr">
                <button onclick="selectNickname('user02@og.or.kr')">조회</button>
                <div id="result">콘솔 확인</div>

                <hr>

                <h3>닉네임이 일치하는 회원의 전화번호 조회</h3>
                <input type=" text" id="inputNickname">
                <button id="btn1">조회</button>
                <h4 id="result1"></h4>

                <hr>

                <h3>이메일을 입력 받아 일치하는 회원의 정보 조회</h3>
                email : <input type="text" id="inputEmail">
                <button id="btn2">조회</button>
                <ul id="result2"></ul>

                <hr>
                <h3>이메일이 일부라도 일치하는 모든 회원 조회</h3>
                검색어 : <input type="text" id="input">
                <button id="btn3">조회</button>

                <table border="1" style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th>회원번호</th>
                            <th>이메일</th>
                            <th>닉네임</th>
                        </tr>

                    </thead>
                    <tbody id="result3"></tbody>

                </table>


            </section>

            <section class="content-2">


                <!-- 로그인 X -->
                <!-- <th:block th:unless="${session.loginMember != null}"> -->
                <th:block th:unless="${session.loginMember}"> <!-- 값있으면 true, 없으면 false -->
                    <!-- if 조건식에 값만 작성한 경우 : 있으면 true, 없으면 false -->
                     <!-- thymeleaf에서는 session. 써줘야 함.  -->

                    <!-- method="POST" : 제출 되는 값이 주소에 안보임 -->
                    <form th:action="@{/member/login}" method="POST" id="loginFrm">
                        <fieldset class="id-pw-area">
                            <section>
                                <input type="text" name="memberEmail" placeholder="이메일"
                                autocomplete="off" value="">
                                <input type="password" name="memberPw" placeholder="비밀번호">
                            </section>
                            <section>
                                <button>로그인</button>
                            </section>
                        </fieldset>


                        <label>
                            <input type="checkbox" name="saveId" > 아이디 저장
                        </label>

                        <article class="signup-find-area">
                            <a th:href="@{/member/signUp}">회원가입</a>
                            <span>|</span>
                            <a th:href="@{#}">ID/PW 찾기</a>
                        </article>
                    </form>
                </th:block>


                <th:block th:if="${session.loginMember}"> <!-- 값있으면 true, 없으면 false -->
                    <!-- 로그인 되었을 때 -->
                     <article class="login-area">

                         <a th:href="@{/myPage/profile}">

                             <!-- 프로필 이미지가 없는 경우 -->
                             <!-- <img th:src="@{/images/user.png}" id="memberProfile"> -->
                             <img th:unless="${session.loginMember.profileImage}" th:src="@{/images/user.png}" id="memberProfile">
                             <!-- 프로필 이미지가 있는 경우 -->
                             <img th:if="${session.loginMember.profileImage}" th:src="${session.loginMember.profileImage}" id="memberProfile">

                         </a>

                         <div class="my-info">
                             <div>
                                 <!-- <th:block th:text="${session.loginMember.memberNickname}">로그인한 회원의 닉네임</th:block> -->
                                 <a th:href="@{/myPage/info}" id="nickname">[[${session.loginMember.memberNickname}]]</a>

                                 <a th:href="@{/member/logout}" id="logoutBtn">로그아웃</a>
                             </div>

                             <p>[[${session.loginMember.memberEmail}]]</p>

                         </div>
                     </article>
                </th:block>


            </section>
        </section>
    </main>

    <!-- footer.html 추가 -->
    <th:block th:replace="~{common/footer}">footer.html</th:block>

    <!-- SockJS 추가 -->
    <!--<script src="https://cdn.jsdelivr.net/npm/sockjs-client@1/dist/sockjs.min.js"></script>-->

    <!-- main.js 추가 -->
    <script th:src="@{/js/main.js}"></script>

</body>
</html>


<link rel="stylesheet" th:href="@{/css/main-style.css}">
<!-- 최상위 경로: static -> 안적고 쓴다, th:ref ->동적으로 주소변경 가능, @{ } -> 경로적을때 -->

<!-- 알림관련 전역 변수:2025/09/18 -->
<script th:inline="javascript">
    // 현재 접속한 클라이언트가 로그인 상태인지 확인하는 변수
    // -> 알림은 로그인한 회원만 받을 수 있다!

    const notificationLoginCheck = /*[[${session.loginMember} ? true : false]]*/ false;

    // 알림을 보낸 회원의 프로필 이미지가 없을 경우 사용할 기본 이미지
    // #{ } : user.default.image 있는지 체크해서 있으면 쓰고, 없으면 기본이미지
    // -> messages.properties에서 얻어온 값
    const notificationDefaultImage = /*[[#{user.default.image}]]*/ '기본이미지';


</script>


<script th:src="@{/js/header.js}"></script>  <!-- by jhsSam -->
<!-- <script th:src="@{/js/autocomplete.js}"></script> -->  <!-- by yyp -->

<!-- static 폴더 제외하고 경로 작성, @{url}표기를 적용하는 속성(href, src, action) -->

<!-- font awesome 라이브러리 추가 + key 등록 -->
<script th:src="@{https://kit.fontawesome.com/f7459b8054.js}" crossorigin="anonymous"></script>



<header>
    <section>
        <!-- 클릭 시 메인 페이지로 이동하는 로고 -->
        <!--   <a href="#"> -->
        <a th:href="@{/}">
            <img th:src="@{/images/logo.png}" alt="로고" id="homeLogo">
        </a>
    </section>


    <section>
        <!-- 검색어 입력할 수 있는 요소 배치 -->

        <article class="search-area">

            <!--
                action : 내부 input에 작성된 값을 제출할 경로/주소
                method : 어떤 방식으로 제출할지 지정

                - GET : input태그 값을 주소에 담아서 제출(주소에 보임)
                - POST : input태그 값을 주소에 담지 않고 제출(주소에 안보임)
                        -> HTTP Body에 담아서 제출
            -->
            <!-- <form action="#" method="GET"> -->
            <!-- 항상 공지사항 페이지로 넘어가게 -->
            <!-- <form action="/board/1" method="GET"> -->
            <div class="container-outer">
                <!-- <form th:action="@{/board/search}" method="GET">  모든 게시글 통함 검색해보자 -->
                <form th:action="@{/board/search}" method="GET" onsubmit="return searchCheck()">  <!--모든 게시글 통함 검색해보자 -->

                    <!-- <div class="container-inner"> -->
                        <!-- <div id="inputWraper"> -->
                            <!-- form태그 내 영역 구분 -->
                            <fieldset id="fieldset">

                                <!--
                                    input의 name 속성 == 제출 시 key
                                    input에 입력된 내용 == 제출 시 value

                                    autocomplete="off" : 브라우저 제공 자동완성 off
                                -->
                                <input type="search" name="query" id="query"
                                placeholder="검색어를 입력해주세요."
                                autocomplete="off" th:value="${param.query}" >
                                <!-- autocomplete="off" th:value="${param.query}"  -->


                                <!-- 통합검색시 key값을 all로 해서 기존 하단 검색과 요청주소의 일관성을 유지하는  trick:2025/09/04 -->
                                <input type="hidden" name="key"  value="all" id="key">

                                <!-- 검색 버튼 -->
                                <!-- button type="submit" 이 기본값 -->
                                <button id="searchBtn" class="fa-solid fa-magnifying-glass"></button>

                                <!-- <div class="suggestion-item">testA</div>
                                <div class="suggestion-item">testB</div>
                                <div class="suggestion-item">testC</div>
                                <div class="suggestion-item">testD</div> -->

                            </fieldset>

                        <!-- </div> -->

                        <!-- 통합 검색창 자동 완성, 화면 제작용: 2025/09/05 -->
                        <!-- <div id="suggestions">
                            <div class="suggestion-item">test1</div>
                            <div class="suggestion-item">test2</div>
                            <div class="suggestion-item">test3</div>
                            <div class="suggestion-item">test4</div>
                            <div class="suggestion-item">test5</div>
                            <div class="suggestion-item">test6</div>
                            <div class="suggestion-item">test7</div>
                            <div class="suggestion-item">test8</div>
                            <div class="suggestion-item">test9</div>
                            <div class="suggestion-item">test10</div>
                        </div> -->

                    <!-- </div> -->
                </form>

                <ul id="searchResult" class="close"></ul>


            </div>


        </article>

    </section>

    <!-- 출력 테스트 by span-tag -->
    <!-- th:에서는 session에서  저장된 변수(loginMember)얻어올때 반드시 명시해야한다.  -->
    <!-- <span th:text="${session.loginMember != null}">로그인한 회원의 정보</span> -->

    <section>

        <!-- 알림 영역 -->
        <section class="notification-container" th:if="${session.loginMember}">
            <!-- 알림 버튼 -->
            <button class="notification-btn fa-regular fa-bell" id="my-element">
            <!-- 알림 개수 표시 -->
            <div class="notification-count-area"></div>

            </button>

            <!-- 알림 목록 -->
             <ul class="notification-list">


             </ul>


        </section>

        <section class="header-top-menu">

            <!-- 우축 상단 드롭다운 메뉴  -->

            <!-- 로그인 X -->
            <th:block th:if="${session.loginMember == null}">
                <a th:href="@{/}">메인 페이지</a> | <a th:href="@{/member/login}">로그인</a>
            </th:block>

            <!-- 로그인 O -->
            <!-- th:unless 조건에 if와 같은 조건 작성함. (조건을 자동으로 반대로 바꿈) -->
            <!-- <th:block th:if="${session.loginMember != null}"> -->
            <th:block th:unless="${session.loginMember == null}">
                <label for="headerMenuToggle">
                    <!-- <th:block th:text="${session.loginMember.memberNickname}">로그인한 회원의 닉네임</th:block> -->
                    <!-- [[${session.loginMember}]]   -->
                    [[${session.loginMember.memberNickname}]]
                    <!-- [[...]] th:text="..." 와 같다(html에서 같게 보인다). boot의 EL방식으로 볼수 있다
                        [[...]]  : 누구나 알수 있는 값일때
                        th:text="..." : 유지보수가 중요한데 쓰인다 (b/c 태그안에 설명이 쓰이므로)
                    -->
                    <i class="fa-solid fa-caret-down"></i>
                </label>
            </th:block>

            <input type="checkbox" id="headerMenuToggle">

            <div class="header-menu">
                <a th:href="@{/myPage/info}">내정보</a>
                <a th:href="@{/member/logout}">로그아웃</a>
            </div>


        </section>

    </section>

</header>

<nav>
    <ul>

        <!-- li-tag Sample Data -->
        <!-- <li><a href="#">공지사항</a></li>
        <li><a href="#">자유 게시판</a></li>
        <li><a href="#">질문 게시판</a></li>
        <li><a href="#">FAQ</a></li>
        <li><a href="#">1:1문의</a></li> -->

        <!-- interceptor를 이용해서 조회된 boardTypeList를
             application scope에서 얻어와 출력
        -->

        <!-- 타임리프는 스코프 생략할수 없다. 여기서는 application scope -->
        <!-- 타임리프에서 boardCode설정 방법1(정석) "@{/board/{boardCode}(boardCode=${boardType.BOARD_CODE})}" -->
        <!-- 타임리프에서 boardCode설정 방법2 "|/board/${boardType.BOARD_CODE}|" -->
        <li th:each="boardType : ${application.boardTypeList}">
            <a th:href="@{/board/{boardCode}(boardCode=${boardType.BOARD_CODE})}"
                th:text="${boardType.BOARD_NAME}">게시판 이름</a>

            <!-- <a th:href="|/board/${boardType.BOARD_CODE}|"
                th:text="${boardType.BOARD_NAME}">게시판 이름</a>     -->

        </li>


        <!-- 바뀔일 없으면 이대로 고정으로 박아두어도 된다. -->

        <!-- "boardTypeList"는 interceptor에 의해 application scope에 담겨져 있다 -->

        <!-- <li><a th:href="@{/board/${boardType.BOARD_CODE}}">${boardType.BOARD_NAME}</a></li> -->
        <!-- <li><a th:href="@{/board/${application.boardType.BOARD_CODE}}">${boardType.BOARD_NAME}</a></li> -->


        <!-- 로그인 시 채팅 보여주기, 2025/09/08 for SpringMVC: "/chatting" controller필요-->
        <!-- 로그인 시 채팅 보여주기, 2025/09/17 for SpringBoot-->
        <li th:if="${session.loginMember}">
            <a th:href="@{/chatting}">채팅</a>
        </li>


    </ul>
</nav>

<!-- 2025/09/06 숙제 -->
<!-- <script th:src="@{/js/autocomplete.js}"></script> -->
<!-- <script th:src="@{/js/header.js}"></script> -->



<footer>
    <p>Copyright &copy; JR Computer Academy 903 class</p>

    <article>
        <a th:href="@{#}">프로젝트 소개</a>
        <span>|</span>
        <a th:href="@{#}">이용약관</a>
        <span>|</span>
        <a th:href="@{#}">개인정보처리방침</a>
        <span>|</span>
        <a th:href="@{#}">고객센터</a>
    </article>
</footer>


<!-- 알림창 띄우기 -->
<!-- javascript 영역에서 타임리프 해석/적용 -->
<!-- th:inline="javascript": 자바스크립트 안에서 Thymeleaf쓰겠다 -->
<script th:inline="javascript">

    /* Natural Template : Thymeleaf에서 HTML 파일을 브라우저로 바로 열어도
                          정상적인 HTML처럼 보이고 작동함   */

    const message = /*[[${message}]]*/ "전달 받은 message";
    // 타임리프 해석   값(자료형 알아서 해석)  사라짐(설명)
    //                Natural Template

    if(message != null) alert(message); // message12가 없으면 null값


</script>


 3. 끝으로 첨부한 spring boot controller 로직을 FastAPI에 맞게 바꿔주고,  이번 단계에서 지금까지 네가 바꿔준 signUp, login의 실행을 확인할 수 있도록 Dockerfile & docker-compose.yml을 작성해서 실제 동착을 테스트/확인하는 절차도 자세히 알려줘.

 package com.devlog.project.member.controller;

import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.support.SessionStatus;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.devlog.project.member.model.dto.MemberLoginResponseDTO;
import com.devlog.project.member.model.dto.MemberProfileDTO;
import com.devlog.project.member.model.dto.MemberSignUpRequestDTO;
import com.devlog.project.member.model.security.CustomUserDetails;
import com.devlog.project.member.model.service.MemberProfileService;
import com.devlog.project.member.model.service.MemberService;
import com.devlog.project.member.model.service.MemberService2;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Controller
@RequestMapping("/member")
@RequiredArgsConstructor
public class MemberController {

	private final MemberService memberService; //
	private final MemberService2 service; //
	private final MemberProfileService profileService;

	private final AuthenticationManager authenticationManager; // spring-security

	// -------------------------- [ 로그인 ]
	// 로그인 페이지(전용 화면) 이동
	@GetMapping("/login")
	public String login(HttpServletRequest request, Model model) {

		// 쿠키 설정
	    Cookie[] cookies = request.getCookies();
	    if (cookies != null) {
	        for (Cookie c : cookies) {
	            if ("saveId".equals(c.getName())) {
	                model.addAttribute("cookie", Map.of("saveId", Map.of("value", c.getValue())));
	            }
	        }
	    }

	    return "member/login";
	}


	// 로그인 요청처리
    @PostMapping("/login")
    @ResponseBody
    public ResponseEntity<?> login(
            @RequestParam("memberEmail") String memberEmail,
            @RequestParam("memberPw") String memberPw,
            /////
            @RequestParam(value="saveId", required=false) String saveId,
			HttpServletResponse resp,
			HttpServletRequest request,
			SessionStatus status   // @SessionAttributes 기반 old loginMember 제거용, placeholder
    ) {

    	try {
	        // 인증 토큰 생성
	        UsernamePasswordAuthenticationToken authToken =
	                new UsernamePasswordAuthenticationToken(memberEmail, memberPw);


	        // 인증 시도 (여기서 Security가 모든 검증 수행) -> 실패시 인증실패 exception발생
	        Authentication authentication =
	                authenticationManager.authenticate(authToken);

	        // 인증 성공 → SecurityContext에 저장
	        SecurityContextHolder.getContext().setAuthentication(authentication);

	        // 인증된 사용자 정보 꺼내기 (spring-security가 Member 엔티티에서 꺼내오는 회원정보)
	        CustomUserDetails userDetails =
	                (CustomUserDetails) authentication.getPrincipal();
	        System.out.println(saveId);
	        System.out.println("===== 인증 성공 =====");
	        System.out.println("memberNo: " + userDetails.getMember().getMemberNo());
	        System.out.println("memberEmail: " + userDetails.getMember().getMemberEmail());
	        System.out.println("memberNickname: " + userDetails.getMember().getMemberNickname());
	        System.out.println("authorities: " + userDetails.getAuthorities()); // ?
	        System.out.println("profileImg;: " + userDetails.getMember().getProfileImg());
	        System.out.println("====================");

	        // ------------------------------------------------
	        // 응답 DTO 생성: 서비스에서 처리
	        MemberLoginResponseDTO response =
	                memberService.toLoginResponse( // toLoginResponse
	                    userDetails.getMember(),
	                    authentication.getAuthorities()
	                );

	        // 탈퇴 회원 체크
	        if ("Y".equals(response.getMemberDelFl())) {
	        	SecurityContextHolder.clearContext();
	            throw new BadCredentialsException("탈퇴한 회원입니다.");
	        }

	        System.out.println("##### 응답 DTO (MemberLoginResponseDTO): ");
	        System.out.println(response);

	        // --------------------------------------------------
			// 로그인 성공 시 response DTO에 로그인회원정보 담겨있다
			// 1) 세션에 로그인한 회원 정보 추가

	        // ===== [추가] 하루 1회 로그인 경험치 지급 (쿠키 기반) =====
	        String today = LocalDate.now().toString();
	        String cookieName = "EXP_" + today;
	        Long memberNo = response.getMemberNo();

	        Cookie target = null;

	        if (request.getCookies() != null) {
	            for (Cookie c : request.getCookies()) {
	                if (cookieName.equals(c.getName())) {
	                    target = c;
	                    break;
	                }
	            }
	        }

	        boolean canGain = false;

	        if (target == null) {
	            target = new Cookie(cookieName, "|" + memberNo + "|");
	            canGain = true;
	        } else {
	            String value = target.getValue();
	            if (!value.contains("|" + memberNo + "|")) {
	                target.setValue(value + memberNo + "|");
	                canGain = true;
	            }
	        }

	        if (canGain) {
	            memberService.increaseExp(memberNo, 50);

	            // 자정 만료
	            LocalDateTime now = LocalDateTime.now();
	            LocalDateTime nextMidnight = now.toLocalDate().plusDays(1).atStartOfDay();
	            int secondsUntilMidnight = (int) Duration.between(now, nextMidnight).getSeconds();

	            target.setPath("/");
	            target.setMaxAge(secondsUntilMidnight);
	            resp.addCookie(target);
	        }

	        System.out.println("경험치 이후 ");
	        // ==================================================

	        // 세션 고정 공격 방지 + 이전 사용자 정보 제거
	        HttpSession oldSession = request.getSession(false);
	        if (oldSession != null) {
	            oldSession.invalidate();
	        }

	        // 12-31 YHJ 추가
	        HttpSession newSession = request.getSession(true);
	        newSession.setAttribute("loginMember", response);

	        newSession.setAttribute(
	        		HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY,
	        		SecurityContextHolder.getContext()
	        		);



			// 2) 아이디 저장(쿠키에)
			// 쿠키 생성(K:V로 해당 쿠키에 담을 (로그인멤버의 이메일) 데이터 지정)
			Cookie cookie = new Cookie("saveId", response.getMemberEmail()); // 로그인 성공시
			if(saveId != null) { // 체크 되었을 때
				cookie.setMaxAge(60*60*24*30); // 초 단위; => 한달동안 유지되는 쿠키 생성
			} else { // 체크 않되었을 때
				cookie.setMaxAge(0); // 기존 쿠키 삭제 -> 0초 동안 유지되는 쿠키 생성
			}

			// 클라이언트가 어떤 요청을 할 때 쿠키가 첨부될지 경로(주소)를 지정
			cookie.setPath("/"); // localhost/ 이하의 모든 주소 ex) /, /member/login, /member/logout 등 모든 요청에 쿠키 첨부

			// 응답 객체(HttpServletResponse)을 이용해서 만들어진 쿠키를 클라이언트에게 전달
			resp.addCookie(cookie);

	        return ResponseEntity.ok(response);
    	} catch (BadCredentialsException ex) {
            // 로그인 실패 → 401 Unauthorized + 메시지 전달
            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("message", "아이디 또는 비밀번호가 일치하지 않습니다."));
        } catch (Exception ex) {
            // 기타 서버 오류
            return ResponseEntity
                    .status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("message", "서버 오류가 발생했습니다."));
        }

    }


	@ResponseBody // Postman API test용
    @GetMapping("/loginTest")
    public String loginTest(Authentication authentication) {

        if (authentication == null) {
            System.out.println("###%%%@@@ authentication is null");
        } else {
            System.out.println("###%%%@@@ login user = " + authentication.getName());
        }

        return "ok";
    }


	// -------------------------- [ 로그아웃 ]
	// 로그아웃 요청처리
	// GET - 리다이렉트 방식
	@GetMapping("/logout")
	public String logoutGet(HttpServletRequest request, SessionStatus status) {
		status.setComplete(); // @SessionAttributes 제거
	    logout(request);
	    System.out.println("###%%%@@@ 로그아웃 성공 (GET)");
	    //return "redirect:/member/login"; // 테스트용
	    return "redirect:/"; // 메인페이지와 통합시
	}

	// POST - REST API 방식
	@ResponseBody
	@PostMapping("/logout")
	public ResponseEntity<Map<String, String>> logoutPost(
			HttpServletRequest request
			, SessionStatus status
			) {
		status.setComplete(); // @SessionAttributes 제거
	    logout(request);
	    System.out.println("###%%%@@@ 로그아웃 성공 (POST)");

	    Map<String, String> response = new HashMap<>();
	    response.put("message", "로그아웃 성공");
	    return ResponseEntity.ok(response);
	}

	// 공통 로그아웃 로직
	private void logout(HttpServletRequest request) {
	    HttpSession session = request.getSession(false);
	    if (session != null) {
	        session.invalidate();
	    }
	    SecurityContextHolder.clearContext();
	}



	// -------------------------- [ 회원 가입 ]
	// 회원가입 페이지(전용화면) 이동: GET방식
	@GetMapping("/signUp")
	public String signUp() {

		return "member/signUp";
	}



	// 회원 가입 진행 // 아이디(이메일), 비밀번호, 이름, 닉네임, 전화번호, 경력사항, 이메일 수신동의, 관리자 계정 신청
	@PostMapping("/signUp")
    public String signUp(
    		 @ModelAttribute  MemberSignUpRequestDTO request
    		 , RedirectAttributes ra
    ) {
		log.info("signUp email = {}", request.getMemberEmail());
		log.info("###@@@%%% CONTROLLER DTO = {}", request);

		String path = "redirect:";
		String message = null;
		int result=0; // placeholder

		try { // 회원가입 성공
			service.signUp(request); // MemberService2에서 signUp 처리, signUp 실패시 예외 발생 -> controller에서 성공(1) 실패(0)처리 반환
			result = 1;

			path += "/"; //메인페이지로 (JS에서?)
			message = request.getMemberNickname() + "님의 가입을 환영합니다.\n 로그인 후 서비스를 이용해 주세요.";	 // (JS에서?)
		} catch(Exception e) { // 회원가입 실패
			log.error("회원가입 실패", e);
			result = 0;
			path += "/member/signUp"; //다시 회원가입 페이지로
			message = "서버 오류로 회원 가입에 실패했습니다.\n 잠시후 다시 이용해 주세요.";
		}

		ra.addFlashAttribute("message", message);

		return path;
    }



	// 필수 회원정보 입력 페이지(전용화면) 이동: GET방식
	@GetMapping("/signUpKakao")
	public String signUpKakaoPage() {
	    return "member/signUpKakao"; //  Thymeleaf
	}


	// 필수 회원정보 입력 진행 // 아이디(이메일), 비밀번호, 이름, 닉네임, 전화번호, 경력사항, 이메일 수신동의
	// 카카오 로그인한 유저가 SOCIAL_LOGIN DB에 레코드없을 경우(최초 카카오로그인경우), 회원가입 절차진행
	@PostMapping("/signUpKakao")
    public String signUpKakao(
    		 @ModelAttribute  MemberSignUpRequestDTO request
    		 , RedirectAttributes ra
    		 , HttpSession session
    ) {
		log.info("signUp email = {}", request.getMemberEmail());
		log.info("###@@@%%% CONTROLLER DTO = {}", request);

		String path = "redirect:";
		String message = null;
		int result=0; // placeholder

		try { // 회원가입 성공
			String kakaoId = (String)session.getAttribute("kakaoId");
			MemberLoginResponseDTO loginMemberKakao = service.signUpKakao(request, kakaoId); // MemberService2에서 signUp 처리, signUp 실패시 예외 발생 -> controller에서 성공(1) 실패(0)처리 반환
			session.setAttribute("loginMember", loginMemberKakao);
			result = 1;

			path += "/"; //메인페이지로 (JS에서?)
			message = request.getMemberNickname() + "님, 회원정보를 입력해 주셔서 감사합니다.";	 // (JS에서?)
		} catch(Exception e) { // 회원가입 실패
			log.error("회원가입 실패", e);
			result = 0;
			path += "/member/signUpKakao"; //다시 회원가입 페이지로
			message = "서버 오류로 회원 정보입력에 실패했습니다.\n 잠시후 다시 이용해 주세요.";
		}

		ra.addFlashAttribute("message", message);

		return path;
    }


	@GetMapping("/profile")
	@ResponseBody
	public MemberProfileDTO selectProfile(
			Long memberNo
			) {
		MemberProfileDTO resp = profileService.selectProfile(memberNo);

		if(resp.getProfileImg() == null) {
			resp.setProfileImg("/images/logo.png");
		}


		return resp;
	}


}



package com.devlog.project.member.controller;


import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.SessionAttributes;

import com.devlog.project.member.model.service.EmailServiceJpa;

import lombok.RequiredArgsConstructor;


@Controller
@RequestMapping("/sendEmail")
@SessionAttributes("authKey") // 인증번호를 DB가 아니라 session에 올려서 쓸때 필요.
@RequiredArgsConstructor
public class EmailController {

	private final EmailServiceJpa emailServiceJpa; // Jpa

	@GetMapping("/signUp")
	@ResponseBody
	public int signUp(@RequestParam("email") String email) {
		return emailServiceJpa.signUp(email, "회원 가입") ? 1 :0;
	}


	@GetMapping("/checkAuthKey")
	@ResponseBody
	public int checkAuthKey(@RequestParam Map<String, Object> paramMap){
		return emailServiceJpa.checkAuthKey(paramMap); // DB 조회 (select)
	}

}



package com.devlog.project.member.controller;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.devlog.project.member.model.service.AjaxServiceJpa;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;


@Slf4j
@Controller // 요청과 응답 제어 + bean 등록
@RequiredArgsConstructor
public class AjaxController {

	private final AjaxServiceJpa ajaxServiceJpa; //


	// 이메일 중복 유효성 검사
	@GetMapping("/dupCheck/email")
	@ResponseBody
	public int dupCheckEmail(String email){

		log.info("[ 이메일 중복 유효성 검사 ] email 출력 : {}", email);
		return ajaxServiceJpa.dupCheckEmail(email); // JPA
	}

	// 닉네임 중복 유효성 검사
	@GetMapping(value="/dupCheck/nickname")
	@ResponseBody
	public int dupCheckNickname(String nickname) {
		log.info("[ 닉네임 중복 유효성 검사 ] nickname 출력 : {}", nickname);
		return ajaxServiceJpa.dupCheckNickname(nickname);
	}

	// 관리자 승인 코드 유효성 검사
	@GetMapping(value="/checkCode/adminCode")
	@ResponseBody
	public int checkAdminCode(String adminCode) {
		log.info("[ 관리자 승인코드 유효성 검사 ] adminCode 출력 : {}", adminCode);
		return adminCode.equals("devlog1234")? 1:0;
	}

}


package com.devlog.project.member.model.service;


import java.util.Collection;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.devlog.project.member.model.dto.LevelDTO;
import com.devlog.project.member.model.dto.MemberLoginResponseDTO;
import com.devlog.project.member.model.dto.MemberProfileDTO;
import com.devlog.project.member.model.entity.Level;
import com.devlog.project.member.model.entity.Member;
import com.devlog.project.member.model.repository.LevelRepository;
import com.devlog.project.member.model.repository.MemberRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class MemberService {  // 로그인(login) 서비스 전용

	private final MemberRepository memberRepository;
	private final LevelRepository levelRepository;

    @Transactional(readOnly = true)
    public MemberLoginResponseDTO toLoginResponse(Member member,
                                                  Collection<? extends GrantedAuthority> authorities) {

        Level level = member.getMemberLevel(); // LAZY 초기화 (트랜잭션 안)

        LevelDTO levelDTO = new LevelDTO(
            level.getLevelNo(),
            level.getTitle(),
            level.getRequiredTotalExp()
        );

        String role = authorities.iterator().next().getAuthority();

        return new MemberLoginResponseDTO(
            member.getMemberNo(),
            member.getMemberEmail(),
            member.getMemberNickname(),
            role,
            member.getMemberAdmin(),
            member.getMemberSubscribe(),
            member.getMemberDelFl(),
            member.getMemberCareer(),
            member.getProfileImg(),
            member.getMyInfoIntro(),
            member.getMyInfoGit(),
            member.getMyInfoHomepage(),
            member.getSubscriptionPrice(),
            member.getBeansAmount(),
            member.getCurrentExp(),
            member.getMCreateDate(),
            levelDTO
        );
    }

    // 로그인 시 회원 경험치 증가
    @Transactional
	public void increaseExp(Long memberNo, int exp) {

		Member member = memberRepository.findById(memberNo).orElseThrow();


		member.setCurrentExp(member.getCurrentExp() + exp);

		// 현재 회원 레벨 조회
		Integer previousLevel = member.getMemberLevel().getLevelNo();

		// 현재 회원 레벨
		Level level = member.getMemberLevel();

		System.out.println("이전 레벨 : " + previousLevel);

		Integer currentLevel = levelRepository.findByCurrentLevel(member.getCurrentExp());

		System.out.println("현재 레벨 : " + currentLevel);


		if(previousLevel < currentLevel) {

			Level newLevel = levelRepository.findById(currentLevel).orElseThrow();

			member.setMemberLevel(newLevel);
		}

	}


}


package com.devlog.project.member.model.service;


import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.devlog.project.member.enums.CommonEnums.Status;
import com.devlog.project.member.model.dto.LevelDTO;
import com.devlog.project.member.model.dto.MemberLoginResponseDTO;
import com.devlog.project.member.model.dto.MemberSignUpRequestDTO;
import com.devlog.project.member.model.entity.Level;
import com.devlog.project.member.model.entity.Member;
import com.devlog.project.member.model.entity.SocialLogin;
import com.devlog.project.member.model.repository.KakaoSocialLoginRepository;
import com.devlog.project.member.model.repository.LevelRepository;
import com.devlog.project.member.model.repository.MemberRepository;


@Slf4j
@Service
@RequiredArgsConstructor
@Transactional // 회원가입은 하나의 트랜잭션
public class MemberService2 { // 회원가입(signUp) 서비스 전용

    private final MemberRepository memberRepository;
    private final LevelRepository levelRepository;
    private final PasswordEncoder passwordEncoder;
    //
    private final KakaoSocialLoginRepository kakaoSocialLoginRepository;

    public void signUp(MemberSignUpRequestDTO dto) { // devlog.com 사이트 통한 회원가입 => 이후 로그인 =>서비스 이용

    	log.info("email = {}", dto.getMemberEmail());
    	log.info("pw = {}", dto.getMemberPw());
    	System.out.println(dto);

        // 이메일 중복 체크
        if (memberRepository.existsByMemberEmail(dto.getMemberEmail())) {
            throw new IllegalStateException("이미 사용 중인 이메일입니다.");
        }

        // 기본 레벨 조회 (LV1)
        Level defaultLevel = levelRepository.findById(1)
                .orElseThrow(() -> new IllegalStateException("기본 레벨이 존재하지 않습니다."));

        // Member Entity 생성
        Member member = Member.builder()
                .memberEmail(dto.getMemberEmail())
                .memberPw(passwordEncoder.encode(dto.getMemberPw())) // passwordEncoder	반드시 Service에서
                .memberName(dto.getMemberName())
                .memberNickname(dto.getMemberNickname())
                .memberTel(dto.getMemberTel())
                .memberCareer(dto.getMemberCareer())
                .memberAdmin(dto.getMemberAdmin() != null ? dto.getMemberAdmin() : Status.N) //	null 방어 처리
                .memberSubscribe(dto.getMemberSubscribe() != null ? dto.getMemberSubscribe() : Status.N) //	null 방어 처리
                .memberLevel(defaultLevel) // 기본 Level	클라이언트가 못 건드리게
                .build();

        //  저장
        memberRepository.save(member); // 실패 시 예외 발생
    }

    public MemberLoginResponseDTO signUpKakao(MemberSignUpRequestDTO dto, String kakaoId) { // kakao 로그인 (최초) => devlog.com 사이트 통한 회원가입 => 바로 서비스 이용

    	log.info("email = {}", dto.getMemberEmail());
    	log.info("pw = {}", dto.getMemberPw());
    	System.out.println(dto);

        // 이메일 중복 체크
        if (memberRepository.existsByMemberEmail(dto.getMemberEmail())) {
            throw new IllegalStateException("이미 사용 중인 이메일입니다.");
        }

        // [A] ///////////////////////////////////
        // 기본 레벨 조회 (LV1)
        Level defaultLevel = levelRepository.findById(1)
                .orElseThrow(() -> new IllegalStateException("기본 레벨이 존재하지 않습니다."));

        // Member Entity 생성
        Member member = Member.builder()
                .memberEmail(dto.getMemberEmail())
                .memberPw(passwordEncoder.encode(dto.getMemberPw())) // passwordEncoder	반드시 Service에서
                .memberName(dto.getMemberName())
                .memberNickname(dto.getMemberNickname())
                .memberTel(dto.getMemberTel())
                .memberCareer(dto.getMemberCareer())
                .memberAdmin(dto.getMemberAdmin() != null ? dto.getMemberAdmin() : Status.N) //	null 방어 처리
                .memberSubscribe(dto.getMemberSubscribe() != null ? dto.getMemberSubscribe() : Status.N) //	null 방어 처리
                .memberLevel(defaultLevel) // 기본 Level	클라이언트가 못 건드리게
                .build();

        // MEMBER TABLE 저장
        memberRepository.save(member); // 실패 시 예외 발생 ==> 저장되면 이 member의 memberNo 생성됨

        // [B] ///////////////////////////////////
        // SocialLogin Entity 생성
        //String kakaoId = (String)session.getAttribute("kakaoId");
        log.info("kakaoId = {}", kakaoId);
        SocialLogin socialLogin = SocialLogin.builder()
        		.provider("kakao")
        		.providerId(kakaoId)
        		.memberNo(member)
        		.build();

        // SOCIAL_LOGIN TABLE 저장
        kakaoSocialLoginRepository.save(socialLogin); // 실패 시 예외 발생

        // [C] ///////////////////////////////////
        // MemberLoginResponseDTO 생성해서 반환해 주기
    	// 이제 MemberLoginResponseDTO 만들자 with MemberSignUpRequestDTO dto

        String role =  dto.getMemberAdmin() == Status.N ? "ROLE_USER" : "ROLE_ADMIN";

        //Level level = member.getMemberLevel(); // LAZY 초기화 (트랜잭션 안)
        // 기본 레벨 조회 (LV1): 이거 위에서 했다. 그거 그대로 가져다 쓴다.
        //Level defaultLevel = levelRepository.findById(1)
        //        .orElseThrow(() -> new IllegalStateException("기본 레벨이 존재하지 않습니다."));
        LevelDTO levelDTO = new LevelDTO(
        		defaultLevel.getLevelNo(),
        		defaultLevel.getTitle(),
        		defaultLevel.getRequiredTotalExp()
        );

        // 위에서 member entity 조회하여 memberNo를 포함함 모든 필드 읽어와야 MemberLoginResponseDTO 만들수 있다.
        Member member2 = memberRepository
                .findByMemberEmailAndMemberDelFl(dto.getMemberEmail(), Status.N)
                .orElseThrow(() ->
                        new UsernameNotFoundException("회원이 존재하지 않습니다.") // 바로 위에서 저장한 거라, 이게 발생하면 안됨
                );


        MemberLoginResponseDTO memberKakaoDTO = new MemberLoginResponseDTO(
        		member2.getMemberNo(),
        		member2.getMemberEmail(),
        		member2.getMemberNickname(),
                role,
                member2.getMemberAdmin(),
                member2.getMemberSubscribe(),
                member2.getMemberDelFl(),
                member2.getMemberCareer(),
                member2.getProfileImg(),
                member2.getMyInfoIntro(),
                member2.getMyInfoGit(),
                member2.getMyInfoHomepage(),
                member2.getSubscriptionPrice(),
                member2.getBeansAmount(),
                member2.getCurrentExp(),
                member2.getMCreateDate(),
                levelDTO
                );

        return memberKakaoDTO;
    }


}




package com.devlog.project.member.model.service;

import java.util.Map;
import java.util.Optional;

import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.devlog.project.member.model.entity.Auth;
import com.devlog.project.member.model.repository.EmailRepository;

import jakarta.mail.Message;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service // 비즈니스 로직 처리 + bean 등록
@RequiredArgsConstructor
public class EmailServiceJpa {

    private final EmailRepository emailRepository;
	private final JavaMailSender mailSender;

	private String fromEmail = "yypark.rok@gmail.com"; // 발송자
	private String fromUsername = "수업용프로젝트";

	public String createAuthKey() { // 6자리 난수 생성 함수
		String key = "";
		for(int i=0 ; i< 6 ; i++) { // 6바퀴 돈다

			int sel1 = (int)(Math.random() * 3); // 0:숫자 / 1,2:영어
			              // 0.0 <= Math.random() < 1

			if(sel1 == 0) { // 0:숫자

				int num = (int)(Math.random() * 10); // 0~9
				key += num;

			}else {

				char ch = (char)(Math.random() * 26 + 65); // A~Z

				int sel2 = (int)(Math.random() * 2); // 0:소문자 / 1:대문자

				if(sel2 == 0) { // 0:소문자
					ch = (char)(ch + ('a' - 'A')); // 소문자로 변경
				}

				key += ch;
			}

		}
		return key;
	}


	@Transactional // 이메일 인증은 하나의 트랜잭션(DB 삽입)
	public boolean signUp(String email, String title) { // JPA: SaveOrUpdateAuthKey

		//6자리 난수 인증번호 생성
		String authKey = createAuthKey();

		// 1) DB에 저장
		try {

			// 이메일 중복 체크
			Optional<Auth> optionalAuth = emailRepository.findByEmail(email);
			if (emailRepository.existsByEmail(email)) { // 이미 존재하는 이메일이면 code (=authKey) 업데이트
				Auth authEmail = optionalAuth.get();
				authEmail.setCode(authKey);
				emailRepository.save(authEmail);            //
				log.info("기존 인증번호 업데이트 - email: {}", email);
			} else {
				// 새 Auth Entity 생성
				Auth authEmail= new Auth(authKey, email); // 객체가 완성된상태로 생성되어야 할 때(인증용 엔티티, 상태값 반드시 있어야 하는 경우)
				emailRepository.save(authEmail);
				log.info("새 인증번호 생성 - email: {}", email);
			}


		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("### signUp Exception 발생[ DB저장/수정시]");
			return false;
		}


		// 2) 이메일 발송
		try {
			//인증메일 보내기
			MimeMessage mail = mailSender.createMimeMessage(); // javax.mail.internet.MimeMessage;
			// 제목
			String subject = "[Board Project]"+title+" 인증코드"; //  yypark.rok@gmail.com에서 받는 이메일 제목을 바꿀수 있다
			// 문자 인코딩
			String charset = "UTF-8";
			// 메일 내용
			String mailContent
			= "<p>Board Project "+title+" 인증코드입니다.</p>"
					+ "<h3 style='color:blue'>" + authKey + "</h3>";
			// 송신자(보내는 사람) 지정
			mail.setFrom(new InternetAddress(fromEmail, fromUsername));
			// 수신자(받는사람) 지정
			mail.addRecipient(Message.RecipientType.TO, new InternetAddress(email));
			// 이메일 제목 세팅
			mail.setSubject(subject, charset);
			// 내용 세팅
			mail.setText(mailContent, charset, "html"); //"html" 추가 시 HTML 태그가 해석됨
			mailSender.send(mail);
		} catch (Exception e) {
			e.printStackTrace();
			return false; // JPA
		}

		// 여기 까지 도달했으면, DB저장과 이메일발송 모두 성공
		return true; // JPA
	}


	@Transactional(readOnly = true)
	public int checkAuthKey(Map<String, Object> paramMap) {
		return emailRepository.countByCodeAndEmail((String)paramMap.get("inputKey"), (String)paramMap.get("email"));
	}


}



package com.devlog.project.member.model.service;


import org.springframework.stereotype.Service;

import com.devlog.project.member.model.repository.MemberRepository;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service // 비즈니스 로직 처리 + bean 등록
@RequiredArgsConstructor
public class AjaxServiceJpa {

    private final MemberRepository memberRepository;

    // 이메일 중복 유효성 검사 by ajax
    public int dupCheckEmail(String email) {
    	int result = 0;
    	if (memberRepository.existsByMemberEmail(email)) { // 이미 사용중인 이메일 경우
    		result = 1;
    	}
    	return result;
    }

    // 닉네임 중복 유효성 검사 by ajax
    public int dupCheckNickname(String nickname) {
    	int result = 0;
    	if (memberRepository.existsByMemberNickname(nickname)) { // 이미 사용중인 닉네임 경우
    		result = 1;
    	}
    	return result;
    }

}



#####################################################
#####################################################
#####################################################



친구야.   java version 17 기반 Spring Boot 웹앱을 만들었는데 환경은 spring boot 3.5.7 + sts4 IDE + gradle + jpa-hibernate(회원가입/로그인/카카오 소셜로그인) + myBatis(자유게시판) + oracle database + elasticsearch(docker로 elasticsearch + kibana + logstash) + spring-security 이야. 여러 구성부분이 있는데 내가 담당했던 회원가입, 로그인, 카카오 소셜로그인, 자유게시판(게시글 CRUD + 댓글 CRUD + 좋아요 + 조회수 기능), 그리고 게시글 삽입/수정에서 사용하도록 제작된  spring ai + openAI API 기반 챗봇 기능을 python version 3.10 기반 FastAPI + Oracle + Elasticsearch + Docker Compose 로 완전 동작 가능한 Dockerfile & docker-compose.yml 풀셋으로 porting하고 싶어.
 (FastAPI 백엔드: 인증/인가 (JWT) + 회원관리 (Oracle) + 게시판 CRUD (Oracle) + 검색 API (Elasticsearch) + ORM(SQLAlchemy))
 단계적/순차적으로 옮겨오고 싶은데, 우선 회원가입, 로그인 기능을 FastAPI 기반으로 옮겨왔으면 좋겠어서, 아래 1, 2, 3번으로 이와 관련한 요청내용과 관련화일을 구성해 보았어.
 1. 로그인/회원가입에 필요한 오라클 DB의 해당 테이블은 다음과 같이 ERD에서 정의하고 MEMBER, LEVELS 테이블을 생성하고, 또 그에 맞는 jpa entity들 (Member, Auth)를 아래처럼 생성했는데, 이걸 FastAPI백엔드에 맞게 바꿔줘.

로그인과 회원 가입을위한 front는 첨부한 login.html, login.css, login.js, signUp.html, signUp.css, signUp.js는 spring boot의 thymeleaf를 사용하도록 작성된 건데, 이것도 FastAPI와 native JS 기반 프론트엔드에 맞게 바꿔줘. 그리고 여기서 main.html과 main.css,main.js를 네가 작성해 줬으면 좋겠는데, naviation bar를 기반으로 하는 일반적인 형태의 main으로 작성해 주면서 일단 navigation bar에 메뉴는 자유게시판, 모니터링 대쉬보드, 데이터 분석, ML/DL 모델링의 4 메뉴를 placeholder로 넣어줘. header, footer또한 네가 그에 맞춰 작성해주는데, header에는 앞에서 옮겨온 login 메뉴가 풀다운메뉴로 우측에 위치했으면 좋겠고, 그 옆에는 알림 메뉴가 위치하도록 했으면 좋겠어. main, header, footer는 첨부한 걸 한 예로 참조 해줘.

끝으로 첨부한 spring boot controller 로직을 FastAPI에 맞게 바꿔주고,  이번 단계에서 지금까지 네가 바꿔준 signUp, login의 실행을 확인할 수 있도록 Dockerfile & docker-compose.yml을 작성해서 실제 동착을 테스트/확인하는 절차도 자세히 알려줘.

부탁해!

Show more
5:39 PM
친구야, 정말 큰 프로젝트를 FastAPI로 포팅하는거네! 단계적으로 차근차근 진행해보자. 먼저 회원가입/로그인 기능부터 완벽하게 옮겨볼게.

1단계: FastAPI 백엔드 구조 및 DB 모델 생성
models.py - SQLAlchemy 모델
Code
schemas.py - Pydantic 스키마
Code
auth.py - JWT 인증 유틸리티
Code
database.py - DB 연결 설정
Code
2단계: FastAPI 라우터 구현
member_router.py - 회원 라우터
Code
email_router.py - 이메일 인증 라우터
Code
3단계: 프론트엔드 - Native JS 기반
login.html - 로그인 페이지
Interactive artifact
login.js - 로그인 로직
Code
signup.html - 회원가입 페이지
Interactive artifact
signup.js - 회원가입 로직
Code
이제 메인 페이지와 공통 컴포넌트를 만들어볼게!

index.html - 메인 페이지
Interactive artifact
common.css - 공통 스타일
Code
main.css - 메인 페이지 스타일
Code
common.js - 공통 JavaScript
Code
main.js - 메인 페이지 로직
Code
4단계: FastAPI 메인 애플리케이션 및 Docker 설정
main.py - FastAPI 애플리케이션
Code
requirements.txt - Python 의존성
Code
Dockerfile - FastAPI 컨테이너
Code
docker-compose.yml - 전체 스택
Code
.env.example - 환경 변수 예시
Code
init.sql - DB 초기화 스크립트
Code
마지막으로 실행 가이드를 작성할게!

README.md - 설치 및 실행 가이드
Document
완벽해! 이제 login.css와 signup.css도 추가로 만들어줄게.

login.css - 로그인 페이지 스타일
Code
signup.css - 회원가입 페이지 스타일
Code
완벽해! 이제 프로젝트 전체 디렉토리 구조를 보여주고 마지막으로 빠진 파일들을 추가할게.

프로젝트 디렉토리 구조 및 설정 가이드
Document
완벽해! 친구야, 이제 Spring Boot에서 FastAPI로 회원가입/로그인 기능을 완전히 포팅했어!

📌 완성된 것들 요약:
✅ 백엔드 (FastAPI)
SQLAlchemy 모델 - Member, Level, Auth 엔티티
Pydantic 스키마 - 요청/응답 검증
JWT 인증 - 토큰 기반 인증/인가
회원 라우터 - 회원가입, 로그인, 중복체크
이메일 라우터 - 인증번호 발송/확인
Oracle DB 연결 - cx_Oracle 기반
✅ 프론트엔드 (Native JS)
메인 페이지 - Hero 섹션, 기능 소개, 최근 게시글
로그인 페이지 - 이메일/비밀번호 인증, 쿠키 저장
회원가입 페이지 - 전체 유효성 검사, 이메일 인증
공통 컴포넌트 - 헤더, 네비게이션, 푸터
공통 유틸리티 - API 호출, 인증 체크, 날짜 포맷
✅ 인프라 (Docker)
FastAPI 컨테이너 - Python 3.10 + Oracle Instant Client
Oracle Database - Express Edition 21c
Elasticsearch - 8.11.0 (검색용)
Kibana - 8.11.0 (모니터링용)
Logstash - 8.11.0 (로그 수집용)
🎯 다음 단계 제안:
자유게시판 CRUD - 다음에 포팅할 기능
Elasticsearch 통합 - 게시글 검색 기능
AI 챗봇 - OpenAI API 통합
파일 업로드 - 프로필 이미지, 게시글 첨부파일
혹시 특정 부분에 대해 더 자세한 설명이 필요하거나, 다음 단계(자유게시판)를 바로 시작하고 싶으면 말해줘! 😊






Claude is AI and can make mistakes. Please double-check responses.





