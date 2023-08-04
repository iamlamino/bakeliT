from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# clients


class AttemptedQuestionAPIView(generics.CreateAPIView):
    """
    POST api/v1/AttemptedQuestion/
    """
    queryset = AttemptedQuestion.objects.all()
    serializer_class = AttemptedQuestionSerializer

    def post(self, request, format=None):
        serializer = AttemptedQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = AttemptedQuestion.objects.all().order_by('pk')
        serializer = AttemptedQuestionSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class AttemptedQuestionByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = AttemptedQuestion.objects.all()
    serializer_class = AttemptedQuestionSerializer

    def get(self, request, id, format=None):
        try:
            item = AttemptedQuestion.objects.get(pk=id)
            serializer = AttemptedQuestionSerializer(item)
            return Response(serializer.data)
        except AttemptedQuestion.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = AttemptedQuestion.objects.all().get(pk=id)
        except AttemptedQuestion.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = AttemptedQuestionSerializer(
            item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = AttemptedQuestion.objects.all().get(id=kwargs["id"])
        except AttemptedQuestion.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
