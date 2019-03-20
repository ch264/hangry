$(document).ready(function() {
  $('.navbar-burger').on('click', function(event) {
    event.preventDefault();
    // console.log('click burger')
    $('.navbar-burger').toggleClass('is-active');
    $('.navbar-menu').toggleClass('is-active');
  });
});