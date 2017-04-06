(function defer() {
    if (window.CMS) {
        (function($, settings) {
            var ConcurrentUsers = {
                wasBlocked: false,
                showOverlay: function setOverlay() {
                    // var ele = $('.js-concurrentExclude');
                    $('.js-preventClickOverlay').css({
                        position: 'fixed',
                        top: 0 + 'px',
                        left: 0 + 'px',
                        width: '100%',
                        height: '100%',
                        backgroundColor: 'rgba(0,0,0,0.5)',
                        'z-index': '10000',
                    }).show();
                },
                hideOverlay: function hideOverlay() {
                    $('.js-preventClickOverlay').hide();
                    $('.js-concurrentWarning').remove();
                },
                updateIndicator: function updateIndicator() {
                    $.ajax({
                        method: 'POST',
                        url: settings.page_indicator_url,
                        data: {
                            csrfmiddlewaretoken: settings.csrf,
                            page_id: settings.page
                        }
                    });
                },
                updateStatus: function updateStatus() {
                    $.ajax({
                        method: 'GET',
                        url: settings.page_indicator_url,
                        data: {
                            page_id: settings.page
                        },
                        success: function(data) {
                            data = JSON.parse(data);

                            if (data.conflict && data.block_editing) {
                                // if this page is blocked, we insert an overlay to prevent clicking
                                if (!$('.js-preventClickOverlay').length) {
                                    var overlay = '<div class="js-preventClickOverlay preventClickOverlay"></div>';
                                    $('body, .cms-structure').append(overlay);
                                }
                                // display the overlay
                                ConcurrentUsers.showOverlay();
                                // display the message coming from the server
                                if (!$('.js-concurrentWarning').length) {
                                    message_bar = '<div class="js-concurrentWarning concurrentWarning">' + data.message + '</div>'
                                    $('body, .cms-structure').append(message_bar);
                                }
                                else {
                                    $('.js-concurrentWarning').html(data.message);
                                }
                                ConcurrentUsers.wasBlocked = true;
                            }
                            else {
                                if (data.conflict) {
                                    ConcurrentUsers.updateIndicator();
                                }
                                else {
                                    if (ConcurrentUsers.wasBlocked) {
                                        // it this user was blocked, we need to reload the changed content
                                        location.reload();
                                    }
                                    else {
                                        ConcurrentUsers.updateIndicator();
                                        ConcurrentUsers.hideOverlay();
                                    }

                                }
                            }
                        },
                    });
                },
            };

            document.addEventListener('DOMContentLoaded', ConcurrentUsers.updateStatus, false);

            setInterval(ConcurrentUsers.updateStatus, settings.check_time);
        })(CMS.$, ConcurrentUsersSettings);
    }
    else {
        setTimeout(function() {
            defer()
        }, 50);
    }
})();
