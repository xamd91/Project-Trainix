const customBox = document.getElementById("date-custom");
const dateInput = document.getElementById("date-range-custom");

const filtersButton = document.getElementById("filters-button");
const panel = document.getElementById("filter-panel");

// const filters = document.getElementById("filters");

const dateFilters = document.querySelectorAll(".date-filter");

dateFilters.forEach(filter => {
    filter.addEventListener("change", (e) => {
        if (e.target.checked) {
            // uncheck all others
            dateFilters.forEach(other => {
                if (other !== e.target) {
                    other.checked = false;
                }
            });
        }

        // show/hide custom range only if "custom" is active
        dateInput.classList.toggle("visible", customBox.checked);
    });
});


const deliveryFilters = document.querySelectorAll(".delivery-filter");

deliveryFilters.forEach(filter => {
    filter.addEventListener("change", (e) => {
        if (e.target.checked) {
            deliveryFilters.forEach(other => {
                if (other !== e.target) {
                    other.checked = false;
                }
            });
        }
    });
});


const areaFilters = document.querySelectorAll(".area-filter");

areaFilters.forEach(filter => {
    filter.addEventListener("change", (e) => {
        if (e.target.checked) {
            areaFilters.forEach(other => {
                if (other !== e.target) {
                    other.checked = false;
                }
            });
        }
    });
});



filtersButton.addEventListener("click", () => {
    const open = panel.classList.toggle("open");
    filtersButton.classList.toggle("active", open);
});

document.querySelector('.clear-filters-button').addEventListener('click', () => {
    document.querySelectorAll('.filter-panel input[type=checkbox]').forEach(cb => cb.checked = false);
    dateInput.classList.remove('visible');
});


// filter logic - idk what i'm doing but it will work eventually (maybe...)

const filterState = {
    search: '',
    date: 'all',
    delivery: 'all',
    department: 'all',
    page: 1,
    perPage: 9
};

const cards = document.querySelectorAll('.training-card');
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

function applyPagination(fltered) {

    const start = (filterState.page - 1 ) * filterState.perPage;
    const end = start + filterState.perPage;

    wrappers.forEach(wrapper => {
        const card = wrapper.querySelector('.training-card');
        const isInFilteredList = filtered.includes(wrapper);

        if (!isInFilteredList) wrapper.classList.add('is-hidden');
        card.style.opacity = '';
        card.style.transform = '';
    });

    

}