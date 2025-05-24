jQuery(function () {
    (function ($) {
        /*
         find .youtube
         if .youtube:
         isYoutubeAccessible = ping youtube

         for each .youtube
         if isYoutubeAccessible
         create an overlay div which is clickable (launch jig pop-up)
         else
         create an overlay div "video is not available"
         */
        var $youtube = $('.youtube');
        var $body = $('body');
        if ($youtube.length) {

            // http://stackoverflow.com/questions/286021/detecting-if-youtube-is-blocked-by-company-isp/1804634#1804634
            // using onload callback to prevent a race condition as Eric mentioned on stackoverflow
            var image = new Image();
            image.onerror = function () {
                $youtube.each(function (i, elem) {
                    create(elem, false)
                });
            }

            image.onload = function () {
                $youtube.each(function (i, elem) {
                    create(elem, true);
                });
            }

            function create(youtubeElem, isYoutubeAccessible) {
                var $elem = $(youtubeElem);
                var $container = $('<div class="youtube-container"></div>');
                var $message = {};

                isYoutubeAccessible = typeof isYoutubeAccessible !== 'undefined' ? isYoutubeAccessible : false;

                if (isYoutubeAccessible === true) {
                    $message = $('<div class="youtube-available"></div>');
                    $message.click(videoClick);
                } else {
                    $message = $('<div class="youtube-unavailable"><span class="youtube-msg">Video content is currently unavailable.</span></div>');
                }

                $iframes = $elem.find('[src *= "youtube.com"]');

                if ($iframes.length) {
                    $elem.css('width', $iframes[0].style.width || $iframes[0].width)
                        .css('height', $iframes[0].style.width || $iframes[0].height);
                }
                // set the width & height of the overlay message
                $message.css('width', $elem.css('width'))
                    .css('height', $elem.css('height'));

                // $elem.wrap($container).before($message);
                $elem.wrap($container).before($message);
            }

            function videoClick(event) {
                var $this = $(this),
                    defaultWidth = 845,
                    defaultHeight = 480,
                    $diag = $('<div id="youtube-diag"/>').appendTo($body);

                $body.remove('#youtube-diag');

                // get the iframe
                var $iframes = $this.parent().find('[src *= "youtube.com"]');
                $iframes.clone()
                    .css('width', defaultWidth)
                    .css('height', defaultHeight)
                    .appendTo($diag);

                $diag.ncbidialog({autoOpen: true, width: 'auto', title: "NCBI", modal: true, draggable: true});
                $diag.ncbidialog('open');
                return false;
            }

            image.src = "//youtube.com/favicon.ico";
        }
    })(jQuery);
})
