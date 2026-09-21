from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="aluno"
    )

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professor"
    )

    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome
    