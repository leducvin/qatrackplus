require(['jquery'], function($) {

    var loggedOutMessage = (
        '<div class="logout-alert alert fade in alert-warning">' +
        '  <a class="close" href="#" data-dismiss="alert">&times;</a>' +
        '  Warning, either the server is not responding or you are currently logged out! ' +
        '  In order to prevent any potential data loss, please log in in ' +
        '  a different tab by clicking the following link and then ' +
        '  return to this page. ' +
        '  <a class="btn btn-xs btn-default new-tab-link alert-link" href="' + QAURLs.LOGIN + '">' +
        '    Log Back In  <i class="fa fa-chevron-right" aria-hidden="true"></i>' +
        '  </a>' +
        '</div>'
    );

    var currentPing = null;
    var loggedOutMessageShown = false;

    window.userIsAuthenticated = true;

    function setAuthenticatedState(authenticated){
        window.userIsAuthenticated = authenticated;
        if (window.userIsAuthenticated && loggedOutMessageShown){
            $(".logout-alert").remove();
            loggedOutMessageShown = false;
        }else if (!window.userIsAuthenticated && !loggedOutMessageShown){
            $(".content-header").append(loggedOutMessage);
            loggedOutMessageShown = true;
        }
    }
    function ping(){
        if (currentPing === null){
            currentPing = $.ajax({
                url: QAURLs.PING,
                type: 'GET',
                timeout: 1000,
                success: function (res) {
                    setAuthenticatedState(res.logged_in);
                },
                error: function (res) {
                    setAuthenticatedState(false);
                },
                complete: function(){
                    currentPing = null;
                }
            });
        }
    }

    setInterval(ping, 5000);

});
