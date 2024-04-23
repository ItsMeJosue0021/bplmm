// const formSections = document.querySelectorAll(".form-section");
// const navButtons = document.querySelectorAll(".nav-button");
// const stepperNavButtons = document.querySelectorAll(".stepper-nav-button");

// function hideAllSections() {
//     formSections.forEach(section => {
//         section.style.display = "none";
//     });
// }

// navButtons.forEach(button => {
//     button.addEventListener("click", () => {
//         const nextSectionId = button.getAttribute("data-next");
//         const backSectionId = button.getAttribute("data-back");

//         if (nextSectionId) {
//             hideAllSections();
//             document.getElementById(nextSectionId).style.display = "block";
//         } else if (backSectionId) {
//             hideAllSections();
//             document.getElementById(backSectionId).style.display = "block";
//         }
//     });
// });

// stepperNavButtons.forEach(button => {

//     button.addEventListener("click", () => {
//         const nextSectionId = button.getAttribute("data-next");
//         const backSectionId = button.getAttribute("data-back");

//         if (nextSectionId) {
//             hideAllSections();
//             document.getElementById(nextSectionId).style.display = "block";
//         } else if (backSectionId) {
//             hideAllSections();
//             document.getElementById(backSectionId).style.display = "block";
//         }
//     });
// });


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
        button.style.backgroundColor = 'initial'; // Reset color to initial state
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
            document.querySelector(`.stepper-nav-button[data-next="${nextSectionId}"]`).style.backgroundColor = '#1ED760';
            // document.querySelector(`.stepper-nav-button[data-next="${nextSectionId}"]`).classList.replace("bg-gray-50", "bg-black");
        } else if (backSectionId) {
            hideAllSections();
            resetStepperColors();
            document.getElementById(backSectionId).style.display = "block";
            document.querySelector(`.stepper-nav-button[data-next="${backSectionId}"]`).style.backgroundColor = '#1ED760';
            // document.querySelector(`.stepper-nav-button[data-next="${nextSectionId}"]`).classList.replace("bg-gray-50", "bg-black");
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
            this.style.backgroundColor = '#1ED760';
            // this.classList.replace("bg-gray-50", "bg-black");
        } else if (backSectionId) {
            hideAllSections();
            resetStepperColors();
            document.getElementById(backSectionId).style.display = "block";
            this.style.backgroundColor = '#1ED760';
            // this.classList.replace("bg-gray-50", "bg-black");
        }
    });
});
