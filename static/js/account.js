const editProfileForm = document.getElementById('edit-profile-form');
const errorModal = document.getElementById('error-modal-container');
const errorMessage = document.getElementById('error-modal-message');
const errorCloseBtn = document.getElementById('error-modal-close');
const warningModal = document.getElementById('warning-modal-container');
const warningMessage = document.getElementById('warning-modal-message');
const warningCloseBtn = document.getElementById('warning-modal-close');
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

function showWarningModal(message) {
    warningMessage.textContent = message;
    warningModal.classList.add('active');
    document.body.classList.add("modal-open");
}

function hideWarningModal() {
    warningModal.classList.remove('active');
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

if (warningCloseBtn) {
    warningCloseBtn.addEventListener('click', hideWarningModal);
}

if (editProfileForm) {
    editProfileForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(editProfileForm);

        try {
            const response = await fetch(editProfileForm.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.href = '/account';
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}