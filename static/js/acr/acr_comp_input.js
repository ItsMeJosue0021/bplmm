var DEDUCT_FROM_45DAYS_INPUT = document.getElementById('DEDUCT_FROM_45DAYS_INPUT');
var DEDUCT_FROM_45DAYS_DAYS = document.getElementById('DEDUCT_FROM_45DAYS_DAYS');
var DEDUCT_FROM_45DAYS_NUMBER = document.getElementById('DEDUCT_FROM_45DAYS_NUMBER');
var DEDUCT_FROM_45DAYS_TYPE = document.getElementById('DEDUCT_FROM_45DAYS_TYPE');
var DEDUCT_FROM_45DAYS_CONDITIONAL = document.getElementById('DEDUCT_FROM_45DAYS_CONDITIONAL');
var DEDUCT_FROM_45DAYS_NOTAPPLICABLE = document.getElementById('DEDUCT_FROM_45DAYS_NOTAPPLICABLE');
var initialInputs = document.getElementById('initial-inputs');
var conditionCntr = document.getElementById('condition-cntr');
var conditionInput = conditionCntr.querySelector('input');
var previewSpan = document.getElementById('deduct-45-days-preview');

conditionCntr.style.display = 'none';

var lastChecked = null;

previewSpan.textContent = DEDUCT_FROM_45DAYS_INPUT.value.toUpperCase();

if (DEDUCT_FROM_45DAYS_INPUT.value.toUpperCase().includes('CONDITION')) {
    DEDUCT_FROM_45DAYS_CONDITIONAL.checked = true;
    updateDisplay()
}

function updateInputValue() {
    let value;
    if (DEDUCT_FROM_45DAYS_CONDITIONAL.checked) {
        value = 'CONDITION: ' + conditionInput.value.toUpperCase();
    } else if (DEDUCT_FROM_45DAYS_NOTAPPLICABLE.checked) {
        value = 'N/A';
    } else {
        let type = DEDUCT_FROM_45DAYS_TYPE.value;
        if (DEDUCT_FROM_45DAYS_TYPE.value !== "" && DEDUCT_FROM_45DAYS_NUMBER.value > 1) {
            type += 's';
        }
        value = DEDUCT_FROM_45DAYS_DAYS.value;
        if (DEDUCT_FROM_45DAYS_NUMBER.value) {
            value += ' DAYS PER ' + DEDUCT_FROM_45DAYS_NUMBER.value;
        }
        value += ' ' + type;
        value = value.toUpperCase();
    }
    DEDUCT_FROM_45DAYS_INPUT.value = value;
    previewSpan.textContent = value;
}

function updateDisplay() {
    if (DEDUCT_FROM_45DAYS_CONDITIONAL.checked) {
        initialInputs.style.display = 'none';
        conditionCntr.style.display = 'block';
    } else if (DEDUCT_FROM_45DAYS_NOTAPPLICABLE.checked) {
        DEDUCT_FROM_45DAYS_DAYS.disabled = true;
        DEDUCT_FROM_45DAYS_NUMBER.disabled = true;
        DEDUCT_FROM_45DAYS_TYPE.disabled = true;
        conditionInput.disabled = true;
    } else {
        DEDUCT_FROM_45DAYS_DAYS.disabled = false;
        DEDUCT_FROM_45DAYS_NUMBER.disabled = false;
        DEDUCT_FROM_45DAYS_TYPE.disabled = false;
        conditionInput.disabled = false;
        initialInputs.style.display = 'flex';
        conditionCntr.style.display = 'none';
    }
}

DEDUCT_FROM_45DAYS_CONDITIONAL.addEventListener('click', function() {
    if (lastChecked === this) {
        this.checked = false;
        lastChecked = null;
    } else {
        lastChecked = this;
    }
    updateDisplay();
    updateInputValue();
});

DEDUCT_FROM_45DAYS_NOTAPPLICABLE.addEventListener('click', function() {
    if (lastChecked === this) {
        this.checked = false;
        lastChecked = null;
    } else {
        lastChecked = this;
    }
    updateDisplay();
    updateInputValue();
});

DEDUCT_FROM_45DAYS_DAYS.addEventListener('input', updateInputValue);
DEDUCT_FROM_45DAYS_NUMBER.addEventListener('input', updateInputValue);
DEDUCT_FROM_45DAYS_TYPE.addEventListener('change', updateInputValue);
conditionInput.addEventListener('input', updateInputValue);