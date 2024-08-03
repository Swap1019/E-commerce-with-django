document.addEventListener('DOMContentLoaded', function () {
    const colorSwatches = document.querySelectorAll('.color-swatch');
    const selectedColorInput = document.getElementById('selectedColor');

    colorSwatches.forEach(swatch => {
        swatch.addEventListener('click', function () {
            // Remove selected class from all swatches
            colorSwatches.forEach(s => s.classList.remove('selected'));

            // Add selected class to the clicked swatch
            swatch.classList.add('selected');

            // Update the hidden input with the selected color value
            selectedColorInput.value = swatch.getAttribute('data-color');
        });
    });
});