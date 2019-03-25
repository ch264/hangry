$(document).ready(function() {
  // Click function to open navbar when hamburger icon is clicked
  $('.navbar-burger').on('click', function(event) {
    event.preventDefault();
    // Toggles 'is-active' class to show or hide navbar
    $('.navbar-burger').toggleClass('is-active');
    $('.navbar-menu').toggleClass('is-active');
  });

  // Click function to open modal when user wants to delete a recipe
  $('.modal-button').on('click', function(event) {
    event.preventDefault();
    $('.modal').toggleClass('is-active');
  });

  // Click function to close delete recipe modal
  $('.modal-close').on('click', function(event) {
    event.preventDefault();
    $('.modal').toggleClass('is-active');
  });
});
