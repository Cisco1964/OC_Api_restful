from rest_framework import serializers
from .models import Contributors, Projects, Issues, Comments
from django.contrib.auth import get_user_model

User = get_user_model()


class ContributorsSerializer(serializers.ModelSerializer):
    '''
    Contributeur
    '''
    class Meta:
        model = Contributors
        fields = ['id', 'project_id', 'user_id', 'role']


class ProjectsSerializer(serializers.ModelSerializer):
    '''
    Création d'un projet
    '''
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'type': {'required': True},
        }


class ProjectsIDSerializer(serializers.ModelSerializer):
    '''
    Mise à jour d'un projet
    '''
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'type': {'required': True},
            'author_user_id': {'required': True},
        }


class IssuesSerializer(serializers.ModelSerializer):
    '''
    Détail d'un problème
    '''
    class Meta:
        model = Issues
        fields = ['id', 'project_id', 'title', 'desc', 'tag', 'priority', 'status',
                        'assignee_user_id', 'time_created']
        extra_kwargs = {
            "project_id": {'read_only': True},
            "title": {'required': True},
            "desc": {'required': True},
            "priority": {'required': True},
            "status": {'required': True},
            "assignee_user_id": {'required': True},
            "time_created": {'read_only': True}
        }


class CommentsSerializer(serializers.ModelSerializer):
    '''
    Commentaires
    '''
    class Meta:
        model = Comments
        fields = ['id', 'issue_id', 'description', 'time_created']
        extra_kwargs = {
            "issue_id": {'read_only': True},
        }

