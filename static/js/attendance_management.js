function toggleSession(sessionId) {
    const card = document.getElementById(sessionId);
    card.classList.toggle('open');
}

function markAttendance(btn, type, sessionId, userId) {
  const row = btn.closest('.attendee-row');
  const attendedBtn = row.querySelector('.attendance-btn.attended');
  const absentBtn   = row.querySelector('.attendance-btn.absent');
  const hiddenInput = document.getElementById(`input-${sessionId}-${userId}`);

  const wasActive = btn.classList.contains('active');

  attendedBtn.classList.remove('active');
  absentBtn.classList.remove('active');
  attendedBtn.setAttribute('aria-pressed', 'false');
  absentBtn.setAttribute('aria-pressed', 'false');

  if (!wasActive) {
    btn.classList.add('active');
    if (hiddenInput) hiddenInput.value = type;
  } else {
    if (hiddenInput) hiddenInput.value = '';
  }

  updateCounter(sessionId);
}