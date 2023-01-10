// Getting the countryfield value via id.
let countrySelected = $('#id_default_country').val();
// If countrySelected is False (no option selected)...
if(!countrySelected) {
    // Set the color of the placeholder, default selection.
    $('#id_default_country').css('color', '#aab7c4');
};
// Whenever the selection changes...
$('#id_default_country').change(function() {
    // Get value of field.
    countrySelected = $(this).val();
    // If no option selected, set color.
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    // Otherwise set different color. 
    } else {
        $(this).css('color', '#000');
    };
});