const loginForm = document.getElementById('login-form');
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

if (loginForm) {

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(loginForm);
        const response = await fetch('/login', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'error') {
            showErrorModal(data.message);
        } else {
            showSuccessModal(data.message);
            document.getElementById('success-modal-close').onclick = () => {
                document.body.classList.remove("modal-open");
                if (data.role === 'learner') window.location.href = '/account';
                else if (data.role === 'trainer') window.location.href = '/attendance_management';
                else if (data.role === 'manager') window.location.href = '/manager_dashboard';
                else if (data.role === 'admin') window.location.href = '/admin_dashboard';
            };
        }

    });

}