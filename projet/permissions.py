from rest_framework.permissions import BasePermission
from django.db.models import Q
from .models import Contributors
from django.contrib.auth import get_user_model


User = get_user_model()


class IsUserAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print("REQUEST.USER", request.user)
        return bool(request.user and request.user.is_authenticated)


class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if Contributors.objects.filter(Q(user_id=user.id) & Q(project_id=view.kwargs['pk1'])):
            return True
        return False


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if view.kwargs != {}:
            if Contributors.objects.filter(Q(user_id=user.id) & Q(project_id=view.kwargs['pk1'])):
                return True
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "DELETE"):
            return obj.author_user_id == request.user
        return False


class IssuePermission(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if Contributors.objects.filter(Q(user_id=user.id) & Q(project_id=view.kwargs['pk1'])):
            return True
        return False

    def object_permission(self, request, view, obj):
        if request.method in ("PUT", "DELETE"):
            if obj.author_user_id == request.user:
                return True
        return request.user == obj.author_user_id


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if Contributors.objects.filter(Q(user_id=user.id) & Q(project_id=view.kwargs['pk1'])):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT", "DELETE"):
            if obj.author_user_id == request.user:
                return True
        return request.user == obj.author_user_id
