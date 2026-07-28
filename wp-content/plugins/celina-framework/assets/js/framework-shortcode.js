(function($) {
    "use strict";
    var YL_SC = {

        init: function() {
            YL_SC.owlCarousel();
            YL_SC.popupInfo();
            YL_SC.sc_historySlideSlick();
            YL_SC.sc_historySlideCarousel();
            YL_SC.countAppear();
            YL_SC.countProcess();
            YL_SC.sc_video();
            YL_SC.single_product_slick();
        },
        owlCarousel: function() {
            if ($('.owl-carousel[data-owl]').length > 0) {
                $('.owl-carousel[data-owl]').each(function() {
                    var item = $(this).attr('data-owl'),
                        autoplay = $(this).attr('data-autoplay'),
                        rtl = $(this).attr('data-rtl'),
                        duration = $(this).attr('data-duration'),
                        loop = $(this).attr('data-loop'),
                        margin = $(this).attr('data-margin'),
                        nav = $(this).attr('data-nav'),
                        pagination = $(this).attr('data-pagination');
                    var defaults = {
                        // Most important owl features
                        items: item ? parseInt(item) : 1,
                        rtl: rtl ? rtl : false,
                        margin: margin ? parseInt(margin) : 0,
                        nav: nav ? nav : false,
                        loop: loop ? loop : false,
                        autoplay: autoplay ? autoplay : false,
                        autoplayTimeout: duration ? parseInt(duration) : 1000,
                        autoplayHoverPause: true,
                        dots: pagination ? pagination : false,
                        navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"],
                        slideBy: 1,
                    };
                    var config = {};
                    if (item >= 3) {
                        config = {
                            responsive: {
                                0: {
                                    items: 1
                                },
                                500: {
                                    items: 2
                                },
                                991: {
                                    items: item ? parseInt(item) : 3
                                }
                            }
                        }
                    }
                    if (item < 3) {
                        var config = {
                            responsive: {
                                0: {
                                    items: 1
                                },
                                500: {
                                    items: item ? parseInt(item) : 1
                                },
                                991: {
                                    items: item ? parseInt(item) : 1
                                }
                            }
                        }
                    }
                    var configs = $.extend(defaults, config);
                    // Initialize Slider
                    $(this).owlCarousel(configs);
                });
            }
        },
        /*Popup callback*/
        popupInfo: function() {
            if ($('.yolo-teammember').length > 0) {
                $('.teammember-content').on('click', function() {
                    var $id = $(this).attr('data-option-id');
                    $('.yolo-team-fix').addClass('db');

                    $.ajax({
                        url: yolo_framework_ajax_url,
                        type: 'POST',
                        data: ({
                            action: 'yolo_team_detail',
                            id: $id
                        }),
                        success: function(data) {
                            if (data) {
                                $('.yolo-team-fix').addClass('bk-noimage');
                                $('.yolo-team-wrap').html(data);
                                $('.yolo-team-wrap').animate({
                                    'top': '50%',
                                    opacity: 1
                                }, 350, function() {

                                });

                                $('.team-remove').click(function() {

                                    $('.yolo-team-wrap').animate({
                                        'top': '80%',
                                        opacity: 0
                                    }, 350, function() {
                                        $('.yolo-team-fix').removeClass('bk-noimage');
                                        $('.yolo-team-fix').removeClass('db');
                                    });

                                });
                            }
                        }
                    });
                });
            }
        },
        single_product_slick: function() {
            if ($('.yl-image-slick').length > 0) {
                $('div.slick-slider[data-owl]').each(function() {
                    var slider = $(this),
                        columns = slider.data("owl") ? slider.data("owl") : 1,
                        rows = slider.data("rows") ? slider.data("rows") : 1,
                        autoplay = slider.data('autoplay') ? slider.data('autoplay') : false,
                        rtl = slider.data('rtl') ? slider.data('rtl') : false,
                        autoplayTimeout = slider.data('duration') ? parseInt(slider.data('duration')) : 2000,
                        nav = slider.data('nav') ? slider.data('nav') : false,
                        pagination = slider.data('pagination') ? slider.data('pagination') : false,
                        vertical = slider.data('vertical') ? slider.data('vertical') : false,
                        slider_for = slider.data('for') ? slider.data('for') : false,
                        slider_nav = slider.data('thumb_nav') ? slider.data('thumb_nav') : false,
                        defaults = {
                            dots: pagination,
                            infinite: false,
                            vertical: vertical,
                            speed: 300,
                            slidesToShow: columns,
                            slidesToScroll: columns,
                            rtl: rtl,
                            autoplay: autoplay,
                            autoplaySpeed: autoplayTimeout,
                            arrows: nav,
                            nextArrow: "<div class='slick-next'><i class='fa fa-long-arrow-right'></i></div>",
                            prevArrow: "<div class='slick-prev'><i class='fa fa-long-arrow-left'></i></div>",
                            rows: rows,
                            draggable: false
                        };
                    if (columns > 3) {
                        var config = {
                            slidesToShow: columns,
                            slidesToScroll: columns,
                            responsive: [{
                                    breakpoint: 1450,
                                    settings: {
                                        slidesToShow: columns,
                                        slidesToScroll: columns
                                    }
                                },
                                {
                                    breakpoint: 1200,
                                    settings: {
                                        slidesToShow: 3,
                                        slidesToScroll: 3
                                    }
                                },
                                {
                                    breakpoint: 991,
                                    settings: {
                                        slidesToShow: 2,
                                        slidesToScroll: 2
                                    }
                                },
                                {
                                    breakpoint: 500,
                                    settings: {
                                        slidesToShow: 1,
                                        slidesToScroll: 1
                                    }
                                }
                            ]
                        };
                    }
                    if (columns <= 3 && columns >= 2) {
                        var config = {
                            slidesToShow: columns,
                            slidesToScroll: columns,
                            responsive: [{
                                    breakpoint: 1200,
                                    settings: {
                                        slidesToShow: columns,
                                        slidesToScroll: columns
                                    }
                                },
                                {
                                    breakpoint: 991,
                                    settings: {
                                        slidesToShow: 2,
                                        slidesToScroll: 2
                                    }
                                },
                                {
                                    breakpoint: 500,
                                    settings: {
                                        slidesToShow: 1,
                                        slidesToScroll: 1
                                    }
                                }
                            ]
                        };
                    }
                    if (columns < 2) {
                        var config = {
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            responsive: [{
                                    breakpoint: 1200,
                                    settings: {
                                        slidesToShow: 1,
                                        slidesToScroll: 1
                                    }
                                },
                                {
                                    breakpoint: 991,
                                    settings: {
                                        slidesToShow: 1,
                                        slidesToScroll: 1
                                    }
                                },
                                {
                                    breakpoint: 500,
                                    settings: {
                                        slidesToShow: 1,
                                        slidesToScroll: 1
                                    }
                                }
                            ]
                        };
                    }

                    var configs = $.extend(defaults, config);
                    if (slider_for != false) {
                        var config_for = {
                            slidesToScroll: 1,
                            asNavFor: '.' + slider_for,
                            centerMode: false,
                            focusOnSelect: true
                        };
                        configs = $.extend(config_for, configs);
                    }
                    if (slider_nav != false) {
                        var config_nav = {
                            asNavFor: '.' + slider_nav
                        };
                        configs = $.extend(config_nav, configs);
                    }
                    console.log(configs);
                    // Initialize Slider
                    slider.slick(configs);

                });
            }
        },
        sc_historySlideSlick: function() {
            if ($('.history-slider-shortcode-wrap').length > 0) {
                $('.slick-slider').each(function() {
                    var autoplay = $(this).attr('data-autoplay'),
                        duration = $(this).attr('data-duration'),
                        rtl = $(this).attr('data-rtl'),
                        nav = $(this).parent().attr('id');
                    $(this).slick({
                        rtl: rtl ? rtl : false,
                        centerMode: true,
                        centerPadding: '250px',
                        speed: 500,
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        autoplay: autoplay ? true : false,
                        autoplaySpeed: duration ? parseInt(duration) : 1000,
                        prevArrow: '#' + nav + ' .nav-prev',
                        nextArrow: '#' + nav + ' .nav-next',
                        cssEase: 'linear',
                        responsive: [{
                                breakpoint: 1500,
                                settings: {
                                    centerPadding: '200px',
                                    slidesToShow: 1
                                }
                            },
                            {
                                breakpoint: 1130,
                                settings: {
                                    centerPadding: '200px',
                                    slidesToShow: 1
                                }
                            },
                            {
                                breakpoint: 850,
                                settings: {
                                    centerPadding: '150px',
                                    slidesToShow: 1
                                }
                            },
                            {
                                breakpoint: 767,
                                settings: {
                                    centerPadding: '0px',
                                    slidesToShow: 1
                                }
                            },
                            {
                                breakpoint: 500,
                                settings: {
                                    centerPadding: '0px',
                                    slidesToShow: 1
                                }
                            },
                            {
                                breakpoint: 479,
                                settings: {
                                    centerPadding: '0',
                                    slidesToShow: 1
                                }
                            },
                        ]
                    });
                });
            }
        },
        sc_historySlideCarousel: function() {
            if ($('.history-slider-carousel').length > 0) {
                $('.history-slider-carousel').each(function() {
                    var rtl = $(this).attr('data-rtl'),
                        sync1 = $("#sync1", $(this)),
                        sync2 = $("#sync2", $(this)),
                        flag = false,
                        duration = 500;
                    sync1.owlCarousel({
                            items: 1,
                            margin: 0,
                            nav: false,
                            rtl: rtl ? true : false,
                            navText: ["<i class='ion-android-arrow-back'></i>", "<i class='ion-android-arrow-forward'></i>"],
                            dots: true
                        })
                        .on('changed.owl.carousel', function(e) {
                            if (!flag) {
                                flag = true;
                                sync2.trigger('to.owl.carousel', [e.item.index, duration, true]);
                                flag = false;
                            }

                            // Add class synced to current slide
                            var current = e.item.index;
                            sync2
                                .find(".owl-item")
                                .removeClass("synced")
                                .eq(current)
                                .addClass("synced");
                        });

                    sync2.owlCarousel({
                            margin: 30,
                            items: 3,
                            nav: false,
                            rtl: rtl ? true : false,
                            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
                            center: false,
                            dots: true,
                            onInitialized: function() {
                                sync2.find(".owl-item").eq(0).addClass("synced");
                            }
                        })
                        .on('click', '.owl-item', function() {
                            sync1.trigger('to.owl.carousel', [$(this).index(), duration, true]);
                        })
                        .on('changed.owl.carousel', function(e) {
                            if (!flag) {
                                flag = true;
                                sync1.trigger('to.owl.carousel', [e.item.index, duration, true]);
                                flag = false;
                            }
                        });
                });
            }
        },
        countAppear: function() {
            if ($(".gr-animated").length > 0) {

                $(".gr-animated").appear();

                $(document.body).on("appear", ".gr-animated", function() {
                    $(this).addClass("go");
                });

                $(document.body).on("disappear", ".gr-animated", function() {
                    $(this).removeClass("go");
                });
            }
        },
        /* --------------------------------------------------------------------- */
        /* COUNTER
         /* --------------------------------------------------------------------- */
        countProcess: function() {
            if (!$(".gr-number-counter").length) return;
            $(".gr-number-counter").appear(); // require jquery-appear
            $('body').on("appear", ".gr-number-counter", function() {
                var counter = $(this);
                if (!counter.hasClass("count-complete")) {
                    counter.countTo({
                        speed: 1500,
                        refreshInterval: 100,
                        onComplete: function() {
                            counter.addClass("count-complete");
                        }
                    });
                }
            });
            $('body').on("disappear", ".gr-number-counter", function() {
                $(this).removeClass("count-complete");
            });
        },
        sc_video: function() {
            if ($('.yolo-sc-video-player').length > 0) {
                $('.yolo-sc-video-player').each(function() {

                    var id = $(this).attr('id');
                    if ($(this).hasClass('popup')) {
                        $(this).find('.play-button-wrap').lightGallery({
                            thumbnail: false,
                            fullScreen: false,
                            counter: false,
                            zoom: false,
                            controls: false,
                            mousewheel: false,
                            share: false,
                            rotate: false,
                            mode: 'lg-scale-up',
                            videoMaxWidth: "2000px",
                            autoplayFirstVideo: true,
                            youtubePlayerParams: { modestbranding: 0, showinfo: 0, controls: 1, rel: 0, autoplay: 1 },
                        });
                    } else {
                        $('#' + id + ' .video-close').click(function() {
                            $(this).closest('.yolo-sc-video-player').removeClass("play-video");
                            $(this).parent().find('iframe').remove();
                            $(this).parent().animate({ opacity: 0 }, function() { $(this).hide(); });

                            $(this).closest('.yolo-sc-video-player').find('.play-button-wrap').css({ display: 'block', opacity: 0 })
                                .animate({ opacity: 1 });

                        });
                        $('#' + id + ' .play-button').click(function() {
                            $(this).closest('.yolo-sc-video-player').addClass("play-video");

                            $(this).closest('.play-button-wrap').css({ display: 'block', opacity: 1 })
                                .animate({ opacity: 0 });

                            var url = $(this).data('video');
                            var height = $(this).data('height'),
                                yolo_width = $(this).data('width');
                            var embed, id = $(this).data('id');
                            if (url.indexOf('youtube.com') > -1) {
                                embed = 'https://www.youtube.com/embed/' + id + '?autoplay=1';
                            } else if (url.indexOf('vimeo.com') > -1) {
                                embed = 'https://player.vimeo.com/video/' + id + '?autoplay=1';
                            }
                            var w = $(window).width();
                            /* iframe default */
                            if (yolo_width == 'default') {
                                $(this).closest('.yolo-sc-video-player')
                                    .find('.iframe-video-player')
                                    .append('<iframe allow="autoplay" allowfullscreen style="height:' + height + 'px;width:100%;position:absolute;top:0;" src="' + embed + '"></iframe')
                                    .css({ display: 'block', opacity: 0 })
                                    .animate({ opacity: 1 });
                            } else {
                                var h = parseInt(w * 0.5625);
                                var mt = -parseInt((h - height) / 2);
                                $(this).closest('.yolo-sc-video-player')
                                    .find('.iframe-video-player')
                                    .append('<iframe allow="autoplay" allowfullscreen style="height:' + h + 'px;width:100%;margin-top:' + mt + 'px" src="' + embed + '"></iframe>')
                                    .css({ display: 'block', opacity: 0 })
                                    .animate({ opacity: 1 });
                            }
                            /* Resize */
                            $(window).resize(function() {
                                var w = $(window).width();
                                /* iframe full width */
                                if (yolo_width == 'full_width') {
                                    var h = parseInt(w * 0.5625);
                                    var mt = -parseInt((h - height) / 2);
                                    var atttt = "height:" + h + "px;width:100%;margin-top:" + mt + "px;";
                                    $('.iframe-video-player iframe').attr('style', atttt);
                                }
                            });
                        });
                    }
                });
            }
        }
    };
    $(document).ready(function() {
        YL_SC.init();
    });
})(jQuery);