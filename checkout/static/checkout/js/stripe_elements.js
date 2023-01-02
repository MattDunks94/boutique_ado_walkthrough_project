
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

form.addEventListener('submit', function(ev) {
    // Prevents default action 'POST'
    ev.preventDefault();
    // Disabaling card-element and submit btn to prevent multiple submissions. 
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // Sending card details securely to Stripe. 
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
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