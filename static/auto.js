$(function() {
var $player_name = $("#player_name");
$player_name.autocomplete({
    source: "/autocomplete",
    minLength: 1,
});})