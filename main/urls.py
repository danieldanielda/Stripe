from django.urls import path
from . import views
from main.views import CreateCheckoutSessionView, CancelView, SuccessView, stripe_webhook
app_name = 'main'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('item/<int:id>/', views.item, name = 'item'),
    # path('create-checkout-session/item/<int:id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]
