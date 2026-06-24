const navy = '#001842', amber = '#F99D20', pacific = '#00B0C2', green = '#10b981', muted = '#9ca3af';

Chart.defaults.font.family = 'inherit';
Chart.defaults.color = '#6b7280';
Chart.defaults.font.size = 11;
Chart.defaults.devicePixelRatio = 5.5;

const chartSessions = new Chart(document.getElementById('chartSessions'), {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mar','Apr','May','Jun'],
        datasets: [{
        data: [24, 29, 33, 30, 38, 42],
        backgroundColor: pacific,
        borderRadius: 0,
        maxBarThickness: 36
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
        y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { stepSize: 10 } },
        x: { grid: { display: false } }
        }
    }
});