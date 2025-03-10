document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".form-step");
    const nextBtns = document.querySelectorAll(".next-btn");
    const prevBtns = document.querySelectorAll(".prev-btn");
    const progressBar = document.getElementById("progressBar");
    const profileForm = document.getElementById("profileSetupForm");

    let stepIndex = 0; // Tracks the current step

    // Function to show the current step
    function showStep(index) {
        steps.forEach((step, i) => {
            step.classList.toggle("active", i === index);
        });
        updateProgressBar();
    }

    // Function to update the progress bar
    function updateProgressBar() {
        let progressPercentage = ((stepIndex + 1) / steps.length) * 100;
        progressBar.style.width = `${progressPercentage}%`;
    }

    // Function to validate the current step before proceeding
    function validateStep() {
        const currentStep = steps[stepIndex];
        const inputs = currentStep.querySelectorAll("input, select");
        let isValid = true;

        inputs.forEach((input) => {
            if (input.hasAttribute("required") && input.value.trim() === "") {
                isValid = false;
                input.classList.add("is-invalid");
            } else {
                input.classList.remove("is-invalid");
            }
        });

        return isValid;
    }

    // Handle "Next" button click
    nextBtns.forEach((button) => {
        button.addEventListener("click", () => {
            if (validateStep()) {
                stepIndex++;
                showStep(stepIndex);
            }
        });
    });

    // Handle "Previous" button click
    prevBtns.forEach((button) => {
        button.addEventListener("click", () => {
            stepIndex--;
            showStep(stepIndex);
        });
    });

    // Prevent form submission if validation fails
    profileForm.addEventListener("submit", function (event) {
        if (!validateStep()) {
            event.preventDefault();
            alert("Please fill in all required fields before submitting.");
        }
    });

    // Initially show the first step
    showStep(stepIndex);
});
