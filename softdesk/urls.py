from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authentication.views import RegisterView, LoginView
from projet.views import IssuesView, CommentsView,\
    ContributorsView, ProjectsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('projects/', ProjectsView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:pk1>/', ProjectsView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),
    path('projects/<int:pk1>/users/', ContributorsView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:pk1>/users/<int:pk2>/', ContributorsView.as_view({'delete': 'destroy'})),
    path('projects/<int:pk1>/issues/', IssuesView.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:pk1>/issues/<int:pk2>/', IssuesView.as_view({'put': 'update', 'delete': 'destroy'})),
    path('projects/<int:pk1>/issues/<int:pk2>/comments/', CommentsView.as_view({'post': 'create', 'get': 'list'})),
    path('projects/<int:pk1>/issues/<int:pk2>/comments/<int:pk3>/', CommentsView.as_view({'get': 'retrieve', 'delete': 'destroy', "put": "update"}))
]
