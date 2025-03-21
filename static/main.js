// 모든 폼 제출 이벤트를 처리하는 함수
function handleFormSubmit(event) {
    event.preventDefault();
    
    // 폼의 종류에 따라 다른 메시지 표시
    let message = '';
    const form = event.target;
    
    if (form.id === 'post_form') {
        message = '게시글을 작성하시겠습니까?';
    } else if (form.action && form.action.includes('/edit')) {
        message = '게시글을 수정하시겠습니까?';
    } else if (form.classList.contains('delete_form')) {
        message = '정말로 이 게시글을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.';
    }

    // 확인 메시지 표시 후 처리
    if (confirm(message)) {
        form.submit();
    }
}

// 페이지 로드 완료 시 이벤트 리스너 등록
document.addEventListener('DOMContentLoaded', function() {
    // 게시글 작성 폼
    const postForm = document.getElementById('post_form');
    if (postForm) {
        postForm.addEventListener('submit', handleFormSubmit);
    }

    // 게시글 수정 폼
    const editForm = document.querySelector('form[action*="/edit"]');
    if (editForm) {
        editForm.addEventListener('submit', handleFormSubmit);
    }

    // 게시글 삭제 폼
    const deleteForms = document.querySelectorAll('.delete_form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
});
