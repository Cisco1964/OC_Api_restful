from django.conf import settings
from django.db import models


class Projects(models.Model):

    PROJECT_TYPE = [
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('android', 'android'),
        ('ios', 'ios'),
    ]
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    # type (back-end, front-end, iOS ou Android)
    type = models.CharField(choices=PROJECT_TYPE,
                            max_length=100, blank=False, default='back-end')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       related_name='project_author',
                                       on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributors(models.Model):

    PERMISSIONS = [
        ('restricted', 'restricted'),
        ('all', 'all')
    ]
    ROLES = [
        ('auteur', 'auteur'),
        ('contributeur', 'contributeur')
    ]
    user_id = models.IntegerField()
    project_id = models.ForeignKey(Projects,
                                   on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, max_length=20, blank=False, default='auteur')
    permission = models.CharField(choices=PERMISSIONS,
                                  max_length=20,
                                  blank=False, default='all')

    def __str__(self):
        return self.role


class Issues(models.Model):

    PRIORITY_TYPE = [
        ('Faible', 'Faible'),
        ('Moyenne', 'Moyenne'),
        ('élevée', 'élevée')
    ]
    STATUS_TYPE = [
        ('A faire', 'A faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé')
    ]
    title = models.CharField(max_length=100, blank=False)
    desc = models.CharField(max_length=2000, blank=False)
    tag = models.CharField(max_length=10, blank=False)
    # priorité (FAIBLE, MOYENNE ou ÉLEVÉE)
    priority = models.CharField(choices=PRIORITY_TYPE, max_length=20,
                                blank=False, default='Faible')
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    # statut (À faire, En cours ou Terminé),
    status = models.CharField(choices=STATUS_TYPE, max_length=20, blank=False, default='A faire')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='issue_author')
    # (l’assigné par défaut étant l'auteur lui-même)
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='issue_assignee')
    time_created = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=2000, blank=False)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='comment_author')
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE, related_name='comment_issues')
    time_created = models.DateTimeField(auto_now_add=True)
