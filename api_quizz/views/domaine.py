from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *
# clients


class DomaineAPIView(generics.CreateAPIView):
    """
    POST api/v1/Domaine/
    """
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer

    def post(self, request, format=None):
        serializer = DomaineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = Domaine.objects.all().order_by('pk')
        serializer = DomaineSerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class DomaineByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer

    def get(self, request, id, format=None):
        try:
            item = Domaine.objects.get(pk=id)
            serializer = DomaineSerializer(item)
            return Response(serializer.data)
        except Domaine.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Domaine.objects.all().get(pk=id)
        except Domaine.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = DomaineSerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = Domaine.objects.all().get(id=kwargs["id"])
        except Domaine.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
