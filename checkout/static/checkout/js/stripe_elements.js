
// Collecting public key and client secret, slicing one character at either end.
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
// Setting up Stripe, pass it the public key.
var stripe = Stripe(stripe_public_key);
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