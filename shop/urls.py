from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path("register/", views.register,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name = 'shop/login.html'),name="Login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='shop/logout.html'),name="Logout"),
    path("profile/", views.profile,name="profile"),

]

