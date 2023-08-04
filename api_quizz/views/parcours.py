from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *
# clients


class ParcoursAPIView(generics.CreateAPIView):
    """
    POST api/v1/Parcours/
    """
    queryset = Parcours.objects.all()
    serializer_class = ParcoursSerializer

    def post(self, request, format=None):
        serializer = ParcoursSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = Parcours.objects.all().order_by('pk')
        serializer = ParcoursSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class ParcoursByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Parcours.objects.all()
    serializer_class = ParcoursSerializer

    def get(self, request, id, format=None):
        try:
            item = Parcours.objects.get(pk=id)
            serializer = ParcoursSerializer(item)
            return Response(serializer.data)
        except Parcours.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Parcours.objects.all().get(pk=id)
        except Parcours.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = ParcoursSerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = Parcours.objects.all().get(id=kwargs["id"])
        except Categorie.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
