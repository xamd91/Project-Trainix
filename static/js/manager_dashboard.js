const overlay = document.getElementById('modal-overlay');
const iconWrap = document.getElementById('modal-icon-wrap');
const title = document.getElementById('modal-title');
const message = document.getElementById('modal-message');
const confirmBtn = document.getElementById('modal-confirm');
const cancelBtn = document.getElementById('modal-cancel');

const ICONS = {
    approve: `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00B0C2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>`,
    reject:  `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`
};

let currentAction = null;
let currentForm = null;

function openModal(action, name, session, form) {
    currentAction = action;
    currentForm = form;

    overlay.className = `modal-overlay ${action}`;

    iconWrap.innerHTML = ICONS[action];

    if (action === 'approve') {
        title.textContent = 'Approve Request';
        message.innerHTML = `Approve <span class="modal-name">${name}</span>'s request for <span class="modal-name">${session}</span>? They will be notified by email.`;
        confirmBtn.textContent = 'Approve';
    } else {
        title.textContent = 'Reject Request';
        message.innerHTML = `Are you sure you want to reject <span class="modal-name">${name}</span>'s request for <span class="modal-name">${session}</span>?`;
        confirmBtn.textContent = 'Reject';
    }

    requestAnimationFrame(() => overlay.classList.add('open'));
    document.addEventListener('keydown', handleKey);
}

function closeModal() {
    overlay.classList.remove('open');
    document.removeEventListener('keydown', handleKey);
}

function handleKey(e) {
    if (e.key === 'Escape') closeModal();
    if (e.key === 'Enter') confirmBtn.click();
}

overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });

confirmBtn.addEventListener('click', () => {
    if (currentForm) {
        currentForm.querySelector('input[name="action"]').value = currentAction;
        currentForm.submit();
    }
    closeModal();
});

cancelBtn.addEventListener('click', ()  => {
    closeModal();
});

document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', function () {
        const action = this.dataset.action;
        const name = this.dataset.name;
        const session = this.dataset.session;
        const form = this.closest('form');

        openModal(
            action,
            name,
            session,
            form
        );
    });
});

document.getElementById('history-chips').addEventListener('click', e => {
    const chip = e.target.closest('.chip'); 
    
    if(!chip) return;
    
    document.querySelectorAll('#history-chips .chip').forEach( c => c
        .classList.remove('active')
    );

    chip.classList.add('active');
    filterHistory();
});

document.getElementById('history-search').addEventListener('input', filterHistory);

function filterHistory() {
    const filter = document.querySelector('#history-chips .chip.active').dataset.filter;
    const search = document.getElementById('history-search').value.toLowerCase();

    document.querySelectorAll('#history-body tr').forEach(row=>{
        const matchStatus = filter === 'all'|| row.dataset.status === filter;
        const matchSearch = !search || row.textContent.toLowerCase().includes(search);

        row.style.display = matchStatus && matchSearch ? '' : 'none';
    });
}