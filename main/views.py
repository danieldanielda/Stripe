import json

from django.shortcuts import render
from django.views import View
from .models import Item
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
stripe.api_key=settings.SECRET_KEY1

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "main/index.html"


    def get_context_data(self, **kwargs):
        item = Item.objects.get(name="Test")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',
            success_url='127.0.0.1:8000/success/',
            cancel_url='127.0.0.1:8000/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


def index(request):
    name = Item.objects.order_by('name')
    description = Item.objects.order_by('description')
    price = Item.objects.order_by('price')
    context = {'name': name, 'description':description, 'price':price}
    return render(request, 'main/index.html', context)

def item(request, id):
    name = Item.objects.get(id=id)
    description = Item.objects.order_by('description')
    price = Item.objects.order_by('price')
    context = {'name': name, 'description': description, 'price': price}
    return render(request, 'main/item.html', context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)







    return HttpResponse(status=200)
class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            item_id = self.kwargs["pk"]
            item = Item.objects.get(id=id)
            intent = stripe.PaymentIntent.create(
                amount=item.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": item.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })