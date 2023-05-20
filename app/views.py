from django.db.models import Q
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from app.models import Audio

from .serializers import AudioSerializer


@api_view(["GET"])
def get_routes(request, format=None):

    return Response(
        {
            "Audio elements data": reverse("audio-api", request=request, format=format),
           # "users profiles data": reverse("audio-details-api", request=request, format=format),
        }
    )


class AudioListView(
    generics.ListAPIView,
    generics.CreateAPIView,
):
    serializer_class = AudioSerializer

    def get(self, request, format=None):
        return self.list(request)

    def post(self, request, format=None):
        data = request.data
        print(data)
        serializer = AudioSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Audio.objects.all()
        return queryset


class AudioElementDetailsView(
    generics.GenericAPIView,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)

    def post(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
