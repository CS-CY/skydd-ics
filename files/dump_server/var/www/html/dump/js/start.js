function b64EncodeUnicode(str) {
    // https://developer.mozilla.org/en-US/docs/Web/API/WindowBase64/Base64_encoding_and_decoding
    // first we use encodeURIComponent to get percent-encoded UTF-8,
    // then we convert the percent encodings into raw bytes which
    // can be fed into btoa.
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
        function toSolidBytes(match, p1) {
            return String.fromCharCode('0x' + p1);
    }));
}
function b64DecodeUnicode(str) {
    // Going backwards: from bytestream, to percent-encoding, to original string.
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}
$(document).ready(function () {
    "use strict";
    get_files();
    setInterval(function () {
        if ($('input.search-bar').val() === ''){
            get_files();
        }
    }, 60000);
    $(".search-bar").keyup(function(event) {
        if (event.keyCode == '13') {
            if ($(".search-bar").val() === ""){
                get_files();
            } else {
                get_files_search(b64EncodeUnicode($(".search-bar").val()));
            }
        }
        return false;
    });
});
function get_search_result() {
    var ajax = new XMLHttpRequest(),
        url  = 'searching.json',
        json;
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4) {
            if (ajax.status === 200 || ajax.status === 304) {
                if (ajax.responseText){
                    json = JSON.parse(ajax.responseText);
                    if (json.files){
                        show_files(json, 'search');
                    } else if (json.search) {
                        $(".data-message").text("Söker i fil: " + json.search);
    			setTimeout(function(){
                        	get_search_result();
    			},300);
                    } else {
    			setTimeout(function(){
                        	get_search_result();
    			},300);
                    }
                } else {
    			setTimeout(function(){
                        	get_search_result();
    			},300);
		}
            } else {
                return false;
            }
        }
    }
    ajax.mozBackgroundRequest = true;
    ajax.open("GET", url, true);
    ajax.setRequestHeader( 'Pragma', 'no-cache');
    ajax.setRequestHeader( 'cache-control', 'no-store, must-revalidate');
    ajax.setRequestHeader("Accept","application/json");
    ajax.send(null);
}
function get_files() {
    var ajax = new XMLHttpRequest(),
        url  = 'cgi/get_files.cgi',
    json;
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4) {
            if (ajax.status === 200 || ajax.status === 304) {
                if (ajax.responseText){
                    json = JSON.parse(ajax.responseText);
                    show_files(json);
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
function get_files_search(query) {
    var ajax = new XMLHttpRequest(),
        url  = 'cgi/get_files.cgi?search=' + query,
    json;
    $(".data-list").empty();
    $(".data-size").empty();
    $(".data-message").empty();
    ajax.mozBackgroundRequest = true;
    ajax.open("GET", url, true);
    ajax.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax.send(null);
    setTimeout(function(){
        get_search_result();
    },300);
}
function show_files(json, action){
    $(".data-list").empty();
    $(".data-message").empty();
    if (action === 'search'){
        $(".data-size").text("Totalt antal filer i sökresultatet: " + json.files.length + " av " + json.files_count);
    } else {
        $(".data-size").text("Totalt antal filer: " + json.files.length);
    }
    $(".data-message").text(json.message);
    $.each(json.files, function() {
        $(".data-list").append("<li><a href='log.html#" + this.name + "' class='list-item'><h2>" + this.name + "</h2><h3>" + this.size + "</h3><h3>" + this.time + "</h3></a></li>");
    });
}
