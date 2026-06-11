function openEditModal(UserId, firstName, lastName, jobTitle, role, department) {
    document.getElementById('editModal').style.display = 'block';
    document.getElementById('editFirstName').value = firstName;
    document.getElementById('editLastName').value = lastName;
    document.getElementById('editJobTitle').value = jobTitle;
    document.getElementById('editRole').value = role;
    document.getElementById('editDepartment').value = department;

    document.getElementById('editForm').action = "/admin_dashboard/edit_user/" + UserId;
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}