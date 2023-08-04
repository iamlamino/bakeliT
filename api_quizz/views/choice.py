from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *


class ChoiceAPIView(generics.CreateAPIView):
    """
    POST api/v1/Choice/
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def post(self, request, format=None):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = Choice.objects.all().order_by('pk')
        serializer = ChoiceSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class ChoiceByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get(self, request, id, format=None):
        try:
            item = Choice.objects.get(pk=id)
            serializer = ChoiceSerializer(item)
            return Response(serializer.data)
        except Choice.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Choice.objects.all().get(pk=id)
        except Choice.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = ChoiceSerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = Choice.objects.all().get(id=kwargs["id"])
        except Choice.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
