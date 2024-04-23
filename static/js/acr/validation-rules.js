window.onload = function() {
    var textarea = document.querySelector('#textarea');

    var buttons = document.querySelectorAll('.key');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var text = this.querySelector('span').textContent;

            var cursorPos = textarea.selectionStart;

            var currentValue = textarea.value;
            var newValue = currentValue.substring(0, cursorPos) + text + currentValue.substring(cursorPos);
            textarea.value = newValue;

            textarea.selectionStart = cursorPos + text.length;
            textarea.selectionEnd = cursorPos + text.length;
            this.blur();
        });
    });
}