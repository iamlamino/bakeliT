from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
# clients


class QuizProfileAPIView(generics.CreateAPIView):
    """
    POST api/v1/QuizProfile/
    """
    queryset = QuizProfile.objects.all()
    serializer_class = QuizProfileSerializer

    def post(self, request, format=None):
        serializer = QuizProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = QuizProfile.objects.all().order_by('pk')
        serializer = QuizProfileSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class QuizProfileByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = QuizProfile.objects.all()
    serializer_class = QuizProfileSerializer

    def get(self, request, id, format=None):
        try:
            item = QuizProfile.objects.get(pk=id)
            serializer = QuizProfileSerializer(item)
            return Response(serializer.data)
        except QuizProfile.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = QuizProfile.objects.all().get(pk=id)
        except QuizProfile.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = QuizProfileSerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = QuizProfile.objects.all().get(id=kwargs["id"])
        except QuizProfile.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)


class ResultatByIdAPIView(APIView):

    def get(self, request, id_quizz, format=None):
        try:
            print("id quizz", id_quizz)
            item = AttemptedQuestion.objects.filter(quiz_profile=id_quizz)
            print("item", item)
            serializer = AttemptedQuestionSerializer(item, many=True)
            return Response(serializer.data)
        except AttemptedQuestion.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)
