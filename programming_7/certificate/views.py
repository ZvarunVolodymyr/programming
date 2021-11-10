import rest_framework.request
from django.shortcuts import render

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from certificate.models import Certificate
from certificate.serializers import CertificateSerializer


class view(ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ('id', 'username', 'birth_date', 'start_date', 'end_date', 'international_passport', 'vaccine')

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CertificateSerializer(data=data)
        if serializer.validator(data):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        count = Certificate.objects.all().delete()
        return JsonResponse({'message': f'{count[0]} сертифікати успішно видалено'},
                            status=status.HTTP_204_NO_CONTENT)


class detail_view(APIView):

    def get_by_id(self, id):
        try:
            return Certificate.objects.get(id=id)
        except Certificate.DoesNotExist:
            return JsonResponse({'message': 'сертифікату з таким ід не існує'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        serializer = CertificateSerializer(self.get_by_id(pk))
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        data = JSONParser().parse(request)
        serializer = CertificateSerializer(data=data)
        if serializer.validator(data):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_by_id(pk).delete()
        return JsonResponse({'message': 'Сертифікат успішно видалено'}, status=status.HTTP_204_NO_CONTENT)

