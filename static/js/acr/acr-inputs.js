function getElement(id, event, handler) {
    const element = document.getElementById(id);
    if (event && handler) {
        element.addEventListener(event, handler);
    }
    return element;
}

var CHECK_OCCURS_PER_PERSON_INPUT = getElement('CHECK_OCCURS_PER_PERSON', 'input', OCCURS_PER_PERSON_REFRESH_ON_INPUT),
    CHECK_OCCURS_PER_PERSON_LABEL = getElement('CHECK_OCCURS_PER_PERSON_LABEL'),
    DENIED_AND_PENDING_CLAIM_CHECKBOX = getElement('DENIED_AND_PENDING_CLAIM', 'change', APPEND_VALUE),
    DENIED_AND_PENDING_CLAIM_LABEL = getElement('DENIED_AND_PENDING_CLAIM_LABEL'),
    CHECK_OCCURS_PER_PERSON_MULTIPLE = getElement('CHECK_OCCURS_PER_PERSON_Multiple', 'change', OCCURS_PER_PERSON_SET_MULTIPLE),
    CHECK_OCCURS_PER_PERSON_NOTAPPLICABLE = getElement('CHECK_OCCURS_PER_PERSON_NotApplicable', 'change', OCCURS_PER_PERSON_SET_NOT_APPLICABLE),
    OCCURS_PER_PERSON_ORIGINAL_VALUE = CHECK_OCCURS_PER_PERSON_INPUT.value,

    CHECK_OCCURS_PER_CLAIM_INPUT = getElement('CHECK_OCCURS_PER_CLAIM', 'input', OCCURS_PER_CLAIM_REFRESH_ON_INPUT),
    CHECK_OCCURS_PER_CLAIM_LABEL = getElement('CHECK_OCCURS_PER_CLAIM_LABEL'),
    CHECK_OCCURS_PER_CLAIM_MULTIPLE = getElement('CHECK_OCCURS_PER_CLAIM_MULTIPLE', 'change', OCCURS_PER_CLAIM_SET_MULTIPLE),
    CHECK_OCCURS_PER_CLAIM_NOTAPPLICABLE = getElement('CHECK_OCCURS_PER_CLAIM_NOTAPPLICABLE', 'change', OCCURS_PER_CLAIM_SET_NOT_APPLICABLE);

function APPEND_VALUE() {
    CHECK_OCCURS_PER_PERSON_INPUT.value = this.checked ? OCCURS_PER_PERSON_ORIGINAL_VALUE + ' (Including Denied and Pending Claim)' : OCCURS_PER_PERSON_ORIGINAL_VALUE;
}

function OCCURS_PER_PERSON_REFRESH_ON_INPUT() {
    OCCURS_PER_PERSON_ORIGINAL_VALUE = CHECK_OCCURS_PER_PERSON_INPUT.value;
    [CHECK_OCCURS_PER_PERSON_MULTIPLE, CHECK_OCCURS_PER_PERSON_NOTAPPLICABLE, DENIED_AND_PENDING_CLAIM_CHECKBOX].forEach(el => el.checked = false);
    DENIED_AND_PENDING_CLAIM_CHECKBOX.disabled = false;
    setEnabledColor();
}

function OCCURS_PER_PERSON_SET_MULTIPLE() {
    CHECK_OCCURS_PER_PERSON_LABEL.classList.remove('line-through');
    CHECK_OCCURS_PER_PERSON_INPUT.classList.remove('text-gray-300');
    CHECK_OCCURS_PER_PERSON_INPUT.value = 'M';
    disableDAPC();
}

function OCCURS_PER_PERSON_SET_NOT_APPLICABLE() {
    CHECK_OCCURS_PER_PERSON_LABEL.classList.add('line-through');
    CHECK_OCCURS_PER_PERSON_INPUT.classList.add('text-gray-300');
    CHECK_OCCURS_PER_PERSON_INPUT.value = 'N/A';
    disableDAPC();
}

function disableDAPC() {
    DENIED_AND_PENDING_CLAIM_CHECKBOX.checked = false; 
    DENIED_AND_PENDING_CLAIM_CHECKBOX.disabled = true;
    setDisabledColor();
}

