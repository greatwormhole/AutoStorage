from django.urls import path
from .views import (
    HomeView,
    LoginView,
    THDList,
    MainView,
    THDSelect,
    WebSocketTHDcheck,
    LogoutView,
    CrateView,
    CheckConnection,
    MoveCrateView
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('API/login', LoginView.as_view(), name='login'),
    path('API/THD-list', THDList.as_view(), name='THD_list'),
    path('API/THD-lock', MainView.as_view(), name='locking'),
    path('API/THD-select', THDSelect.as_view(), name="THD_select"),
    path('API/THD-check', WebSocketTHDcheck.as_view(), name='websocket_THD_check'),
    path('API/logout', LogoutView.as_view(), name='logout'),
    path('API/crate/<int:pk>/', CrateView.as_view(), name='crate'),
    path('API/move-crate/<int:pk>/', MoveCrateView.as_view(), name='move_crate'),
    path('API/check-connection', CheckConnection.as_view(), name='check_connection'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)