function toggleSession(sessionId) {
    const card = document.getElementById(sessionId);
    card.classList.toggle('open');
}

function togglePast(sessionId) {
    const card = document.getElementById(sessionId);
    card.classList.toggle('open');
}

function markAttendance(btn, type, sessionId, userId) {
    const row = btn.closest('.attendee-row');
    const attendedBtn = row.querySelector('.attendance-btn.attended');
    const absentBtn   = row.querySelector('.attendance-btn.absent');
    const hiddenInput = document.getElementById(`input-${sessionId}-${userId}`);

    const wasActive = btn.classList.contains('active');

    attendedBtn.classList.remove('active');
    absentBtn.classList.remove('active');
    attendedBtn.setAttribute('aria-pressed', 'false');
    absentBtn.setAttribute('aria-pressed', 'false');

    if (!wasActive) {
      btn.classList.add('active');
      if (hiddenInput) hiddenInput.value = type;
    } else {
      if (hiddenInput) hiddenInput.value = '';
    }

    // updateCounter(sessionId);
}

let _commentTarget = null;

function openCommentModal(sessionId, userId, name) {
    _commentTarget = { sessionId, userId };
    const existing = document.getElementById(`comment-input-${sessionId}-${userId}`);
    document.getElementById('comment-modal-textarea').value = existing ? existing.value : '';
    // document.getElementById('comment-modal-textarea').textContent = `${comments}`;
    document.getElementById('comment-modal-name').textContent = `${name}`;
    const modal = document.getElementById('comment-modal');
    modal.removeAttribute('hidden');
    requestAnimationFrame(() => modal.classList.add('open'));
    modal.querySelector('textarea').focus();
}

function closeCommentModal() {
    const modal = document.getElementById('comment-modal');
    modal.classList.remove('open');
    modal.addEventListener('transitionend', () => modal.setAttribute('hidden', ''), { once: true });
    _commentTarget = null;
}

function saveComment() {
    if (!_commentTarget) return;
    const { sessionId, userId } = _commentTarget;
    const text = document.getElementById('comment-modal-textarea').value.trim();
    const input = document.getElementById(`comment-input-${sessionId}-${userId}`);
    if (input) input.value = text;

    const row = document.querySelector(`.attendee-row[data-user="${userId}"]`);
    if (row) {
        const btn = row.querySelector('.comment-btn');
        if (btn) btn.classList.toggle('has-note', text.length > 0);
    }
    closeCommentModal();
}

document.getElementById('comment-modal').addEventListener('click', (e) => {
    if (e.target === this) closeCommentModal();
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeCommentModal();
});


const errorModal = document.getElementById('error-modal-container');
const errorMessage = document.getElementById('error-modal-message');
const errorCloseBtn = document.getElementById('error-modal-close');
const successModal = document.getElementById('success-modal-container');
const successMessage = document.getElementById('success-modal-message');

function showErrorModal(message) {
    errorMessage.textContent = message;
    errorModal.classList.add('active');
    document.body.classList.add("modal-open");
}

function hideErrorModal() {
    errorModal.classList.remove('active');
    document.body.classList.remove("modal-open");
}

function showSuccessModal(message) {
    successMessage.textContent = message;
    successModal.classList.add('active');
    document.body.classList.add("modal-open");
}

if (errorCloseBtn) {
    errorCloseBtn.addEventListener('click', hideErrorModal);
}

document.querySelectorAll('form[id^="attendance-form-"]').forEach(form => {

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        try {

            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    // window.location.href = '/attendance_management';
                }
            }

        } catch (error) {
            console.error(error);
        }
    });

});