// 공통 JavaScript 유틸리티
// const API_BASE_URL = "http://localhost:8000"; // login.js, signup.js, main.js에서 중복설정 충돌 발생
// const API_BASE_URL = "http://localhost:8880"; // login.js, signup.js, main.js에서 중복설정 충돌 발생
// 전역 설정 객체
window.APP_CONFIG = window.APP_CONFIG || {
    API_BASE_URL: "http://localhost:8880",
    DEBUG: true
};
// 편의를 위한 상수
const API_BASE_URL = window.APP_CONFIG.API_BASE_URL;

console.log("common.js loaded, API_BASE_URL:", API_BASE_URL);


// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
    checkLoginStatus();
    setupLogoutHandler();
});

// 로그인 상태 확인 및 UI 업데이트
function checkLoginStatus() {
    const token = localStorage.getItem('access_token');
    const loginMember = JSON.parse(localStorage.getItem('loginMember') || 'null');
    
    const loginMenu = document.getElementById('loginMenu');
    const userInfo = document.getElementById('userInfo');
    const notificationContainer = document.getElementById('notificationContainer');
    const userNickname = document.getElementById('userNickname');
    
    if (token && loginMember) {
        // 로그인 상태
        if (loginMenu) loginMenu.style.display = 'none';
        if (userInfo) {
            userInfo.style.display = 'block';
            if (userNickname) {
                userNickname.textContent = loginMember.member_nickname;
            }
        }
        if (notificationContainer) {
            notificationContainer.style.display = 'block';
        }
    } else {
        // 로그아웃 상태
        if (loginMenu) loginMenu.style.display = 'flex';
        if (userInfo) userInfo.style.display = 'none';
        if (notificationContainer) {
            notificationContainer.style.display = 'none';
        }
    }
}

// 로그아웃 핸들러 설정
function setupLogoutHandler() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            try {
                const response = await fetch(`${API_BASE_URL}/member/logout`, {
                    method: 'GET',
                    credentials: 'include'
                });
                
                if (response.ok) {
                    // 로컬 스토리지 정리
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('loginMember');
                    
                    alert('로그아웃 되었습니다.');
                    // window.location.href = '/index.html';
                    window.location.href = '/static/index.html';
                }
            } catch (error) {
                console.error('로그아웃 오류:', error);
                // 에러가 발생해도 로컬 데이터는 정리
                localStorage.removeItem('access_token');
                localStorage.removeItem('loginMember');
                // window.location.href = '/index.html';
                window.location.href = '/static/index.html';
            }
        });
    }
}

// API 요청 헬퍼 함수 (JWT 토큰 자동 포함)
async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    if (token) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`
        };
    }
    
    options.credentials = 'include';
    
    const response = await fetch(url, options);
    
    // 401 에러 시 로그인 페이지로 리다이렉트
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('loginMember');
        alert('로그인이 필요합니다.');
        // window.location.href = '/login.html';
        window.location.href = '/static/login.html';
        return null;
    }
    
    return response;
}

// 날짜 포맷팅 함수
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return '방금 전';
    if (diffMins < 60) return `${diffMins}분 전`;
    if (diffHours < 24) return `${diffHours}시간 전`;
    if (diffDays < 7) return `${diffDays}일 전`;
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}

// 쿠키 관련 함수
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires.toUTCString()}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

// 현재 사용자 정보 가져오기
function getCurrentUser() {
    return JSON.parse(localStorage.getItem('loginMember') || 'null');
}

// 로그인 여부 확인
function isLoggedIn() {
    return !!localStorage.getItem('access_token');
}

// 페이지 접근 권한 체크 (로그인 필수 페이지)
function requireLogin() {
    if (!isLoggedIn()) {
        alert('로그인이 필요한 페이지입니다.');
        // window.location.href = '/login.html';
        window.location.href = '/static/login.html';
        return false;
    }
    return true;
}
