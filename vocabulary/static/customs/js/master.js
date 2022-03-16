(function($,sr){
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
      var timeout;

        return function debounced () {
            var obj = this, args = arguments;
            function delayed () {
                if (!execAsap)
                    func.apply(obj, args);
                timeout = null;
            }

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100);
        };
    };

    // smartresize
    jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

})(jQuery,'smartresize');

var BASE_URL = 'https://addwordstoenglish.com/'

function initSidebar() {
    var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
                    $BODY = $('body'),
                    $MENU_TOGGLE = $('#sidebar-menu-btn'),
                    $SIDEBAR = $('#sidebar-menu'),
                    // $LEFT_COL = $('.left_col'),
                    $MAIN_CONTENT = $('.main-content'),
                    $TOP_NAVIGATION = $('.top-navigation'),
                    $FOOTER = $('footer');

    function setContentHeight() {
        // reset height
        $MAIN_CONTENT.css('min-height', $(window).height());

        var bodyHeight = $BODY.outerHeight(),
            footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
            sidebarHeight = $SIDEBAR.height(),
            contentHeight = bodyHeight < sidebarHeight ? sidebarHeight : bodyHeight;

        // normalize content
        contentHeight -= $TOP_NAVIGATION.height() + footerHeight;
        
        $MAIN_CONTENT.css('min-height', contentHeight);
    };
    
    function closeMenu() {
        $SIDEBAR.find('li').removeClass('active');
        $SIDEBAR.find('li ul').slideUp();
        $SIDEBAR.find('li span').removeClass('rotate');
    }

    $SIDEBAR.find('a').click(function() {
        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
            $li.find('span').removeClass('rotate');
        } else {
            if (!$li.parent().is('.sub-menu')) {
                closeMenu();
            }
            $li.addClass('active');
            $('ul:first', $li).slideDown(function () {
                setContentHeight();
            });
            if ($li.has('.sub-menu')) {
                $li.find('span').addClass('rotate');
            }
        }
    })

    // toggle small or large menu
    $MENU_TOGGLE.click(function () {
        if ($SIDEBAR.hasClass('sidebar')) {
            $SIDEBAR.addClass('sidebar-sm').removeClass('sidebar');
            // $SIDEBAR.find('sidebar').hide();
            // $SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
        } else {
            $SIDEBAR.addClass('sidebar').removeClass('sidebar-sm')
            // $SIDEBAR.find('li.active-sm ul').show();
            // $SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
        }

        // $BODY.toggleClass('nav-md nav-sm');

        setContentHeight();

        $('.dataTable').each(function () { $(this).dataTable().fnDraw(); });
    });

    // check active menu
    $SIDEBAR.find('a[href="/'+ CURRENT_URL.split(BASE_URL)[1] + '"]').parent('li').addClass('active');

    // recompute content when resizing
    $(window).smartresize(function () {
        setContentHeight();
    });

    setContentHeight();
}

function fetchUser() {
    $.ajax({
        type: 'GET',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('access')
        },
        url: BASE_URL + 'auth/api/fetch-user/',
        data: {

        },
        success: function (data) {
            console.log('# ---- Fetch user success ---- #');
            if (data) {
                $("#username").html(data.username);
            }
        },
        error: function (error) {
            console.log('# ---- Fetch user error ---- #');
            window.location.replace(BASE_URL + 'auth/login/');
        }
    })
}

function logout() {
    if (localStorage.getItem('access')) {
        localStorage.removeItem('access');
    }

    if (localStorage.getItem('refresh')) {
        localStorage.removeItem('refresh')
    }
    window.location.replace(BASE_URL + 'auth/login/');
}

$(document).ready(function () {
    initSidebar();
    fetchUser();
})