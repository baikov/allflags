/* Project specific Javascript goes here. */
$(document).ready(function () {
    // Copy color
    var cp = document.querySelectorAll('.cp');
    var clipboard = new ClipboardJS(cp);
    clipboard.on('success', function (e) {
        console.log(e);
        console.info('Action:', e.action);
        console.info('Text:', e.text);
        console.info('Trigger:', e.trigger);
        $('#copy').toast('show')
    });

    clipboard.on('error', function (e) {
        console.log(e);
    });

    // Tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    // Dropdown Bootstrap 4 menu
    $('.dropdown-menu a.dropdown-toggle').on('mouseover', function (e) {
        if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
        }
        var $subMenu = $(this).next('.dropdown-menu');
        $subMenu.toggleClass('show');


        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function (e) {
            $('.dropdown-submenu .show').removeClass('show');
        });


        return false;
    });

    // Carousel for historical flags
    $('.history-carousel').slick({
        dots: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        responsive: [
            {
              breakpoint: 1140, // xl
              settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: true,
                dots: true
              }
            },
            {
              breakpoint: 960, // lg
              settings: {
                slidesToShow: 3,
                slidesToScroll: 2
              }
            },
            {
              breakpoint: 720, // md
              settings: {
                slidesToShow: 2,
                slidesToScroll: 1
              }
            },
            {
                breakpoint: 540, // sm
                settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1
                }
              }
            // You can unslick at a given breakpoint now by adding:
            // settings: "unslick"
            // instead of a settings object
          ]
    });
    $('.history-carousel-hor').slick({
        dots: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
    });
});
