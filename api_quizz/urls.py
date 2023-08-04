from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from django.urls import path, include
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Bakeli training API",
        default_version='v1',
        description="backend de cv builder",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('v1/',
         include([
             # docs
             path('docs/', schema_view.with_ui('swagger',
                 cache_timeout=0), name="swagger-schema"),
             # authentification
             path('login/', views.LoginView.as_view()),
             path('logout/', views.LogoutView.as_view()),

             # # user
             path('users/', views.UserAPIView.as_view()),

             # domaine
             path('domaine/', views.DomaineAPIView.as_view()),
             path('domaine/<int:id>', views.DomaineByIdAPIView.as_view()),

             # categorie
             path('category/', views.CategoryAPIView.as_view()),
             path('category/<int:id>', views.CategoryByIdAPIView.as_view()),

             # Parcours
             path('parcours/', views.ParcoursAPIView.as_view()),
             path('parcours/<int:id>', views.ParcoursByIdAPIView.as_view()),

             # Attemptedquestion
             path('attemptedquestion/', views.AttemptedQuestionAPIView.as_view()),
             path('attemptedquestion/<int:id>',
                 views.AttemptedQuestionByIdAPIView.as_view()),

             # Choice
             path('choice/', views.ChoiceAPIView.as_view()),
             path('choice/<int:id>', views.ChoiceByIdAPIView.as_view()),

             # Question
             path('question/', views.QuestionAPIView.as_view()),
             path('question/<int:id>', views.QuestionByIdAPIView.as_view()),

             # Quizz
             path('quizzprofile/', views.QuizProfileAPIView.as_view()),
             path('quizzprofile/<int:id>', views.QuizProfileByIdAPIView.as_view()),
             path('quizzprofile/resultat/<int:id_quizz>',
                 views.ResultatByIdAPIView.as_view()),

             # Tutoriel
             path('tutorial/', views.TutorialAPIView.as_view()),
             path('tutorial/<int:id>', views.TutorialByIdAPIView.as_view()),
             path('play/<int:quiz_profile_id>/<str:completed>',
                 views.PlayAPIView.as_view()),
             path('send_response/<int:question_id>/<int:quiz_profile_id>/<int:response_id>/<str:completed>',
                 views.TraiterQuestionAPIView.as_view()),

             # Recommendation
             path('recommendation/<int:user__id>',
                 views.RecommenderAPIView.as_view()),

         ])
         )
]
