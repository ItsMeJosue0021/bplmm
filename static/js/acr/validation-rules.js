// var textarea = document.querySelector('#textarea');
// var buttons = document.querySelectorAll('.key');
// var cursorPos = 0;

// textarea.addEventListener('blur', function() {
//     cursorPos = textarea.selectionStart;
// });

// buttons.forEach(function(button) {
//     button.addEventListener('click', function() {
//         var text = this.querySelector('span').textContent;

//         var currentValue = textarea.value;
//         var newValue = currentValue.substring(0, cursorPos) + text + currentValue.substring(cursorPos);
//         textarea.value = newValue;

//         cursorPos += text.length;
//         textarea.selectionStart = cursorPos;
//         textarea.selectionEnd = cursorPos;
//         this.blur();
//         textarea.focus();
//     });
// });


var textarea = document.querySelector('#textarea');
var buttons = document.querySelectorAll('.key');

var cursorPos = textarea.value.length;

textarea.addEventListener('input', function() {
    cursorPos = textarea.selectionStart;
});
textarea.addEventListener('click', function() {
    cursorPos = textarea.selectionStart;
});

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        var text = this.querySelector('span').textContent;

        var currentValue = textarea.value;
        var newValue = currentValue.substring(0, cursorPos) + text + currentValue.substring(cursorPos);
        textarea.value = newValue;

        cursorPos += text.length;
        textarea.selectionStart = cursorPos;
        textarea.selectionEnd = cursorPos;
        this.blur();
        textarea.focus();
    });
});

function addRules(button) {
    var text = button.parentElement.querySelector('.rule').textContent;

    var currentValue = textarea.value;
    var newValue = currentValue.substring(0, cursorPos) + text + currentValue.substring(cursorPos);
    textarea.value = newValue;

    cursorPos += text.length;
    textarea.selectionStart = cursorPos;
    textarea.selectionEnd = cursorPos;
    button.blur();
    textarea.focus();
}
    
