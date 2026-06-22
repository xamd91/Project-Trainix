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
    'cancel-session-modal'
);

const closeDepartmentModal = setupModal(
    'add-department-modal',
    'open-department-modal',
    'close-department-modal',
    'cancel-department-modal'
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
    'cancel-edit-session-modal'
);

const closeEditDepartmentModal = setupModal(
    'edit-department-modal',
    null,
    'close-edit-department-modal',
    'cancel-edit-department-modal'
);

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

    editSessionForm.action = `/update-session/${id}`;

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

const editDepartmentForm = document.getElementById('edit-department-form');

function openEditDepartment(btn) {
    const id = btn.dataset.id;
    const name = btn.dataset.name;
    const manager = btn.dataset.manager;

    editUserForm.action = `/update-department/${id}`;

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