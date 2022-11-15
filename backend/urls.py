from django.urls import path

from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from backend.views import PartnerUpdate, RegisterAccount, ConfirmAccount, LoginAccount, \
    AccountDetails,CategoryView, ShopView, ProductsView, ProductInfoView, BasketView,\
    PartnerOrders, OrderView, PartnerState

app_name = 'backend'
urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('shops', ShopView.as_view(), name='shops'),
    path('products', ProductsView.as_view(), name='products'),
    path('product', ProductInfoView.as_view(), name='shops'),
    path('user/basket', BasketView.as_view(), name='basket'),
    path ('user/order', OrderView.as_view(), name='order')




]