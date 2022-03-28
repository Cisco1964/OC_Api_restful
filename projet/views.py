from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from projet.permissions import (IsUserAuthenticated, ProjectPermission, ContributorPermission,\
                                IssuePermission, CommentPermission)

from django.contrib.auth import get_user_model

from .models import Contributors, Projects, Issues, Comments
from projet.serializers import (IssuesSerializer, ProjectsSerializer, ProjectsIDSerializer,\
                                CommentsSerializer, ContributorsSerializer)


User = get_user_model()


class ProjectsView(ModelViewSet):
    """
    Endpoints 3, 4, 5, 6, 7
    """
    serializer_class = ProjectsIDSerializer
    permission_classes = [IsUserAuthenticated, ProjectPermission]
    queryset = Projects.objects.all()

    ''' 3-Récupérer la liste de tous les projets '''
    def list(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        liste = Projects.objects.filter(author_user_id=user.id)
        serializer = ProjectsIDSerializer(liste, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    ''' 4-Création d'un projet '''
    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author_user_id=user)
            contributor = Contributors.objects.create(project_id=project,
                                                      user_id=user.id,
                                                      role='Auteur')
            contributor.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    ''' 5-Récupérer les détails d'un projet '''
    def retrieve(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(self.queryset, pk=kwargs['pk1'])
        if project:
            project = ProjectsIDSerializer(project, many=False)
            return Response(project.data,
                            status=status.HTTP_200_OK)

    ''' 6-Mettre à jour un projet '''
    def update(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(self.queryset, pk=kwargs['pk1'])
        self.check_object_permissions(self.request, project)
        user = User.objects.get(username=request.user)
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['author_user_id'] = user.id
        serializer = ProjectsIDSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    ''' 7-Supprimer un projet '''
    def destroy(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(self.queryset, pk=kwargs['pk1'])
        self.check_object_permissions(self.request, project)
        project.delete()
        return Response({
                    'status': 'OK',
                    'message': "Projet supprimé"
                }, status=status.HTTP_204_NO_CONTENT)


class IssuesView(ModelViewSet):
    """
    Endpoints 11, 12, 13 et 14
    """
    serializer_class = IssuesSerializer
    permission_classes = [IsUserAuthenticated, IssuePermission]
    queryset = Issues.objects.all()

    '''11-Récupérer la liste de tous les problèmes liés à un projet'''
    def list(self, request, pk=None, *args, **kwargs):
        try:
            project = Projects.objects.get(pk=kwargs['pk1'])
        except Projects.DoesNotExist:
            return Response({
                    'status': 'Incorrect',
                    'message': "Ce projet n'existe pas"
                }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            liste = Issues.objects.filter(project_id=kwargs['pk1'])
        except Issues.DoesNotExist:
            return Response({
                    'status': 'Incorrect',
                    'message': "Aucun problème rattachés au projet"
                }, status=status.HTTP_401_UNAUTHORIZED)

        request.data['project_id'] = kwargs['pk1']
        serializer = IssuesSerializer(liste, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    ''' 12-Créer un problème dans un projet '''
    def create(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        user = User.objects.get(username=request.user)
        try:
            assignee = User.objects.get(username=request.data['assignee_user_id'])
        except User.DoesNotExist:
            return Response({
                    'status': 'Incorrect',
                    'message': 'Utilisateur inconnu'
                }, status=status.HTTP_401_UNAUTHORIZED)

        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['assignee_user_id'] = assignee.id
        serializer = IssuesSerializer(data=request.data)
        if Contributors.objects.filter(user_id=assignee.id).filter(project_id=project).exists():
            if serializer.is_valid():
                serializer.save(author_user_id=user, project_id=project)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                    'status': 'Incorrect',
                    'message': "l'assignee saisi n'est pas un contributeur du projet"
                }, status=status.HTTP_200_OK)

    ''' 13-Mise à jour d'un problème dans un projet'''
    def update(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        self.check_object_permissions(request, issue)

        try:
            assignee = User.objects.get(username=request.data['assignee_user_id'])
        except User.DoesNotExist:
            return Response({
                    'status': 'Incorrect',
                    'message': 'Utilisateur inconnu'
                }, status=status.HTTP_401_UNAUTHORIZED)

        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['assignee_user_id'] = assignee.id
        serializer = IssuesSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    ''' 14-Supprimer un problème dans un projet'''
    def destroy(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response({
                    'status': 'OK',
                    'message': "Problème supprimé"
                }, status=status.HTTP_204_NO_CONTENT)


class CommentsView(ModelViewSet):
    """
    Endpoints 15, 16, 17, 18, 19
    """
    serializer_class = CommentsSerializer
    permission_classes = [IsUserAuthenticated, CommentPermission]
    queryset = Comments.objects.all()

    '''15-Créer des commentaires sur un problème'''
    def create(self, request, pk=None, *args, **kwargs):
        user = User.objects.get(username=request.user)
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=user, issue_id=issue)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    '''16-Récupérer la liste de tous les commentaires liés à un problème'''
    def list(self, request, pk=None, *args, **kwargs):
        user = User.objects.get(username=request.user)
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        comment = Comments.objects.filter(issue_id=kwargs['pk2'])
        serializer = CommentsSerializer(comment, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    '''17-Mise à jour d'un commentaire'''
    def update(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        comment = get_object_or_404(Comments, pk=kwargs['pk3'])
        self.check_object_permissions(request, comment)
        user = User.objects.get(username=request.user)
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    ''' 18-Supprimer un commentaire'''
    def destroy(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        comment = get_object_or_404(Comments, pk=kwargs['pk3'])
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({
                    'status': 'OK',
                    'message': "Commentaire supprimé"
                }, status=status.HTTP_204_NO_CONTENT)

    ''' 19-Récupérer un commentaire via son id'''
    def retrieve(self, request, pk=None, *args, **kwargs):
        user = User.objects.get(username=request.user)
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        issue = get_object_or_404(Issues, pk=kwargs['pk2'])
        comment = get_object_or_404(Comments, pk=kwargs['pk3'])
        if comment:
            project = CommentsSerializer(comment, many=False)
            return Response(project.data,
                            status=status.HTTP_200_OK)


class ContributorsView(ModelViewSet):
    """
    Endpoints 8, 9, 10
    """
    serializer_class = ContributorsSerializer
    permission_classes = [IsUserAuthenticated, ContributorPermission]
    queryset = Contributors.objects.all()

    ''' 9 - Liste des utilisateurs rattachés à un projet '''
    def list(self, request, pk=None, *args, **kwargs):
        user = User.objects.get(username=request.user)
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        instance = Contributors.objects.filter(project_id=kwargs['pk1'])
        serializer = ContributorsSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    ''' 8- Ajouter un nouveau contributeur à un projet'''
    def create(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, id=kwargs['pk1'])
        try:
            user = User.objects.get(username=request.data['user_id'])
        except User.DoesNotExist:
            return Response({
                    'status': 'Incorrect',
                    'message': 'Utilisateur inconnu'
                }, status=status.HTTP_401_UNAUTHORIZED)
        if request.user == request.data['user_id']:
            return Response({
                    'status': 'Incorrect',
                    'message': "Le contributeur ne peut pas être l'auteur"
                }, status=status.HTTP_401_UNAUTHORIZED)

        if Contributors.objects.filter(Q(user_id=user.id) & Q(project_id=kwargs['pk1'])):
            return Response({
                    'status': 'Incorrect',
                    'message': "Ce contributeur existe déjà"
                }, status=status.HTTP_200_OK)

        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['project_id'] = project.id
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['user_id'] = user.id
        serializer = ContributorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project, role='contributeur', permission='restricted')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    ''' 10 - Supprimer un contributeur '''
    def destroy(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['pk1'])
        if project.author_user_id != request.user:
            return Response({
                    'status': 'Incorrect',
                    'message': "Suppression non autorisée"
                }, status=status.HTTP_401_UNAUTHORIZED)

        contributor = Contributors.objects.filter(Q(user_id=kwargs['pk2']) & Q(project_id=kwargs['pk1']))
        contributor.delete()
        return Response({
                    'status': 'OK',
                    'message': "Contributeur supprimé"
                }, status=status.HTTP_204_NO_CONTENT)
