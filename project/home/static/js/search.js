$(document).ready(function(){
    $('#search_go').click(function(){
        search_value = $('#search_bar').val();
        window.location.href = `/search/${search_value}`;
    });
});
