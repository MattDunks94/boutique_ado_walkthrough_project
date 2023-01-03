from django.http import HttpResponse


class StripeWH_Handler:
    """ Handle Stripe webhooks """
    # Webhooks notifies user about payment events ie. 
    # successful, dispute or recurring payments.
    # They are sent out whenever an event occurs, such as a payment.

    # Assigning request as an attribute of the class.
    def __init__(self, request):
        self.request = request

    # Takes the stripe event and return a http response.
    def handle_event(self, event):
        """
        Handle a generic/unexpected/unknown webhook event.
        """

        return HttpResponse(
            content=f'Webhook received:{event["type"]}', 
            status=200)