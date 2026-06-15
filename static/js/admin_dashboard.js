function openUsersEditModal(UserId, firstName, lastName, jobTitle, role, department) {
    document.getElementById('editUserModal').style.display = 'block';
    document.getElementById('editFirstName').value = firstName;
    document.getElementById('editLastName').value = lastName;
    document.getElementById('editJobTitle').value = jobTitle;
    document.getElementById('editRole').value = role;
    document.getElementById('editUserDepartment').value = department;

    document.getElementById('editUserForm').action = "/admin_dashboard/edit_user/" + UserId;
}

function closeUsersEditModal() {
    document.getElementById('editUserModal').style.display = 'none';
}

function openSessionsEditModal(SessionId, title, trainer, department) {
    document.getElementById('editSessionsModal').style.display = 'block';
    document.getElementById('editSessionName').value = title;
    document.getElementById('editTrainer').value = trainer;
    document.getElementById('editSessionsDepartment').value = department;

    document.getElementById('editSessionsForm').action = "/admin_dashboard/edit_sessions/" + SessionId;
}

function closeSessionsEditModal() {
    document.getElementById('editSessionsModal').style.display = 'none';
}

function openDepartmentsEditModal(DepartmentId, DepartmentName, manager) {
    document.getElementById('editDepartmentsModal').style.display = 'block';
    document.getElementById('editDepartmentName').value = DepartmentName;
    document.getElementById('editManager').value = manager;

    document.getElementById('editSessionsForm').action = "/admin_dashboard/edit_departments/" + DepartmentId;
}

function closeDepartmentsEditModal() {
    document.getElementById('editDepartmentsModal').style.display = 'none';
}