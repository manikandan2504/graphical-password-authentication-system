from django.db import models

class GraphicalUser(models.Model):

    username = models.CharField(max_length=100)

    email = models.EmailField()

    password = models.CharField(max_length=255)

    graphical_password = models.CharField(max_length=100)

    def __str__(self):
        return self.username