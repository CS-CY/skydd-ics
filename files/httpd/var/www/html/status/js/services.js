$(document).ready(function () {
    "use strict";
    $(".data-list").empty();
    set_services();
});
function set_services() {
    var ajax = new XMLHttpRequest(),
        url  = 'cgi/status.cgi',
    json;
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4) {
            if (ajax.status === 200 || ajax.status === 304) {
                if (ajax.responseText){
                    json = JSON.parse(ajax.responseText);
                    show_services(json);
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
function show_services(json){
    var services = '';
    $.each(json, function() {
        $.each(this, function(key, value) {
            services += '<li>';
            if (value === 'active'){
                services += '<a href="#" class="list-item active-item">';
            }
            else {
                services += '<a href="#" class="list-item inactive-item">';
            }
            services += '<h2>' + key + '</h2>';
            if (value === 'active'){
                services += '<span class="list-status">Aktiv</span>';
            }
            else {
                services += '<span class="list-status">Inaktiv</span>';
            }
            services += '</a></li>';
        });
    });
    $(".data-list").html(services);
}
