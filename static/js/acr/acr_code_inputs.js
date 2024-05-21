
// CHECK ADDITIONAL CODES

let codes = [];
let codesValue = document.querySelector('#CHECK_ADDITIONAL_CODES').value;
let currentCodesContainer = document.querySelector('.current-additional-codes-container');

updateCodeCntr('.current-additional-codes-container', codes);

function createCodeTemplate(code) {
    return `
        <div class="w-full flex items-center justify-between p-2 rounded-md border border-gray-300 cursor-pointer bg-white bg-opacity-40">
            <span class="text-sm">${code}</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 minus-button">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14" />
            </svg>                        
        </div>`;
}

if (codesValue !== '') {
    codes = codesValue.split(' ');
    document.querySelector('#codes-preview').textContent = codes.join(' ');
    updateCodeCntr('.current-additional-codes-container', codes);
    codes.forEach(code => {
        currentCodesContainer.innerHTML += createCodeTemplate(code);
        removeAdditionalCode()
    });
}

function removeAdditionalCode() {
    currentCodesContainer.querySelectorAll('.minus-button').forEach(mBtn => {
        mBtn.addEventListener('click', function () {
            let codeToRemove = this.parentElement.querySelector('span').textContent;
            codes = codes.filter(c => c !== codeToRemove);
    
            var compiledCodes = document.querySelector('#CHECK_ADDITIONAL_CODES').value = codes.join(' ');
            document.querySelector('#codes-preview').textContent = compiledCodes;
    
            this.parentElement.remove();
            updateCodeCntr('.current-additional-codes-container', codes);
        });
    });
}

function addAdditionalCode(button) {
    let code = button.parentElement.querySelector('.code').textContent;

    if (!codes.includes(code)) {
        codes.push(code);

        var compiledCodes = document.querySelector('#CHECK_ADDITIONAL_CODES').value = codes.join(' ');
        document.querySelector('#codes-preview').textContent = compiledCodes;

        currentCodesContainer.innerHTML += createCodeTemplate(code);

        removeAdditionalCode();
        updateCodeCntr('.current-additional-codes-container', codes);
    } else {
        let errorMessageDiv = document.createElement('div');
        errorMessageDiv.innerHTML = `
            <div class="absolute top-5 right-5 w-fit rounded p-2 bg-red-200 text-red-800">
                <span>This code has already been added.</span>
            </div>`;
        document.querySelector('#additional-code-cntr').appendChild(errorMessageDiv);

        setTimeout(function() {
            errorMessageDiv.remove();
        }, 1500);
    }
}


// CHECK SPC RELATED BEN CODES  

let SPCcodes = [];
let SPCCodesValue = document.querySelector('#CHECK_SPC_RELATED_BEN_CODES').value;
let currentSPCCodesContainer = document.querySelector('.current-spc-codes-container');

updateCodeCntr('.current-spc-codes-container', SPCcodes);

if (SPCCodesValue !== '') {
    SPCcodes = SPCCodesValue.split(' ');
    document.querySelector('#spc-codes-preview').textContent = SPCcodes.join(' ');
    updateCodeCntr('.current-spc-codes-container', SPCcodes);
    SPCcodes.forEach(code => {
        currentSPCCodesContainer.innerHTML += createCodeTemplate(code);
        removeSPCCode();
    });
}

function removeSPCCode() {
    currentSPCCodesContainer.querySelectorAll('.minus-button').forEach(mBtn => {
        mBtn.addEventListener('click', function () {
            let codeToRemove = this.parentElement.querySelector('span').textContent;
            SPCcodes = SPCcodes.filter(c => c !== codeToRemove);

            var compiledCodes = document.querySelector('#CHECK_SPC_RELATED_BEN_CODES').value = SPCcodes.join(' ');
            document.querySelector('#spc-codes-preview').textContent = compiledCodes;

            this.parentElement.remove();

            updateCodeCntr('.current-spc-codes-container', SPCcodes);
        });
    });
}


function addSPCcode(button) {
    let code = button.parentElement.querySelector('.spc-code').textContent;

    if (!SPCcodes.includes(code)) {
        
        SPCcodes.push(code);

        var compiledCodes = document.querySelector('#CHECK_SPC_RELATED_BEN_CODES').value = SPCcodes.join(' ');
        document.querySelector('#spc-codes-preview').textContent = compiledCodes;

        currentSPCCodesContainer.innerHTML += createCodeTemplate(code);

        removeSPCCode();
        updateCodeCntr('.current-spc-codes-container', SPCcodes);
    } else {
        let errorMessageDiv = document.createElement('div');
        errorMessageDiv.innerHTML = `
            <div class="absolute top-5 right-5 w-fit rounded p-2 bg-red-200 text-red-800">
                <span>This code has already been added.</span>
            </div>`;
        document.querySelector('#spc-code-cntr').appendChild(errorMessageDiv);

        setTimeout(function() {
            errorMessageDiv.remove();
        }, 1500);
    }
}


function updateCodeCntr(container, codes) {
    let cntr = document.querySelector(container);

    let noCodeMessage = cntr.querySelector('.no-code-message');
    if (noCodeMessage) {
        noCodeMessage.remove();
    }

    if (codes.length === 0) {
        cntr.innerHTML = `<div class="no-code-message h-full w-full flex items-center justify-center">
                            <span class="text-red-500 text-sm">No Data</span>
                            </div>`;
    } 
}