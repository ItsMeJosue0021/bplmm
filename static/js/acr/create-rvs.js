
const formSections = document.querySelectorAll(".form-section");
const navButtons = document.querySelectorAll(".nav-button");
const stepperNavButtons = document.querySelectorAll(".stepper-nav-button");

function hideAllSections() {
    formSections.forEach(section => {
        section.style.display = "none";
    });
}

function resetStepperColors() {
    stepperNavButtons.forEach(button => {
        button.style.backgroundColor = 'initial';
        button.querySelector('.core').classList.replace('text-primary', 'text-white');
    });
}

navButtons.forEach(button => {
    button.addEventListener("click", function () {
        const nextSectionId = this.getAttribute("data-next");
        const backSectionId = this.getAttribute("data-back");

        if (nextSectionId) {
            hideAllSections();
            resetStepperColors();
            document.getElementById(nextSectionId).style.display = "block";
            document.querySelector(`.stepper-nav-button[data-next="${nextSectionId}"]`).style.backgroundColor = '#ffffff';
            document.querySelector(`.stepper-nav-button[data-next="${nextSectionId}"] .core`).classList.replace('text-white', 'text-primary');
        } else if (backSectionId) {
            hideAllSections();
            resetStepperColors();
            document.getElementById(backSectionId).style.display = "block";
            document.querySelector(`.stepper-nav-button[data-next="${backSectionId}"]`).style.backgroundColor = '#ffffff';
            document.querySelector(`.stepper-nav-button[data-next="${backSectionId}"] .core`).classList.replace('text-white', 'text-primary');
        }
    });
});

stepperNavButtons.forEach(button => {
    button.addEventListener("click", function () {
        const nextSectionId = this.getAttribute("data-next");
        const backSectionId = this.getAttribute("data-back");

        if (nextSectionId) {
            hideAllSections();
            resetStepperColors();
            document.getElementById(nextSectionId).style.display = "block";
            this.style.backgroundColor = '#ffffff';
            this.querySelector('.core').classList.replace('text-white', 'text-primary');
        } else if (backSectionId) {
            hideAllSections();
            resetStepperColors();
            document.getElementById(backSectionId).style.display = "block";
            this.style.backgroundColor = '#ffffff';
            
            this.querySelector('.core').classList.replace('text-white', 'text-primary');
        }
    });
});
