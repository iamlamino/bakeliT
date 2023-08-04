
from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *
import random
import json

from .model_recommendation import Recommender
# clients

SIM_OPTION = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}


class RecommenderAPIView(generics.CreateAPIView):
    """
    POST api/v1/Tutorial/
    """

    def post(self, request, user__id, format=None):

        recommender_engine = Recommender(sim_options=SIM_OPTION)
        quiz = QuizProfile.objects.all().filter(
            user=user__id)

        last_quiz = []
        list_of_recommandation = {
            'amelioration': []
        }

        list_length = {
            'amelioration': 0
        }
        affiche = []
        for elt in quiz:
            id_elt = elt.parcours.id
            affiche.append(id_elt)
            tmp = QuizProfile.objects.filter(
                parcours=id_elt).latest('completed')
            last_quiz.append(tmp)

        recommender_engine.train_recommenders(user__id)

        i = -1
        for quizprofile in last_quiz:
            i += 1
            categorie = quizprofile.parcours.categorie.all()[0]

            tmp = round(recommender_engine.make_prediction(
                quizprofile.id, categorie.nom)*100)
            tuto = Tutorial.objects.filter(categorie_id=categorie.id)
            tutoriel = random.choice(tuto)

            if tmp < 80:
                if i < 1:
                    list_of_recommandation['amelioration'].append(tutoriel)

        print("Recommendation: ", list_of_recommandation)

        new_tuto = Tutorial.objects.filter(pk=tutoriel.id)

        serializer = TutorialSerializer(new_tuto, many=True)

        data = {
            'quizz': {
                "recommand": serializer.data,

            },
        }

        return Response({"data": data})
