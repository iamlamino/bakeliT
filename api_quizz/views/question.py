from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *
# clients


class QuestionAPIView(generics.CreateAPIView):
    """
    POST api/v1/Question/
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = Question.objects.all().order_by('pk')
        serializer = QuestionSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class QuestionByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, id, format=None):
        try:
            item = Question.objects.get(pk=id)
            serializer = QuestionSerializer(item)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Question.objects.all().get(pk=id)
        except Question.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = QuestionSerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = Question.objects.all().get(id=kwargs["id"])
        except Question.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
