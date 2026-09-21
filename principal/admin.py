from django.contrib import admin

from .models import (
    Aluno,
    Professor,
    Curso,
    Materia,
    AlunoCurso,
    MateriaCurso,
    Nota,
    Matricula,
    Prova,
)

class MatriculaInline(admin.TabularInline):

    model = Matricula

    extra = 0

@admin.register(MateriaCurso)
class MateriaCursoAdmin(admin.ModelAdmin):

    inlines = [MatriculaInline]

admin.site.register(Curso)
admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Materia)
admin.site.register(AlunoCurso)
admin.site.register(Nota)
admin.site.register(Matricula)
admin.site.register(Prova)
