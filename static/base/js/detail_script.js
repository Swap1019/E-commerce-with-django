/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
// ajax call on your button click
// Initialization for ES Users
import { Carousel, initMDB } from "mdb-ui-kit";

initMDB({ Carousel });
document.addEventListener("DOMContentLoaded", function () {
    // Get the alert element
    var alertContainer = document.getElementById('alert-container');

    // Get the close button
    var closeButton = document.getElementById('close-alert');

    // Hide the alert after 5 seconds (5000 milliseconds)
    setTimeout(function () {
        alertContainer.style.display = 'none';
    }, 5000);

    // Add event listener to the close button
    closeButton.addEventListener('click', function () {
        // Hide the alert when the close button is clicked
        alertContainer.style.display = 'none';
    });
});