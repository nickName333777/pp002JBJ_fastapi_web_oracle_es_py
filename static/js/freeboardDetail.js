/**
 * 자유게시판 상세 JavaScript
 */

// 전역 변수
let boardNo = null;
let currentUser = null;
let boardData = null;

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', async () => {
    // 인증 체크
    if (!isAuthenticated()) {
        alert('로그인이 필요합니다.');
        window.location.href = '/static/login.html';
        return;
    }

    // 현재 사용자 정보 가져오기
    currentUser = getCurrentUserInfo();

    // URL에서 게시글 번호 추출
    const urlParams = new URLSearchParams(window.location.search);
    boardNo = urlParams.get('no');

    if (!boardNo) {
        alert('잘못된 접근입니다.');
        window.location.href = '/static/freeboardList.html';
        return;
    }

    // 헤더/푸터 로드
    await loadCommonComponents();

    // 게시글 로드
    await loadBoardDetail();

    // 댓글 로드 (다음 단계에서 구현)
    // await loadComments();
});

/**
 * 게시글 상세 로드
 */
async function loadBoardDetail() {
    const article = document.getElementById('boardArticle');

    // 로딩 표시
    article.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>게시글을 불러오는 중...</p>
        </div>
    `;

    try {
        const response = await fetchAPI(`/api/board/freeboard/${boardNo}`);

        if (!response.ok) {
            throw new Error('게시글을 찾을 수 없습니다.');
        }

        boardData = await response.json();
        renderBoardDetail(boardData);

    } catch (error) {
        console.error('게시글 로드 오류:', error);
        article.innerHTML = `
            <div class="loading">
                <p>게시글을 불러오는데 실패했습니다.</p>
                <p>${error.message}</p>
                <button class="btn-list" onclick="goToList()">목록으로</button>
            </div>
        `;
    }
}

/**
 * 게시글 상세 렌더링
 */
function renderBoardDetail(board) {
    const article = document.getElementById('boardArticle');

    // 작성자인지 확인
    const isAuthor = currentUser && currentUser.memberNo === board.author.member_no;

    article.innerHTML = `
        <div class="article-header">
            <h1 class="article-title">${escapeHtml(board.board_title)}</h1>
            
            <div class="article-meta">
                <div class="author-info">
                    ${board.author.profile_img 
                        ? `<img src="${board.author.profile_img}" alt="프로필" class="author-profile">`
                        : `<div class="author-profile" style="background:#ddd;display:flex;align-items:center;justify-content:center;">👤</div>`
                    }
                    <div class="author-details">
                        <span class="author-name">${escapeHtml(board.author.member_nickname)}</span>
                        <span class="author-level">Level ${board.author.member_level_no}</span>
                    </div>
                </div>

                <div class="article-stats">
                    <div class="stat-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <span>${formatDate(board.b_create_date)}</span>
                    </div>
                    ${board.b_update_date ? `
                        <div class="stat-item">
                            <span>(수정됨)</span>
                        </div>
                    ` : ''}
                    <div class="stat-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                            <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                        </svg>
                        <span>${board.board_count}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="article-content">
            ${escapeHtml(board.board_content)}
        </div>

        ${board.images && board.images.length > 0 ? `
            <div class="article-images">
                ${board.images.map(img => `
                    <div class="image-item">
                        <img src="${img.img_path}" alt="${img.img_orig || '이미지'}">
                    </div>
                `).join('')}
            </div>
        ` : ''}

        <div class="article-actions">
            <button class="btn-like ${board.is_liked ? 'liked' : ''}" onclick="toggleLike()">
                <svg viewBox="0 0 24 24" fill="${board.is_liked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                    <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                </svg>
                <span class="like-count">${board.like_count}</span>
            </button>

            <button class="btn-list" onclick="goToList()">목록</button>

            ${isAuthor ? `
                <button class="btn-edit" onclick="goToEdit()">수정</button>
                <button class="btn-delete" onclick="deleteBoard()">삭제</button>
            ` : ''}
        </div>
    `;

    // 댓글 개수 업데이트
    document.getElementById('commentCount').textContent = board.comment_count;
}

/**
 * 좋아요 토글 (다음 단계에서 구현)
 */
async function toggleLike() {
    alert('좋아요 기능은 다음 단계에서 구현됩니다.');
    // TODO: API 호출
}

/**
 * 목록으로 이동
 */
function goToList() {
    window.location.href = '/static/freeboardList.html';
}

/**
 * 수정 페이지로 이동 (다음 단계에서 구현)
 */
function goToEdit() {
    window.location.href = `/static/freeboardUpdate.html?no=${boardNo}`;
}

/**
 * 게시글 삭제 (다음 단계에서 구현)
 */
async function deleteBoard() {
    if (!confirm('정말 삭제하시겠습니까?')) {
        return;
    }

    alert('게시글 삭제 기능은 다음 단계에서 구현됩니다.');
    // TODO: API 호출
}

/**
 * HTML 이스케이프 (XSS 방지)
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 날짜 포맷팅
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * 현재 사용자 정보 가져오기
 */
function getCurrentUserInfo() {
    const token = localStorage.getItem('accessToken');
    if (!token) return null;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return {
            memberNo: payload.memberNo,
            memberEmail: payload.memberEmail,
            memberNickname: payload.memberNickname
        };
    } catch (error) {
        console.error('토큰 파싱 오류:', error);
        return null;
    }
}
