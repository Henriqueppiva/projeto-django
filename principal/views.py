from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import AlunoCurso, Matricula, Nota, MateriaCurso, Curso, Prova

@login_required
def menu_aluno(request):

    if not is_aluno(request.user):
        return redirect("principal:professor_index")


    aluno = request.user.aluno

    cursos = AlunoCurso.objects.filter(
        aluno=aluno
    ).select_related("curso")

    context = {
        "cursos": cursos
    }

    return render(request, "principal/aluno_index.html", context)

@login_required
def menu_professor(request):

    if not is_professor(request.user):
                return redirect("principal:aluno_index")

    professor = request.user.professor

    cursos = Curso.objects.filter(
    materias_curso__professor=professor
    ).distinct()

    context = {
        "cursos": cursos,
    }

    return render(request, "principal/professor_index.html", context)


@login_required
def aluno_materia(request, matricula_id):

    if not is_aluno(request.user):
            return redirect("principal:professor_index")

    matricula = get_object_or_404(
        Matricula,
        id=matricula_id,
        aluno_curso__aluno=request.user.aluno
    )

    context = {
        "matricula": matricula
    }

    return render(request, "principal/aluno_materia.html", context)

@login_required
def professor_materia(request, materia_id):

    if not is_professor(request.user):
                return redirect("principal:aluno_index")

    professor = request.user.professor

    materia = get_object_or_404(
            MateriaCurso,
            id=materia_id,
            professor=professor
        )

    matriculas = Matricula.objects.filter(
        materia_curso=materia
    ).select_related("aluno_curso__aluno")

    context ={
         "materia": materia,
         "matriculas": matriculas
    }

    return render(request, "principal/professor_materia.html", context)

@login_required
def professor_notas(request, matricula_id):

    if not is_professor(request.user):
                return redirect("principal:aluno_index")

    professor = request.user.professor

    matricula = get_object_or_404(
            Matricula,
            id=matricula_id,
            materia_curso__professor=professor
        )

    avaliacoes = matricula.materia_curso.avaliacoes.all()
    
    notas_por_prova = {
                       nota.prova_id: nota 
                       for nota in matricula.notas.select_related("prova")
                       }

    linhas = [
        {"prova": prova, "nota": notas_por_prova.get(prova.id)}
        for prova in avaliacoes
    ]

    context ={
         "matricula": matricula,
         "linhas": linhas,
    }

    return render(request, "principal/professor_notas.html", context)

@login_required
def lancar_nota(request, matricula_id, prova_id):

    if not is_professor(request.user):
                return redirect("principal:aluno_index")

    professor = request.user.professor

    matricula = get_object_or_404(
        Matricula,
        id=matricula_id,
        materia_curso__professor=professor
    )

    prova = get_object_or_404(
        Prova,
        id=prova_id,
        materia_curso=matricula.materia_curso
    )

    if request.method == "POST":
        valor = request.POST.get("nota")

        nota = Nota.objects.filter(matricula=matricula, prova=prova).first()
        if nota is None:
            nota = Nota(matricula=matricula, prova=prova)

        nota.nota = valor

        nota.save()


    return redirect('principal:professor_notas', matricula_id=matricula.id)

    
@login_required
def verificacao(request):

    if hasattr(request.user, "aluno"):
        return redirect('principal:aluno_index')

    if hasattr(request.user, "professor"):
            return redirect('principal:professor_index')

def is_aluno(user):
    return hasattr(user, "aluno")


def is_professor(user):
    return hasattr(user, "professor")
