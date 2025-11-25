# libraryapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    # auth
    path('login/', auth_views.LoginView.as_view(template_name='libraryapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # books
    path('add_book/', views.add_book, name='add_book'),
    path('view_books/', views.view_books, name='view_books'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    # members
    path('add_member/', views.add_member, name='add_member'),
    path('view_members/', views.view_members, name='view_members'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete_member/<int:member_id>/', views.delete_member, name='delete_member'),
    # issue/return
    path('issue_book/', views.issue_book, name='issue_book'),
    path('view_issued/', views.view_issued, name='view_issued'),
    path('return_book/<int:issue_id>/', views.return_book, name='return_book'),
    # staff-only admin-like dashboard
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
