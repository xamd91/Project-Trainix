const registerForm = document.getElementById('register-form');
const errorModal = document.getElementById('error-modal-container');
const errorMessage = document.getElementById('error-modal-message');
const errorCloseBtn = document.getElementById('error-modal-close');
const successModal = document.getElementById('success-modal-container');
const successMessage = document.getElementById('success-modal-message');
const icon = document.querySelector('.icon-container');

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

icon.addEventListener("click", () => {
    registerForm.reset();
})

if (registerForm) {

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(registerForm);
        const response = await fetch('/register', {
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
                window.location.href = '/login';
            };
        }
        console.log(data);
    });
}