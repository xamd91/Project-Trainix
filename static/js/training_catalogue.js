const customBox = document.getElementById("date-custom");
const dateInput = document.getElementById("date-range-custom");

const filtersButton = document.getElementById("filters-button");
const panel = document.getElementById("filter-panel");

// const filters = document.getElementById("filters");

const dateFilters = document.querySelectorAll(".date-filter");

dateFilters.forEach(filter => {
    filter.addEventListener("change", (e) => {
    
        if (e.target.checked) {
            dateFilters.forEach(other => {
                if (other !== e.target) {
                    other.checked = false;
                }
            });
        }

        if (document.getElementById('date-week').checked) {
            filterState.date = 'week';
        } else if (document.getElementById('date-month').checked) {
            filterState.date = 'month';
        } else if (document.getElementById('date-custom').checked) {
            filterState.date = 'custom';
        } else {
            filterState.date = 'all';
        }

        dateInput.classList.toggle("visible", customBox.checked);
        
        filterState.page = 1;
        filterTrainingCards();
    });
});

document.getElementById('custom-from').addEventListener("change", function () {
    filterState.customFrom = this.value;
    filterTrainingCards();
});

document.getElementById('custom-to').addEventListener("change", function () {
    filterState.customTo = this.value;
    filterTrainingCards();
});

// const deliveryFilters = document.querySelectorAll(".delivery-filter");

// deliveryFilters.forEach(filter => {
//     filter.addEventListener("change", (e) => {
//         if (e.target.checked) {
//             deliveryFilters.forEach(other => {
//                 if (other !== e.target) {
//                     other.checked = false;
//                 }
//             });
//         }
//     });
// });


// const areaFilters = document.querySelectorAll(".area-filter");

// areaFilters.forEach(filter => {
//     filter.addEventListener("change", (e) => {
//         if (e.target.checked) {
//             areaFilters.forEach(other => {
//                 if (other !== e.target) {
//                     other.checked = false;
//                 }
//             });
//         }
//     });
// });



filtersButton.addEventListener("click", () => {
    const open = panel.classList.toggle("open");
    filtersButton.classList.toggle("active", open);
});


const filterState = {
    search: '',
    date: 'all',
    customFrom: '',
    customTo: '',
    delivery: 'all',
    department: 'all',
    page: 1,
    perPage: 9
};

// const cards = document.querySelectorAll('.training-card');
const wrappers = document.querySelectorAll('.training-card-wrapper');

wrappers.forEach((wrapper, i) => {

    const delay = 300 + Math.min(i * 80, 400);

    const inner = wrapper.querySelector('.training-card');
    inner.style.transition = 'none';
    inner.style.opacity = '0';
    inner.style.transform = 'translateY(10px)';

    setTimeout(() => {
        inner.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        inner.style.opacity = '1';
        inner.style.transform = 'translateY(0)';
    }, delay);
});

function applyPagination(filtered) {

    const start = (filterState.page - 1 ) * filterState.perPage;
    const end = start + filterState.perPage;

    wrappers.forEach(wrapper => {
        const card = wrapper.querySelector('.training-card');
        const isInFilteredList = filtered.includes(wrapper);

        if (!isInFilteredList) wrapper.classList.add('is-hidden');
        card.style.opacity = '';
        card.style.transform = '';
    });

    filtered.forEach((wrapper, index) => {
        if (index < start || index >= end) {
            wrapper.classList.add('is-hidden');
            return;
        }

        const card = wrapper.querySelector('.training-card');
        const wasHidden = wrapper.classList.contains('is-hidden');
        wrapper.classList.remove('is-hidden');
        
        if (wasHidden) {
            card.style.transition = 'none';
            card.style.opacity = '0';
            card.style.transform = 'translateY(10px) scale(0.9)';

            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    card.style.transition = 'opacity 0.3s ease, transform 0.3s cubic-bezier(0.34, 1.7, 0.64, 1)';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0) scale(1)';
                });
            });
        }
    });

    updatePaginationControls(filtered.length);
    updateEmptyState(filtered.length === 0 ? 0 : Math.min(filtered.length - (filterState.page - 1) * filterState.perPage, filterState.perPage));

}

function updatePaginationControls(totalFiltered) {

    const totalPages = Math.ceil(totalFiltered / filterState.perPage) || 1;
    const pageInfo = document.getElementById('page-info');
    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');
    
    if (pageInfo) pageInfo.textContent = `Page ${filterState.page} of ${totalPages}`;
    if (prevBtn) prevBtn.disabled = filterState.page === 1;
    if (nextBtn) nextBtn.disabled = filterState.page >= totalPages;

}

function getFilteredWrappers() {
    
    return Array.from(wrappers).filter(wrapper => {

        const title = wrapper.querySelector('.card-title').textContent.toLocaleLowerCase();
        const date = new Date(wrapper.dataset.date);
        const today = new Date();
        const delivery = wrapper.dataset.delivery;
        const department = wrapper.dataset.department;
        const matchesSearch = filterState.search === '' || title.includes(filterState.search);
        
        today.setHours(0, 0, 0, 0);

        let matchesDate = true; 

        if (filterState.date === "week") {
            const endOfWeek = new Date(today);
            endOfWeek.setDate(today.getDate() + 7);

            matchesDate = date >= today && date <= endOfWeek;
        } else if (filterState.date === "month") {
            matchesDate = date.getMonth() === today.getMonth() && date.getFullYear() === today.getFullYear();
        } else if (filterState.date === "cutsom") {
            const from = filterState.customFrom ? new Date(filterState.customFrom) : null;
            const to = filterState.customTo ? new Date(filterState.customTo) : null;

            if (from && date < from) matchesDate = false;
            if (to && date > to) matchesDate = false;
        }

        const matchesDelivery = filterState.delivery === 'all' || delivery === filterState.delivery;
        const matchesDepartment = filterState.department === 'all' || department === filterState.department;
        const shouldShow = matchesSearch && matchesDate && matchesDelivery && matchesDepartment;
        return shouldShow;

    });

}

