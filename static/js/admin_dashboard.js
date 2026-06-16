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

function openSessionEditModal(SessionId, title, trainer, department) {
    document.getElementById('editSessionModal').style.display = 'block';
    document.getElementById('editSessionName').value = title;
    document.getElementById('editTrainer').value = trainer;
    document.getElementById('editSessionDepartment').value = department;

    document.getElementById('editSessionForm').action = "/admin_dashboard/edit_session/" + SessionId;
}

function closeSessionEditModal() {
    document.getElementById('editSessionModal').style.display = 'none';
}

function openDepartmentEditModal(DepartmentId, DepartmentName, manager) {
    document.getElementById('editDepartmentModal').style.display = 'block';
    document.getElementById('editDepartmentName').value = DepartmentName;
    document.getElementById('editManager').value = manager;

    document.getElementById('editDepartmentForm').action = "/admin_dashboard/edit_department/" + DepartmentId;
}

function closeDepartmentEditModal() {
    document.getElementById('editDepartmentModal').style.display = 'none';
}


function openCreateUserModal() {
    document.getElementById('createUserModal').style.display = 'block';
}

function closeCreateUserModal() {
    document.getElementById('createUserModal').style.display = 'none';
}

function openCreateSessionModal() {
    document.getElementById('createSessionModal').style.display = 'block';
}

function closeCreateSessionModal() {
    document.getElementById('createSessionModal').style.display = 'none';
}
function openCreateDepartmentModal() {
    document.getElementById('createDepartmentModal').style.display = 'block';
}

function closeCreateDepartmentModal() {
    document.getElementById('createDepartmentModal').style.display = 'none';
}