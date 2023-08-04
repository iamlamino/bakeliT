
import random
from traceback import print_tb
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from api_quizz.models import *
from api_quizz.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
NUMBER_OF_QUESTIONS = 5


def new_question(quiz_profile_id, completed):
    quiz_profile = QuizProfile.objects.get(pk=quiz_profile_id)

    parcours = quiz_profile.parcours
    # parcoursSerializer = ParcoursSerializer(parcours)

    categorie = parcours.categorie.all()

    used_questions = AttemptedQuestion.objects.filter(
        quiz_profile=quiz_profile.id).values_list('question', flat=True)
    used_questions_pk = used_questions.all().values_list('question')
    print("USED QUESTIONS PK: ", used_questions)

    if used_questions_pk:
        remaining_questions = Question.objects.exclude(
            pk__in=used_questions_pk).filter(categorie_id=categorie[0].id)
    else:
        remaining_questions = Question.objects.all().filter(
            categorie_id=categorie[0].id)
    # new_question =

    random_question = random.choice(remaining_questions)

    reponses = random_question.choices.all()
    allReponse = ChoiceSerializer(reponses, many=True)

    new_question = QuestionSerializer(random_question)

    data = {
        'quizz': {
            "question": new_question.data,
            "reponses": allReponse.data,
        },
    }

    return Response({"data": data})


class PlayAPIView(APIView):
    """
    POST api/v1/Question/
    """

    def post(self, request, quiz_profile_id, completed):
        return new_question(quiz_profile_id, completed)


class TraiterQuestionAPIView(APIView):
    """
    POST api/v1/Question/
    """

    def post(self, request, question_id, quiz_profile_id, response_id, completed):

        if (completed == "false" or completed == "False"):
            question_traite = Question.objects.get(pk=question_id)
            response_donnee = Choice.objects.get(pk=response_id)
            quiz_profile = QuizProfile.objects.get(pk=quiz_profile_id)

            '''print("QUESTION: {} and RESPONSE: {} and QUIZ: {}".format(
                question_id, response_id, quiz_profile_id))
            print("********************************************\n")
            print("QUESTION: {} and RESPONSE: {} and QUIZ: {}".format(
                question_traite, response_donnee, quiz_profile))'''
            # if question_traite is not None:
            attempted_question = AttemptedQuestion(
                question=question_traite, quiz_profile=quiz_profile)
            attempted_question.save()
            # else:
            attempted_question = quiz_profile.attempts.select_related(
                'question').get(question_id=question_id)

            # debut
            quiz_profile.evaluate_attempt(attempted_question, response_donnee)
            return new_question(quiz_profile_id, completed)

        else:
            quiz_profile = QuizProfile.objects.get(pk=quiz_profile_id)
            quiz_profile.complete_quizz()
            quiz_profile.update_score()
            data = QuizProfileSerializer(quiz_profile)
            return Response({"resultat": data.data})
