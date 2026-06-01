const phoneInput = document.getElementById('phone')
const countrySelect = document.getElementById('country')
const registerForm = document.getElementById('register-form');
const errorModal = document.getElementById('error-modal-container');
const errorMessage = document.getElementById('error-modal-message');
const errorCloseBtn = document.getElementById('error-modal-close');
const successModal = document.getElementById('success-modal-container');
const successMessage = document.getElementById('success-modal-message');

function allowOnlyLetters(input) {
    input.addEventListener("input", function() {
        this.value = this.value.replace(/[^a-zA-Z\s-]/g, '');
    })
}

allowOnlyLetters(document.getElementById('firstname'));
allowOnlyLetters(document.getElementById('lastname'));

phoneInput.addEventListener("input", () => {
    let digits = phoneInput.value.replace(/\D/g, '')

    try {
        const country = countrySelect.value;
        const number = libphonenumber.parsePhoneNumberFromString(digits, country);

        if (number) {
            phoneInput.value = number.formatNational();
            
            const maxlength = number.nationalNumber.length;
            if (digits.length > maxlength) {
               digits = digits.slice(0, maxlength);
               phoneInput.value = digits;
            }
        } else {
            phoneInput.value = digits;
        }
    } catch {
        phoneInput.value = digits;
    }   
});

countrySelect.addEventListener('change', () => {
    phoneInput.dispatchEvent(new Event("input"));
});

if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const selected = countrySelect.options[countrySelect.selectedIndex];
        const code = selected.dataset.code || '';
        const fullphone = code + phoneInput.value.replace(/\D/g, '');

        const formData = new FormData(registerForm);
        formData.set('phone', fullphone);

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
