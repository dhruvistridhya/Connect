jQuery(document).ready(function($) {
  tab = $('.tabs h3 a');

  tab.on('click', function(event) {
    event.preventDefault();
    tab.removeClass('active');
    $(this).addClass('active');

    tab_content = $(this).attr('href');
    $('div[id$="tab-content"]').removeClass('active');
    $(tab_content).addClass('active');
  });
});

// function myFunction() {
//     alert('here');
//     $('#solTitle a').click(function(evt) {
//         evt.preventDefault();
//         alert('here in');
//         var divId = 'summary' + $(this).attr('id');

//         document.getElementById(divId).className = '';

//     });
// }