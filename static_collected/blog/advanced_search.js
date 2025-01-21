// This toggles the title and the search form, and saves it into a localstorage
// cookie, so that the state is kept when navigating search results.
function show_search() {
    $("#advanced_search_title").html("Advanced Search ⇈");
    $("#advanced_search_form_container").show();
    
    if (localStorage.getItem("hidden") != null) {
        localStorage.removeItem("hidden");
    }
}

function hide_search() {
    $("#advanced_search_title").html("Advanced Search ⇊");
    $("#advanced_search_form_container").hide();
    localStorage.setItem("hidden", "true");
}

(localStorage.getItem("hidden") == null) ? show_search() : hide_search();

$(document).ready(function() {
    $("#advanced_search_title").click(function() {
        (localStorage.getItem("hidden") == null) ? hide_search() : show_search();
    });
});