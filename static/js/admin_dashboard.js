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

function setupModal(modalId, openId, closeId, cancelId, formId) {
    const modal = document.getElementById(modalId);
    const openBtn = document.getElementById(openId);
    const closeBtn = document.getElementById(closeId);
    const cancelBtn = document.getElementById(cancelId);
    const form = document.getElementById(formId);

    const open = () => {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    };

    const close = () => {
        modal.classList.remove('open');
        document.body.style.overflow = '';
        form.reset();
    };

    openBtn?.addEventListener('click', open);
    closeBtn?.addEventListener('click', close);
    cancelBtn?.addEventListener('click', close);

    modal?.addEventListener('click', e => {
        if (e.target === modal) close();
    });

    return close;
}

const closeUserModal = setupModal(
    'add-user-modal',
    'open-user-modal',
    'close-user-modal',
    'cancel-user-modal',
    'add-user-form'
);

const closeSessionModal = setupModal(
    'add-session-modal',
    'open-session-modal',
    'close-session-modal',
    'cancel-session-modal',
    'add-session-form'
);

const closeDepartmentModal = setupModal(
    'add-department-modal',
    'open-department-modal',
    'close-department-modal',
    'cancel-department-modal',
    'add-department-form'
);

const closeEditUserModal = setupModal(
    'edit-user-modal',
    null,
    'close-edit-user-modal',
    'cancel-edit-user-modal',
    'edit-user-form'
);

const closeEditSessionModal = setupModal(
    'edit-session-modal',
    null,
    'close-edit-session-modal',
    'cancel-edit-session-modal',
    'edit-session-form'
);

const closeEditDepartmentModal = setupModal(
    'edit-department-modal',
    null,
    'close-edit-department-modal',
    'cancel-edit-department-modal',
    'edit-department-form'
);

const closeDeleteModal = setupModal(
    'delete-user-modal',
    null,
    null,
    'cancel-delete-modal',
    'delete-user-form'
)

const editUserForm = document.getElementById('edit-user-form');

function openEditUser(btn) {
    const id = btn.dataset.id;
    const firstname = btn.dataset.firstname;
    const lastname = btn.dataset.lastname;
    const email = btn.dataset.email;
    const role = btn.dataset.role;
    const department = btn.dataset.department;
    const job = btn.dataset.job;
    const trainerPerms = btn.dataset.perms;

    editUserForm.action = `/admin_dashboard/edit_user/${id}`;

    document.getElementById('edit-firstname').value = firstname;
    document.getElementById('edit-lastname').value = lastname;
    document.getElementById('edit-email').value = email;
    document.getElementById('edit-role').value = role;
    document.getElementById('edit-department').value = department;
    document.getElementById('edit-job-title').value = job;
    document.getElementById('edit-trainer-perms').value = trainerPerms;

    document.getElementById('edit-user-modal').classList.add('open');
    document.body.style.overflow = 'hidden';
}

document.querySelectorAll('.btn-action.edit.user').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        openEditUser(this);
    });
});

const addUserForm = document.getElementById('add-user-form');

if (addUserForm) {
    addUserForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch (this.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else if (data.status === 'success') {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}


if (editUserForm) {
    editUserForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch (this.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else if (data.status === 'success') {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}


const editSessionForm = document.getElementById('edit-session-form');

function openEditSession(btn) {
    const id = btn.dataset.id;
    const title = btn.dataset.title;
    const course = btn.dataset.course;
    const trainer = btn.dataset.trainer;
    const date = btn.dataset.date;
    const time = btn.dataset.time;
    const location = btn.dataset.location;
    const capacity = btn.dataset.capacity;
    const delivery = btn.dataset.delivery;
    const description = btn.dataset.description;
    const prerequisites = btn.dataset.prerequisites;

    editSessionForm.action = `/admin_dashboard/edit_session/${id}`;

    document.getElementById('edit-title').value = title;
    document.getElementById('edit-course').value = course;
    document.getElementById('edit-trainer').value = trainer;
    document.getElementById('edit-date').value = date;
    document.getElementById('edit-time').value = time;
    document.getElementById('edit-location').value = location;
    document.getElementById('edit-capacity').value = capacity;
    document.getElementById('edit-delivery').value = delivery;
    document.getElementById('edit-description').value = description;
    document.getElementById('edit-prerequisites').value = prerequisites;

    document.getElementById('edit-session-modal').classList.add('open');
    document.body.style.overflow = 'hidden';
}

document.querySelectorAll('.btn-action.edit.session').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        openEditSession(this);
    });
});

const addSessionForm = document.getElementById('add-session-form');

if (addSessionForm) {
    addSessionForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch (this.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else if (data.status === 'success') {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}


if (editSessionForm) {
    editSessionForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch (this.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else if (data.status === 'success') {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}


const editDepartmentForm = document.getElementById('edit-department-form');

function openEditDepartment(btn) {
    const id = btn.dataset.id;
    const name = btn.dataset.name;
    const manager = btn.dataset.manager;

    editDepartmentForm.action = `/admin_dashboard/edit_department/${id}`;

    document.getElementById('edit-department-name').value = name;
    document.getElementById('edit-manager').value = manager;


    document.getElementById('edit-department-modal').classList.add('open');
    document.body.style.overflow = 'hidden';
}

document.querySelectorAll('.btn-action.edit.department').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        openEditDepartment(this);
    });
});

const addDepartmentForm = document.getElementById('add-department-form');

if (addDepartmentForm) {
    addDepartmentForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch (this.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else if (data.status === 'success') {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}


if (editDepartmentForm) {
    editDepartmentForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch (this.action, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'error') {
                showErrorModal(data.message);
            } else if (data.status === 'warning') {
                showWarningModal(data.message);
            } else if (data.status === 'success') {
                showSuccessModal(data.message);
                document.getElementById('success-modal-close').onclick = () => {
                    document.body.classList.remove('modal-open');
                    successModal.classList.remove('active');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.error(error);
        }
    });
}


const deleteUserModal = document.getElementById('delete-user-modal');
const deleteCancelBtn = document.getElementById('delete-cancel-btn');
const deleteUserForm = document.getElementById('delete-user-form');
const deleteUserName = document.getElementById('delete-user-name');

function openDeleteUser(btn) {
    const id = btn.dataset.id;
    const firstname = btn.dataset.firstname;
    const lastname = btn.dataset.lastname;

    deleteUserName.textContent = firstname;

    deleteUserForm.action = `/admin_dashboard/delete_user/${id}`;

    deleteUserModal.classList.add('open');
    document.body.style.overflow = 'hidden';
}

document.querySelectorAll('.btn-action.delete.user').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        openDeleteUser(this);
    });
});