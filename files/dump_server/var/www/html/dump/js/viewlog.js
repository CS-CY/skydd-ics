$(document).ready(function () {
    "use strict";
    var filename = unescape($(location).attr('hash').substring(1));
    $('.title').text(filename);
    get_file(filename);
});
function get_file(filename) {
    var ajax = new XMLHttpRequest(),
        url  = 'cgi/get_file.cgi?file=' + filename,
        json,
    html;
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4) {
            if (ajax.status === 200 || ajax.status === 304) {
                if (ajax.responseText){
                    json = JSON.parse(ajax.responseText);
                    $(".data-table-log").empty();
                    $(".data-table-log").append("<h1 class='title'>" + filename + "</h1><h3 class='log-date'>" + json.time + "</h3><a href='cgi/get_file.cgi?file=" + filename + "&download=yes' class='btn' download='" + filename + "'>Ladda ner loggfil</a><ul class='data-list'></ul>");
                    $.each(json.filerows, function() {
                        $(".data-list").append("<li>" + this + "</li>");
                    });
                }
            } else {
                return false;
            }
        }
    }
    ajax.mozBackgroundRequest = true;
    ajax.open("GET", url, true);
    ajax.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax.send(null);
}
