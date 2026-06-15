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

const bookingForm = document.getElementById('booking-form');
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

if (bookingForm) {

    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(bookingForm);

        try {
            const response = await fetch(bookingForm.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else {
                showSuccessModal(data.message);
                closeModal();
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });

}