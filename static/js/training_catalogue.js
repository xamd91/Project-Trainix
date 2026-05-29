const checkbox = document.getElementById("date-custom");
const dateInput = document.getElementById("date-range-custom");

const filtersButton = document.getElementById("filters-button");
const panel = document.getElementById("filter-panel");

// const filters = document.getElementById("filters");

filtersButton.addEventListener("click", () => {
    const open = panel.classList.toggle("open");
    filtersButton.classList.toggle("active", open);
});

checkbox.addEventListener("change", () => {
    dateInput.classList.toggle("visible", checkbox.checked);
});