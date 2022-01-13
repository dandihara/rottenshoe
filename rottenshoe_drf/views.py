from rest_framework.response import Response

from rottenshoe_drf.serializer import SneakerSerializer

from .models import Sneakers

# Create your views here.
def index(req):
    queryset = Sneakers.objects.all()
    serializer = SneakerSerializer(queryset,many=True)
    return Response(serializer.data)