if (typeof JL() !== "undefined") {
    const addCsrfTokenToXhrHeader = function (xhr) {
        const cookieName = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, cookieName.length + 1) === (cookieName + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(cookieName.length + 1));
                    break;
                }
            }
        }
        xhr.setRequestHeader('X-CSRFToken', cookieValue);
    };

    const appender = JL.createAjaxAppender("csrftoken appender");
    appender.setOptions({
        "beforeSend": addCsrfTokenToXhrHeader
    });

    // Get all loggers to use this appender
    JL().setOptions({
        "appenders": [appender]
    });
}