from api_quizz.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import *
# clients


class CategoryAPIView(generics.CreateAPIView):
    """
    POST api/v1/Categorie/
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        # return Response( status=400)

    def get(self, request, format=None):
        items = Categorie.objects.all().order_by('pk')
        serializer = CategorySerializer(items, many=True)
        return Response({"count": items.count(), "data": serializer.data})


class CategoryByIdAPIView(generics.CreateAPIView):
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, id, format=None):
        try:
            item = Categorie.objects.get(pk=id)
            serializer = CategorySerializer(item)
            return Response(serializer.data)
        except Categorie.DoesNotExist:
            return Response({
                "status": 404,
                "message": "no such item with this id",
            }, status=404)

    def put(self, request, id, format=None):
        try:
            item = Categorie.objects.all().get(pk=id)
        except Categorie.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        self.data = request.data.copy()
        serializer = CategorySerializer(item, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            item = Categorie.objects.all().get(id=kwargs["id"])
        except Categorie.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item with this id",
            }, status=404)
        item.delete()
        return Response({"message": "deleted"}, status=204)
