from . import views
from django.urls import path

app_name = 'principal'

urlpatterns = [
    path('aluno/index/', views.menu_aluno, name = "aluno_index"),
    path('professor/index/', views.menu_professor, name = "professor_index"),
    path('verificacao/', views.verificacao, name = "verificacao"),
    path('aluno_materia/<int:matricula_id>/', views.aluno_materia, name = "aluno_materia"),
    path('professor_materia/<int:materia_id>/', views.professor_materia, name = "professor_materia"),
    path('professor_notas/<int:matricula_id>/', views.professor_notas, name = "professor_notas"),
    path('professor_notas/<int:matricula_id>/lancar/<int:prova_id>/', views.lancar_nota, name = "lancar_nota"),
]