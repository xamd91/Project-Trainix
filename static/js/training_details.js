const modal     = document.getElementById('booking-modal');
const openBtn   = document.getElementById('open-modal');
const closeBtn  = document.getElementById('close-modal');
const cancelBtn = document.getElementById('cancel-modal');

function openModal()  { modal.classList.add('open');    document.body.style.overflow = 'hidden'; }
function closeModal() { modal.classList.remove('open'); document.body.style.overflow = ''; }

openBtn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
cancelBtn.addEventListener('click', closeModal);
modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });