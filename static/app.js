$(document).ready(function() {
  $('.navbar-burger').on('click', function(event) {
    event.preventDefault();
    // console.log('click burger')
    $('.navbar-burger').toggleClass('is-active');
    $('.navbar-menu').toggleClass('is-active');
  });

  $('.modal-button').on('click', function(event) {
    event.preventDefault();
    console.log('click delete modal');
    $('.modal').toggleClass('is-active');
  });

  $('.modal-close').on('click', function(event) {
    event.preventDefault();
    console.log('click x to close');
    $('.modal').toggleClass('is-active');
  });
});
