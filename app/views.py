from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from app.models import Audio

from .serializers import AudioFragmentsSerializer, AudioSerializer


@api_view(["GET"])
def get_routes(request, format=None):

    return Response(
        {
            "Audio elements data": reverse("audio-api", request=request, format=format),
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
        serializer = AudioSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get_queryset(self):
        queryset = Audio.objects.all().prefetch_related('duration')

        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if (start and end) and (start.isdigit() and end.isdigit()):
            self.serializer_class = AudioFragmentsSerializer
            queryset = queryset.filter(
                    duration__start_time__range=(start,end),
                    duration__end_time__range=(start,end)
        
                )
        return queryset

class AudioElementDetailsView(
    generics.DestroyAPIView,
    generics.GenericAPIView,
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

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
