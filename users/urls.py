from django.urls import path
from users.views import RegisterView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(template_name='register.html'), name='register'),
]
