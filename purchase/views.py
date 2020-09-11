from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import PurchaseModel, PurchaseStatusModel
from .serializers import PurchaseSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.http.request import QueryDict
from core.common import random_date


class PurchaseViewSet(viewsets.ViewSet):
    """
        A simple ViewSet for the movies.
    """
    model = PurchaseModel
    serializer_class = PurchaseSerializer
    queryset = model.objects.all()

    def list(self, request):
        """
            To list the movies
            URL Structure: /movie/
            Required Fields: None
        """
        import random
        from django.db.models import Avg, Count

        queryset = PurchaseStatusModel.objects.all().extra(select={'month': '%s' % ("EXTRACT(month FROM created_at)",)})\
            .values('month').annotate(count=Count('purchase__quantity'))

        if queryset:
            import calendar
            queryset = sorted(queryset, key=lambda x: x['month'])
            data = {
                'xAxis': list(map(lambda x:int(x['month']), queryset)),
                'yAxis': list(map(lambda x:x['count'], queryset))
            }
            print(data)
            return render(request, 'purchase/index.html', {'data': data})
        else:
            name_list = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10"]
            status_tuple = ('open', 'verified', 'dispatched', 'delivered')
            for i in range(5000):
                purchase_status = [
                    {"status": i, "created_at": random_date("2019-01-01T05:00:00Z", "2020-03-31T22:00:00Z", random.random())}
                    for i in status_tuple]
                data = {
                    "purchaser_name": random.choice(name_list),
                    "quantity": random.randrange(1, 10),
                    "purchase_status": purchase_status
                }
                serializer = self.serializer_class(data=data)

                if serializer.is_valid():
                    serializer.save()
            return Response("Success")




    def create(self, request):
        """
            To create the movies
            URL Structure: /movie/
            Required Fields: 'name', 'director', 'genre', 'popularity','imdb_score'
        """
        # To create movies bulky using file by pandas
        if 'upload_file' in request.data:
            df = pd.read_json(request.FILES['upload_file'])
            df.rename(columns={"99popularity": "popularity"}, inplace=True)

            objs = [
                Movie(
                    name=e.name,
                    director=e.director,
                    genre=','.join(e.genre),
                    popularity=e.popularity,
                    imdb_score=e.imdb_score
                )
                for e in df.itertuples()
            ]
            self.model.objects.bulk_create(objs)
            return Response({'msg':'Success'}, status=200)

        # For create movie
        data = QueryDict.dict(request.data)
        genre = data.get('genre', '')

        data['genre'] = ','.join(genre) if genre and isinstance(genre, list) else genre
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)