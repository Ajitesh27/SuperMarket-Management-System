from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as user_views

urlpatterns = [
    path('home/', user_views.Home.as_view(), name='home'),
    path('user/', user_views.UserListView.as_view(), name='user'),
    path('roles/', user_views.RoleListView.as_view(), name='roles'),
    path('role/', user_views.RoleCreationView.as_view(), name='role'),
    path('edit_role/<int:id>/', user_views.EditRoleView.as_view(), name='edit_role'),
    path('delete_role/<int:id>/', user_views.DeleteRoleView.as_view(), name='delete_role'),
    path('signup/', user_views.SignUpView.as_view(), name='signup'),
    path('edit/<int:id>/', user_views.EditProfileView.as_view(), name='edit'),
    path('change_password/', user_views.PasswordUpdateView.as_view(), name='change_password'),
    path('deactivate/<int:id>/', user_views.DeactivateView.as_view(), name='deactivate'),
    path('activate/<int:id>/', user_views.ActivateView.as_view(), name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('setting/', user_views.Setting.as_view(), name='setting'),
    path('account_report/', user_views.AccountPDFView.as_view(), name='account_report')
]