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

const filtertate = {
    search: '',
    date: 'all',
    delivery: 'all',
    department: 'all'
};

