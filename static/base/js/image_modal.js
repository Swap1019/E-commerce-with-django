document.addEventListener("DOMContentLoaded", function () {
    // Initialize the Bootstrap modal
    var imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
    var modalImage = document.getElementById('modalImage');

    // Add event listener to each carousel image
    var carouselImages = document.querySelectorAll('.carousel-item img');
    carouselImages.forEach(function(img) {
        img.addEventListener('click', function() {
            modalImage.src = img.src; // Set the src of the modal image to the clicked image's src
            imageModal.show(); // Show the modal
        });
    });

    // Optionally handle closing the modal when clicking outside the image
    document.getElementById('imageModal').addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            imageModal.hide();
        }
    });
});