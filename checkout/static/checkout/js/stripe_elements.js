
// Collecting public key and client secret, slicing one character at either end.
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// Setting up Stripe, pass it the public key.
var stripe = Stripe(stripePublicKey);
// Creating an instance of Stripe elements.
var elements = stripe.elements();
// Creating card element.
var card = elements.create('card', {style: style});
// Styling the card element.(see stripe docs.)
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// Mounting the card element to the div created in checkout.html, via id.
card.mount('#card-element');

// Handle realtime validation errors on the card element.
// Listening for a change in the card number input.
card.addEventListener('change', function (event) {
    // Get element with id.
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        // If an error occurs, incorrect details, display message with fa icon.
        var html = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
        `
        $(errorDiv).html(html);
        // Otherwise display nothing.
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

// Adding event listener when form submitted.
form.addEventListener('submit', function(ev) {
    // Prevents default action 'POST'
    ev.preventDefault();
    // Disabaling card-element and submit btn to prevent multiple submissions. 
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // Fading payment-form element. 
    $('#payment-form').fadeToggle(100);
    // Fading loading-overlay element. 
    $('#loading-overlay').fadeToggle(100);
    // Sending card details securely to Stripe. 
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            // Getting users paying method and billing details.
            card: card,
            billing_details: {
                // 'trim' method removes any whitepace from the values.
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county.value),
                }
            }
        },
        // Getting users shipping details.
        shipping: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                postal_code: $.trim(form.postcode.value),
                state: $.trim(form.county.value),
            }
        }

        // Card details results.
    }).then(function(result) {
        // If card details invalid, display error message.
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            // If an error occurs re-enable card-element and submit btn, setting them to false.
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
            // Otherwise successful payment.
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});