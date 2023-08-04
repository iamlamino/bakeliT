from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *
# clients


class TutorialAPIView(generics.CreateAPIView):
    """
    POST api/v1/Tutorial/
    """
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def post(self, request, format=None):
        serializer = TutorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = Tutorial.objects.all().order_by('pk')
        serializer = TutorialSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class TutorialByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def get(self, request, id, format=None):
        try:
            item = Tutorial.objects.get(pk=id)
            serializer = TutorialSerializer(item)
            return Response(serializer.data)
        except Tutorial.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Tutorial.objects.all().get(pk=id)
        except Tutorial.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = TutorialSerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = Tutorial.objects.all().get(id=kwargs["id"])
        except Tutorial.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