function filterTrainingCards() {

    const trainingCount = document.getElementById('training-count');
    const filtered = getFilteredWrappers();

    if (trainingCount) trainingCount.textContent = filtered.length;
    applyPagination(filtered);

}

function updateEmptyState(visibleCount) {
    const grid = document.querySelector('.training-grid');
    const existingEmpty = grid.querySelector('.filter-empty-state');

    if (visibleCount === 0) {
        if (!existingEmpty) {
            const emptyState = document.createElement('div');
            emptyState.className = 'filter-empty-state';

            emptyState.style.opacity = '0';
            emptyState.style.transform = 'translateY(10px) scale(0.95)';
            emptyState.style.transition = 'none';
            
            emptyState.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </div>

                    <h3 class="empty-state-title">
                        No sessions found
                    </h3>

                    <p class="empty-state-text">
                        Try adjusting your search or filters
                    </p>
                </div>
            `;
            grid.appendChild(emptyState);

            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    emptyState.style.transition = 'opacity 0.2s ease, transform 0.2s cubic-bezier(0.34, 1.7, 0.64, 1)';
                    emptyState.style.opacity = '1';
                    emptyState.style.transform = 'translateY(0) scale(1)';
                });
            });

        }
    } else {
        if (existingEmpty) existingEmpty.remove();
    }
}

const searchInput = document.getElementById('search-input');
let searchTimeout;

if (searchInput) {
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            filterState.search = this.value.toLowerCase().trim();
            filterState.page = 1;
            filterTrainingCards();
        }, 300);
    });
}

const deliveryFilters = document.querySelectorAll(".delivery-filter");

deliveryFilters.forEach(filter => {
    filter.addEventListener('change', () => {
        const selected = document.querySelector('.delivery-filter:checked');
        filterState.delivery = selected.dataset.delivery;
        filterState.page = 1;
        filterTrainingCards();
    });
});

const departmentFilters = document.querySelectorAll(".department-filter");

departmentFilters.forEach(filter => {
    filter.addEventListener('change', () => {
        const selected = document.querySelector('.department-filter:checked');
        filterState.department = selected.dataset.department;
        filterState.page = 1;
        console.log(filterState.department);
        filterTrainingCards();
    });
});

const prevBtn = document.getElementById('prev-page');
const nextBtn = document.getElementById('next-page');

if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        if (filterState.page > 1) {
            filterState.page--;
            applyPagination(getFilteredWrappers());
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
}

if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        const filtered = getFilteredWrappers();
        const totalPages = Math.ceil(filtered.length / filterState.perPage) || 1;
        if (filterState.page < totalPages) {
            filterState.page++;
            applyPagination(filtered);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
}

const trainingCards = document.querySelectorAll('.training-card');

trainingCards.forEach(card => {
    card.setAttribute('tabindex', '0');

    card.addEventListener('click', function(e) {
        const title = this.querySelector('.card-title').textContent;
        console.log('Clicked session:', title);
    });
});


document.querySelector('.clear-filters-button').addEventListener('click', () => {
    // document.querySelectorAll('.filter-panel input[type=radio]').forEach(cb => cb.checked = false);
    // dateInput.classList.remove('visible');
    filterState.search = '';
    filterState.date = 'all';
    filterState.delivery = 'all';
    filterState.department = 'all';
    filterState.page = 1;

    if (searchInput) {
        searchInput.value = '';
    }

    document.querySelector('.delivery-filter[data-delivery="all"]').checked = true;
    document.querySelector('.department-filter[data-department="all"]').checked = true;

    dateInput.classList.remove('visible');

    document.querySelectorAll(".date-filter").forEach(cb => cb.checked = false);

    document.getElementById("custom-from").value = "";
    document.getElementById("custom-to").value = "";

    filterState.customFrom = "";
    filterState.customTo = "";

    filterTrainingCards();

});

const allWrappers = Array.from(wrappers)
const maxEntryDelay = Math.min((allWrappers.length - 1) * 80, 400) + 400;
setTimeout(() => {
    updatePaginationControls(allWrappers.length);
    allWrappers.forEach((wrapper, i) => {
        if (i >= filterState.perPage) wrapper.classList.add('is-hidden');
    });
    const trainingCount = document.getElementById('training-count');
    if (trainingCount) trainingCount.textContent = allWrappers.length;
}, maxEntryDelay);

// const deliveryFilters = document.querySelectorAll(".delivery-filter");

// deliveryFilters.forEach(filter => {
//     filter.addEventListener('change', () => {
//         const selected = document.querySelector('.delivery-filter:checked');
//         filterState.delivery = selected.dataset.delivery
//         console.log(filterState.delivery);
//     });
// });