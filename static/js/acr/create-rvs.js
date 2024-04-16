const formSections = document.querySelectorAll(".form-section");
const navButtons = document.querySelectorAll(".nav-button");

function hideAllSections() {
    formSections.forEach(section => {
        section.style.display = "none";
    });
}

navButtons.forEach(button => {
    button.addEventListener("click", () => {
        const nextSectionId = button.getAttribute("data-next");
        const backSectionId = button.getAttribute("data-back");

        if (nextSectionId) {
            hideAllSections();
            document.getElementById(nextSectionId).style.display = "block";
        } else if (backSectionId) {
            hideAllSections();
            document.getElementById(backSectionId).style.display = "block";
        }
    });
});
