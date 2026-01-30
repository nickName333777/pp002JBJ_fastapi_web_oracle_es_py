/**
 * 자유게시판 목록 JavaScript
 */

// 전역 변수
let currentPage = 1;
let currentLimit = 10;
let currentKeyword = '';
let currentSearchType = 'title';
let currentSortBy = 'recent';

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', async () => {
    // 인증 체크
    // if (!isAuthenticated()) {
    if (!isLoggedIn()) {
        alert('로그인이 필요합니다.');
        window.location.href = '/static/login.html';
        return;
    }

    // 헤더/푸터 로드
    //await loadCommonComponents();

    // 이벤트 리스너 등록
    initEventListeners();

    // 게시글 목록 로드
    await loadBoardList();
});

/**
 * 이벤트 리스너 초기화
 */
function initEventListeners() {
    // 검색 버튼
    document.getElementById('searchBtn').addEventListener('click', handleSearch);

    // 검색어 입력 시 엔터
    document.getElementById('searchKeyword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });

    // 정렬 변경
    document.getElementById('sortBy').addEventListener('change', (e) => {
        currentSortBy = e.target.value;
        currentPage = 1;
        loadBoardList();
    });

    // 글쓰기 버튼
    document.getElementById('writeBtn').addEventListener('click', () => {
        window.location.href = '/static/freeboardWrite.html';
    });
}

/**
 * 검색 처리
 */
function handleSearch() {
    currentKeyword = document.getElementById('searchKeyword').value.trim();
    currentSearchType = document.getElementById('searchType').value;
    currentPage = 1;
    loadBoardList();
}

/**
 * 게시글 목록 로드
 */
async function loadBoardList() {
    const boardList = document.getElementById('boardList');
    
    // 로딩 표시
    boardList.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>게시글을 불러오는 중...</p>
        </div>
    `;

    try {
        // API 요청
        const params = new URLSearchParams({
            page: currentPage,
            limit: currentLimit,
            sort_by: currentSortBy
        });

        if (currentKeyword) {
            params.append('keyword', currentKeyword);
            params.append('search_type', currentSearchType);
        }

        const response = await fetchAPI(`/api/board/freeboard/list?${params}`);

        if (!response.ok) {
            throw new Error('게시글 목록을 불러오는데 실패했습니다.');
        }

        const data = await response.json();
        
        // 목록 렌더링
        renderBoardList(data.boards);
        
        // 페이징 렌더링
        renderPagination(data.total, data.page, data.limit, data.total_pages);

    } catch (error) {
        console.error('게시글 목록 로드 오류:', error);
        boardList.innerHTML = `
            <div class="empty-list">
                <p>게시글을 불러오는데 실패했습니다.</p>
                <p>${error.message}</p>
            </div>
        `;
    }
}

/**
 * 게시글 목록 렌더링
 */
function renderBoardList(boards) {
    const boardList = document.getElementById('boardList');

    if (!boards || boards.length === 0) {
        boardList.innerHTML = `
            <div class="empty-list">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <p>게시글이 없습니다.</p>
            </div>
        `;
        return;
    }

    boardList.innerHTML = boards.map(board => `
        <div class="board-item" onclick="goToDetail(${board.board_no})">
            ${board.thumbnail 
                ? `<img src="${board.thumbnail}" alt="썸네일" class="board-thumbnail">`
                : `<div class="board-thumbnail no-image">📄</div>`
            }
            
            <div class="board-content">
                <h3 class="board-title">${escapeHtml(board.board_title)}</h3>
                
                <div class="board-meta">
                    <div class="board-author">
                        ${board.author.profile_img 
                            ? `<img src="${board.author.profile_img}" alt="프로필" class="author-profile">`
                            : `<span>👤</span>`
                        }
                        <span>${escapeHtml(board.author.member_nickname)}</span>
                    </div>
                    <span>·</span>
                    <span>${formatDate(board.b_create_date)}</span>
                </div>

                <div class="board-stats">
                    <div class="stat-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                            <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                        </svg>
                        <span>${board.board_count}</span>
                    </div>
                    <div class="stat-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                        </svg>
                        <span>${board.like_count}</span>
                    </div>
                    <div class="stat-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                        </svg>
                        <span>${board.comment_count}</span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * 페이징 렌더링
 */
function renderPagination(total, currentPage, limit, totalPages) {
    const pagination = document.getElementById('pagination');

    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = '';

    // 이전 버튼
    html += `
        <button class="page-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            ‹
        </button>
    `;

    // 페이지 번호 (최대 10개 표시)
    const startPage = Math.max(1, currentPage - 4);
    const endPage = Math.min(totalPages, startPage + 9);

    for (let i = startPage; i <= endPage; i++) {
        html += `
            <button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">
                ${i}
            </button>
        `;
    }

    // 다음 버튼
    html += `
        <button class="page-btn" onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            ›
        </button>
    `;

    pagination.innerHTML = html;
}

/**
 * 페이지 이동
 */
function goToPage(page) {
    currentPage = page;
    loadBoardList();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * 상세 페이지 이동
 */
function goToDetail(boardNo) {
    window.location.href = `/static/freeboardDetail.html?no=${boardNo}`;
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
    const now = new Date();
    const diff = now - date;

    // 1분 이내
    if (diff < 60000) {
        return '방금 전';
    }
    // 1시간 이내
    if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}분 전`;
    }
    // 24시간 이내
    if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}시간 전`;
    }
    // 7일 이내
    if (diff < 604800000) {
        return `${Math.floor(diff / 86400000)}일 전`;
    }

    // 그 외
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}