function setDisabledColor() {
    DENIED_AND_PENDING_CLAIM_LABEL.classList.replace('text-gray-700', 'text-gray-400');
    CHECK_OCCURS_PER_PERSON_INPUT.classList.replace('border-gray-300', 'border-gray-200');
    DENIED_AND_PENDING_CLAIM_CHECKBOX.classList.replace('cursor-pointer', 'cursor-not-allowed');
}

function setEnabledColor() {
    DENIED_AND_PENDING_CLAIM_LABEL.classList.replace('text-gray-400', 'text-gray-700');
    CHECK_OCCURS_PER_PERSON_INPUT.classList.replace('border-gray-200', 'border-gray-300');
    CHECK_OCCURS_PER_PERSON_INPUT.classList.remove('text-gray-300');
    CHECK_OCCURS_PER_PERSON_LABEL.classList.remove('line-through');
    DENIED_AND_PENDING_CLAIM_CHECKBOX.classList.replace('cursor-not-allowed', 'cursor-pointer');
}

function OCCURS_PER_CLAIM_SET_MULTIPLE() {
    CHECK_OCCURS_PER_CLAIM_LABEL.classList.remove('line-through');
    CHECK_OCCURS_PER_CLAIM_LABEL.classList.remove('text-gray-300');
    CHECK_OCCURS_PER_CLAIM_INPUT.value = 'M';
}

function OCCURS_PER_CLAIM_SET_NOT_APPLICABLE() {
    CHECK_OCCURS_PER_CLAIM_LABEL.classList.add('line-through');
    CHECK_OCCURS_PER_CLAIM_LABEL.classList.add('text-gray-300');
    CHECK_OCCURS_PER_CLAIM_INPUT.value = 'N/A';
}

function OCCURS_PER_CLAIM_REFRESH_ON_INPUT() {
    [CHECK_OCCURS_PER_CLAIM_MULTIPLE, CHECK_OCCURS_PER_CLAIM_NOTAPPLICABLE].forEach(el => el.checked = false);
    CHECK_OCCURS_PER_CLAIM_LABEL.classList.remove('line-through');
    CHECK_OCCURS_PER_CLAIM_LABEL.classList.remove('text-gray-300');
}

// CHECK AGE

var CHECK_AGE = getElement('CHECK_AGE'),
    OPERATOR = getElement('OPERATOR'),
    MINIMUM = getElement('MINIMUM'),
    MINIMUM_Y_D = getElement('MINIMUM_Y_D'),
    MAXIMUM = getElement('MAXIMUM'),
    MAXIMUM_Y_D = getElement('MAXIMUM_Y_D'),
    PREVIEW = getElement('PREVIEW'),
    CHECK_AGE_NOT_APPLICABLE = getElement('CHECK_AGE_NOT_APPLICABLE', 'change', disableAgeInputFields);

function updateCheckAge() {
    var checkAgeValue = OPERATOR.value + MINIMUM.value + MINIMUM_Y_D.value;
    if (MAXIMUM.value) {
        checkAgeValue += "-" + MAXIMUM.value + MAXIMUM_Y_D.value;
    }
    CHECK_AGE.value = checkAgeValue;
    PREVIEW.textContent = "Preview: " + checkAgeValue;
}

[OPERATOR, MINIMUM, MINIMUM_Y_D, MAXIMUM, MAXIMUM_Y_D].forEach(function(element) {
    element.addEventListener('change', updateCheckAge);
    element.addEventListener('input', updateCheckAge);
});

function disableAgeInputFields() {
    if (CHECK_AGE_NOT_APPLICABLE.checked) {
        [OPERATOR, MINIMUM, MINIMUM_Y_D, MAXIMUM, MAXIMUM_Y_D].forEach(function(element) {
            element.disabled = true;
        });
        var CHECK_AGE_VALUE = CHECK_AGE.value = 'N/A';
        PREVIEW.textContent = "Preview: " + CHECK_AGE_VALUE;
    } else {
        [OPERATOR, MINIMUM, MINIMUM_Y_D, MAXIMUM, MAXIMUM_Y_D].forEach(function(element) {
            element.disabled = false;
        });
        PREVIEW.textContent = "Preview: ";;
    }
}
