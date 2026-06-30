document.addEventListener('DOMContentLoaded', () => {

    // ── PARSE BACKEND DATA ────────────────────────────────────────────────
    const dataEl = document.getElementById('chart-data');
    let chartData = {};
    try {
        chartData = dataEl ? JSON.parse(dataEl.textContent) : {};
    } catch (e) {
        console.error('Failed to parse chart-data:', e);
    }

    // ── COLOUR PALETTE ────────────────────────────────────────────────────
    const navy    = '#001842';
    const amber   = '#F99D20';
    const pacific = '#00B0C2';
    const green   = '#10b981';
    const red     = '#ef4444';
    const purple  = '#8b5cf6';
    const muted   = '#9ca3af';
    const orange  = '#f97316';

    // ── CHART DEFAULTS ────────────────────────────────────────────────────
    Chart.defaults.font.family      = 'inherit';
    Chart.defaults.color            = '#6b7280';
    Chart.defaults.font.size        = 11;
    Chart.defaults.devicePixelRatio = 4;

    // ── DATA WITH FALLBACKS ───────────────────────────────────────────────
    // Each key maps to a chartData property from the backend.
    // If the backend omits a key (e.g. no data yet), the fallback is used.

    const sessionsByMonth = chartData.sessions_by_month || {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        data:   [24, 29, 33, 30, 38, 42]
    };

    const sessionsByDept = chartData.sessions_by_dept || {
        labels: ['Technology', 'Sales', 'Marketing', 'L&D', 'Operations'],
        data:   [34, 24, 18, 14, 10]
    };

    const attendanceTrend = chartData.attendance_trend || {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        data:   [82, 85, 81, 87, 88, 89]
    };

    const deliverySplit = chartData.delivery_split || {
        labels: ['Face-to-Face', 'Online'],
        data:   [25, 17]
    };

    const attendanceStack = chartData.attendance_stack || {
        labels:   ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        attended: [210, 225, 238, 219, 260, 280],
        absent:   [28, 30, 24, 22, 29, 26],
        na:       [14, 10, 18, 12, 15, 20]
    };

    const attendancePie = chartData.attendance_pie || {
        attended: 1432,
        absent:   159,
        na:       89
    };

    const bookingStatusStack = chartData.booking_status_stack || {
        labels:   ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        completed: [180, 195, 215, 200, 230, 248],
        cancelled: [18, 22, 19, 24, 26, 21],
        rejected:  [8, 6, 10, 7, 9, 11],
        pending:   [12, 10, 14, 11, 16, 18]
    };

    const bookingFunnel = chartData.booking_funnel || [
        { label: 'Completed',        count: 1268, color: green   },
        { label: 'Approved',         count: 112,  color: pacific  },
        { label: 'Pending Approval', count: 81,   color: amber    },
        { label: 'Cancelled',        count: 130,  color: orange   },
        { label: 'Rejected',         count: 51,   color: red      }
    ];

    const fillRateSessions = chartData.fill_rate_sessions || [
        { title: 'Advanced React Patterns', dept: 'Technology', booked: 38, cap: 40 },
        { title: 'Negotiation Masterclass',  dept: 'Sales',       booked: 31, cap: 35 },
        { title: 'Data-Driven Marketing',    dept: 'Marketing',   booked: 27, cap: 30 },
        { title: 'Leadership Essentials',    dept: 'L&D',         booked: 20, cap: 35 },
        { title: 'Intro to Python',          dept: 'Technology',  booked: 14, cap: 30 },
        { title: 'Ops Process Mapping',      dept: 'Operations',  booked: 9,  cap: 25 }
    ];

    const fillRateTrend = chartData.fill_rate_trend || {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        data:   [64, 68, 71, 69, 73, 76]
    };

    const deptAttendanceRate = chartData.dept_attendance_rate || {
        labels: ['Technology', 'Sales', 'Marketing'],
        data: [85, 78, 91]
    };

    // rankings: backend sends top_trainers, bottom_trainers, top_sessions, etc.
    // Structure per item: { name, sub, metric_num, metric_lbl }
    const rankings = chartData.rankings || {
        top_trainers:    [
            { name: 'Sarah Mitchell', sub: '12 sessions delivered', metric_num: '96%', metric_lbl: 'attendance rate' },
            { name: 'Mark Chen',      sub: '10 sessions delivered', metric_num: '91%', metric_lbl: 'attendance rate' },
            { name: 'Priya Nair',     sub: '8 sessions delivered',  metric_num: '85%', metric_lbl: 'attendance rate' }
        ],
        bottom_trainers: [
            { name: 'James Okafor', sub: '3 sessions delivered', metric_num: '58%', metric_lbl: 'attendance rate' },
            { name: 'Elena Rossi',  sub: '4 sessions delivered', metric_num: '63%', metric_lbl: 'attendance rate' },
            { name: 'Tom Barker',   sub: '5 sessions delivered', metric_num: '67%', metric_lbl: 'attendance rate' }
        ],
        top_sessions:    [
            { name: 'Advanced React Patterns', sub: 'Technology · 38 attended', metric_num: '95%', metric_lbl: 'attendance rate' },
            { name: 'Negotiation Masterclass',  sub: 'Sales · 29 attended',      metric_num: '93%', metric_lbl: 'attendance rate' },
            { name: 'Data-Driven Marketing',    sub: 'Marketing · 25 attended',  metric_num: '92%', metric_lbl: 'attendance rate' }
        ],
        bottom_sessions: [
            { name: 'Ops Process Mapping', sub: 'Operations · 6 attended',  metric_num: '60%', metric_lbl: 'attendance rate' },
            { name: 'Intro to Python',     sub: 'Technology · 9 attended',  metric_num: '64%', metric_lbl: 'attendance rate' },
            { name: 'Brand Fundamentals',  sub: 'Marketing · 11 attended',  metric_num: '69%', metric_lbl: 'attendance rate' }
        ],
        top_courses:    [
            { name: 'Software Engineering',   sub: '4 sessions · Technology', metric_num: '142', metric_lbl: 'attended' },
            { name: 'Sales Fundamentals',     sub: '3 sessions · Sales',       metric_num: '98',  metric_lbl: 'attended' },
            { name: 'Leadership Essentials',  sub: '3 sessions · L&D',         metric_num: '84',  metric_lbl: 'attended' }
        ],
        bottom_courses: [
            { name: 'Ops Compliance',   sub: '2 sessions · Operations', metric_num: '19', metric_lbl: 'attended' },
            { name: 'Brand Strategy',   sub: '2 sessions · Marketing',  metric_num: '27', metric_lbl: 'attended' },
            { name: 'Excel Proficiency',sub: '2 sessions · L&D',        metric_num: '31', metric_lbl: 'attended' }
        ],
        top_learners:    [
            { name: 'Aisha Patel',   sub: 'Technology · 9 sessions attended', metric_num: '9', metric_lbl: 'attended' },
            { name: 'Ryan Kowalski', sub: 'Sales · 7 sessions attended',      metric_num: '7', metric_lbl: 'attended' },
            { name: 'Mei-Ling Zhou', sub: 'Marketing · 6 sessions attended',  metric_num: '6', metric_lbl: 'attended' }
        ],
        bottom_learners: [
            { name: 'Greg Hammond',   sub: 'Operations · 0 attended',       metric_num: '0', metric_lbl: 'attended' },
            { name: 'Claire Simmons', sub: 'L&D · 1 session attended',      metric_num: '1', metric_lbl: 'attended' },
            { name: 'Daniel Webb',    sub: 'Sales · 1 session attended',     metric_num: '1', metric_lbl: 'attended' }
        ]
    };

    // ── CHART: SESSIONS BY MONTH ─────────────────────────────────────────
    new Chart(document.getElementById('chartSessions'), {
        type: 'bar',
        data: {
            labels: sessionsByMonth.labels,
            datasets: [{
                data: sessionsByMonth.data,
                backgroundColor: pacific,
                borderRadius: 0,
                maxBarThickness: 36
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { stepSize: 10 } },
                x: { grid: { display: false } }
            }
        }
    });

    // ── CHART: SESSIONS BY DEPARTMENT (doughnut) ─────────────────────────
    new Chart(document.getElementById('chartPie'), {
        type: 'doughnut',
        data: {
            labels: sessionsByDept.labels,
            datasets: [{
                data: sessionsByDept.data,
                backgroundColor: [navy, pacific, amber, green, purple],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, padding: 12 } } },
            cutout: '62%'
        }
    });

    // ── CHART: ATTENDANCE TREND (line) ───────────────────────────────────
    new Chart(document.getElementById('chartAttendance'), {
        type: 'line',
        data: {
            labels: attendanceTrend.labels,
            datasets: [{
                data: attendanceTrend.data,
                borderColor: green,
                backgroundColor: 'rgba(16,185,129,0.08)',
                fill: true,
                tension: 0.35,
                pointRadius: 3,
                pointBackgroundColor: green,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#f1f5f9' } },
                x: { grid: { display: false } }
            }
        }
    });

    // ── CHART: DELIVERY SPLIT (horizontal bar) ───────────────────────────
    // Matches DeliveryType enum: 'Face-to-Face' | 'Online'
    new Chart(document.getElementById('chartDelivery'), {
        type: 'bar',
        data: {
            labels: deliverySplit.labels,
            datasets: [{
                data: deliverySplit.data,
                backgroundColor: [navy, pacific],
                borderRadius: 0,
                maxBarThickness: 50
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { beginAtZero: true, grid: { color: '#f1f5f9' } },
                y: { grid: { display: false } }
            }
        }
    });

    // ── CHART: ATTENDANCE STACK (stacked bar by month) ───────────────────
    // Source: Attendance.AttendanceStatus grouped by month
    new Chart(document.getElementById('chartAttendStack'), {
        type: 'bar',
        data: {
            labels: attendanceStack.labels,
            datasets: [
                { label: 'Attended', data: attendanceStack.attended, backgroundColor: green,  stack: 'a' },
                { label: 'Absent',   data: attendanceStack.absent,   backgroundColor: red,    stack: 'a' },
                { label: 'N/A',      data: attendanceStack.na,       backgroundColor: muted,  stack: 'a' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, padding: 10 } } },
            scales: {
                x: { stacked: true, grid: { display: false } },
                y: { stacked: true, grid: { color: '#f1f5f9' } }
            }
        }
    });

    // ── CHART: ATTENDANCE OVERALL (doughnut) ────────────────────────────
    new Chart(document.getElementById('chartAttendPie'), {
        type: 'doughnut',
        data: {
            labels: ['Attended', 'Absent'],
            datasets: [{
                data: [attendancePie.attended, attendancePie.absent, attendancePie.na],
                backgroundColor: [green, red, muted],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, padding: 12 } } },
            cutout: '60%'
        }
    });

    // ── CHART: BOOKING STATUS STACK ──────────────────────────────────────
    // Source: Bookings.Status grouped by month
    new Chart(document.getElementById('chartBookingStatus'), {
        type: 'bar',
        data: {
            labels: bookingStatusStack.labels,
            datasets: [
                { label: 'Approved',         data: bookingStatusStack.approved,  backgroundColor: pacific, stack: 'b' },
                { label: 'Cancelled',        data: bookingStatusStack.cancelled, backgroundColor: amber,  stack: 'b' },
                { label: 'Completed',        data: bookingStatusStack.completed, backgroundColor: green,  stack: 'b' },
                { label: 'Rejected',         data: bookingStatusStack.rejected,  backgroundColor: red,    stack: 'b' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, padding: 10 } } },
            scales: {
                x: { stacked: true, grid: { display: false } },
                y: { stacked: true, grid: { color: '#f1f5f9' } }
            }
        }
    });

    // ── FUNNEL: BOOKING STATUS ───────────────────────────────────────────
    // Source: Bookings.Status counts + total
    const funnelTotal = bookingFunnel.reduce((sum, d) => sum + d.count, 0);
    const funnelEl    = document.getElementById('funnelList');
    bookingFunnel.forEach(d => {
        const pct = funnelTotal > 0 ? Math.round((d.count / funnelTotal) * 100) : 0;
        funnelEl.innerHTML += `
            <div class="funnel-row">
                <div class="funnel-meta">
                    <span class="funnel-label">${d.label}</span>
                    <span class="funnel-count">${d.count.toLocaleString()} &nbsp;<span style="color:${d.color};font-weight:600">${pct}%</span></span>
                </div>
                <div class="funnel-track"><div class="funnel-fill" style="width:${pct}%;background:${d.color}"></div></div>
            </div>`;
    });

    // ── UTIL LIST: FILL RATE PER SESSION ────────────────────────────────
    // Source: TrainingSessions.Booked / Capacity
    // const utilEl = document.getElementById('utilList');
    // fillRateSessions.forEach(s => {
    //     const pct = s.cap > 0 ? Math.round((s.booked / s.cap) * 100) : 0;
    //     const cls = pct >= 85 ? 'high' : pct >= 60 ? 'warn' : 'low';
    //     utilEl.innerHTML += `
    //         <div class="util-row">
    //             <div class="util-name">
    //                 <div class="util-session-title">${s.title}</div>
    //                 <div class="util-session-sub">${s.dept} &middot; ${s.booked} / ${s.cap} seats</div>
    //             </div>
    //             <div class="util-bar-wrap">
    //                 <div class="util-track"><div class="util-fill ${cls}" style="width:${pct}%"></div></div>
    //             </div>
    //             <div class="util-pct">${pct}%</div>
    //         </div>`;
    // });

    // ── CHART: FILL RATE TREND (line) ────────────────────────────────────
    // new Chart(document.getElementById('chartFillRate'), {
    //     type: 'line',
    //     data: {
    //         labels: fillRateTrend.labels,
    //         datasets: [{
    //             data: fillRateTrend.data,
    //             borderColor: purple,
    //             backgroundColor: 'rgba(139,92,246,0.08)',
    //             fill: true,
    //             tension: 0.35,
    //             pointRadius: 3,
    //             pointBackgroundColor: purple,
    //             borderWidth: 2
    //         }]
    //     },
    //     options: {
    //         responsive: true,
    //         maintainAspectRatio: false,
    //         plugins: { legend: { display: false } },
    //         scales: {
    //             y: { min: 50, max: 100, grid: { color: '#f1f5f9' }, ticks: { callback: v => v + '%' } },
    //             x: { grid: { display: false } }
    //         }
    //     }
    // });

    // ── CHART: DEPT ATTENDED (polar area) ────────────────────────────────
    // Source: Attendance JOIN Users GROUP BY DepartmentId WHERE AttendanceStatus='Attended'
    new Chart(document.getElementById('chartPolar'), {
        type: 'polarArea',
        data: {
            labels: deptAttendanceRate.labels,
            datasets: [{
                data: deptAttendanceRate.data,
                backgroundColor: [
                    'rgba(0,24,66,0.75)',
                    'rgba(0,176,194,0.75)',
                    'rgba(249,157,32,0.75)',
                    'rgba(16,185,129,0.75)',
                    'rgba(139,92,246,0.75)'
                ],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 12, padding: 16, font: { size: 11 } } },
                tooltip: { callbacks: { label: ctx => ' ' + ctx.label + ': ' + ctx.raw + '% attendance rate' } }
            },
            scales: {
                r: {
                    ticks: { stepSize: 2, font: { size: 10 }, color: '#9ca3af', backdropColor: 'transparent' },
                    grid:  { color: '#e5e7eb' }
                }
            }
        }
    });

    // ── RANKINGS: render top/bottom panels from data ─────────────────────
    // const rankCols = [
    //     { id: 'trainers', label: 'Trainers',  topKey: 'top_trainers',  botKey: 'bottom_trainers'  },
    //     { id: 'sessions', label: 'Sessions',  topKey: 'top_sessions',  botKey: 'bottom_sessions'  },
    //     { id: 'courses',  label: 'Courses',   topKey: 'top_courses',   botKey: 'bottom_courses'   },
    //     { id: 'learners', label: 'Learners',  topKey: 'top_learners',  botKey: 'bottom_learners'  }
    // ];

    // const topRankColors = [amber, pacific, navy];

    // function buildRows(items, isTop) {
    //     return items.map((item, i) => {
    //         const rankStyle = isTop
    //             ? `background:${topRankColors[i] || navy}`
    //             : `background:#fca5a5;color:#7f1d1d`;
    //         const rankLabel = isTop ? (i + 1) : '↓';
    //         return `
    //             <div class="top-row">
    //                 <div class="top-rank" style="${rankStyle}">${rankLabel}</div>
    //                 <div class="top-info">
    //                     <div class="top-name">${item.name}</div>
    //                     <div class="top-sub">${item.sub}</div>
    //                 </div>
    //                 <div class="top-metric">
    //                     <div class="top-metric-num">${item.metric_num}</div>
    //                     <div class="top-metric-lbl">${item.metric_lbl}</div>
    //                 </div>
    //             </div>`;
    //     }).join('');
    // }

    // const perfGrid = document.getElementById('perfGrid');
    // rankCols.forEach(col => {
    //     perfGrid.innerHTML += `
    //         <div class="top-card">
    //             <div class="top-card-header">
    //                 <span class="top-card-title">${col.label}</span>
    //                 <span class="top-card-badge top" id="badge-${col.id}">Top</span>
    //             </div>
    //             <div class="top-panel active is-top" id="${col.id}-top">
    //                 ${buildRows(rankings[col.topKey] || [], true)}
    //             </div>
    //             <div class="top-panel is-bottom" id="${col.id}-bottom">
    //                 ${buildRows(rankings[col.botKey] || [], false)}
    //             </div>
    //         </div>`;
    // });

    // ── TOP / BOTTOM TOGGLE ──────────────────────────────────────────────
    // window.setPerfView = function (view, btn) {
    //     document.querySelectorAll('.perf-toggle-btn').forEach(b => b.classList.remove('active'));
    //     btn.classList.add('active');

    //     rankCols.forEach(col => {
    //         document.getElementById(`${col.id}-top`).classList.toggle('active',    view === 'top');
    //         document.getElementById(`${col.id}-bottom`).classList.toggle('active', view === 'bottom');
    //         const badge = document.getElementById(`badge-${col.id}`);
    //         badge.textContent  = view === 'top' ? 'Top' : 'Bottom';
    //         badge.className    = 'top-card-badge ' + (view === 'top' ? 'top' : 'bottom');
    //     });
    // };

});