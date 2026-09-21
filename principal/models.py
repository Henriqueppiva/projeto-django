from django.db import models
from users.models import Aluno, Professor
from django.core.validators import  MinValueValidator

class Curso(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Materia(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class AlunoCurso(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="cursos" )

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="curso_aluno" )

    class Meta: # O mesmo aluno nao pode ser cadastrado duas vezes no mesmo curso
        constraints = [
            models.UniqueConstraint(
                fields=['aluno', 'curso'],
                name='unique_aluno_por_curso'
            )
        ]

    def __str__(self):
            return f"{self.aluno.nome} - {self.curso.nome}"

class MateriaCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="materias_curso" )

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="cursos" )

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="materias_lecionadas" )

    formula_media = models.CharField(max_length=200,)

    class Meta: # a mesmo materia nao pode ser cadastrada duas vezes no mesmo curso
        constraints = [
            models.UniqueConstraint(
                fields=['curso', 'materia'], 
                name='unique_materia_por_curso'
            )
        ]

    def __str__(self):
            return f"{self.materia.nome} - {self.curso.nome}"

class Prova(models.Model):
    materia_curso = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name="avaliacoes" )

    nome = models.CharField(max_length=100)

    valor_maximo = models.DecimalField(max_digits=4, decimal_places=2, default=10, validators=[MinValueValidator(0)],)

    peso = models.DecimalField(max_digits=4, decimal_places=2, default=1, validators=[MinValueValidator(0)],)

    conteudo = models.TextField(blank=True, null=True)

    class Meta: # Uma nota por avaliacao
        constraints = [
            models.UniqueConstraint(
                fields=["materia_curso", "nome"],
                name="unique_nome_por_materia_curso",
            )
        ]

    def __str__(self):
            return self.nome

class Matricula(models.Model):
     aluno_curso = models.ForeignKey(AlunoCurso, on_delete=models.CASCADE, related_name="matriculas" )

     materia_curso = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name="matriculas" )

     def media(self):
      notas = self.notas.all()

      soma = 0
      pesos = 0

      for nota in notas:
         soma += nota.nota * nota.prova.peso
         pesos += nota.prova.peso

      if pesos == 0:
        return 0

      return round(soma / pesos, 2)

     def __str__(self):
            return f"{self.aluno_curso} - {self.materia_curso.materia}"

class Nota(models.Model):

     matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name="notas" )

     prova = models.ForeignKey(Prova, on_delete=models.CASCADE, related_name="notas" )

     nota = models.DecimalField(max_digits=4, decimal_places=2, default=1, validators=[MinValueValidator(0)],)

     class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['matricula', 'prova'], 
            name='unique_matricula_por_prova'
        )
    ]

     def __str__(self):
            return f"{self.matricula} - {self.prova}"
    
    


