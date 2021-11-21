import rest_framework.request

from django.utils.decorators import method_decorator
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from certificate.models import Certificate
from certificate.serializers import CertificateSerializer
from certificate import swagger_info

class CustomOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({'full_count':self.count,'showed_count':len(data), 'data':data})

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None
        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True
        k = self.offset * self.limit
        if k >= len(queryset):
            return []
        return list(queryset[k:k + self.limit])

class view(ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ('id', 'username', 'birth_date', 'start_date', 'end_date', 'international_passport', 'vaccine')
    pagination_class = CustomOffsetPagination

    @swagger_info.list_post()
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CertificateSerializer(data=data)
        if serializer.validator(data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_info.list_delete()
    def delete(self, request):
        count = Certificate.objects.all().delete()
        return Response({'message': f'{count[0]} сертифікатів успішно видалено'},
                            status=status.HTTP_204_NO_CONTENT)


@method_decorator(
    name="get",
    decorator=swagger_info.detail_get()
)
class detail_view(APIView):

    def get_by_id(self, id):

        try:
            return Certificate.objects.get(pk=id)
        except Certificate.DoesNotExist:
            return Response({'message': 'сертифікату з таким ід не існує'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        obj = self.get_by_id(pk)
        if type(obj) == Response:
            return obj
        serializer = CertificateSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_info.detail_put()
    def put(self, request, pk):
        data = JSONParser().parse(request)
        serializer = CertificateSerializer(data=data)
        if serializer.validator(data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_info.detail_delete()
    def delete(self, request, pk):
        obj = self.get_by_id(pk)
        if type(obj) == Response:
            return obj
        obj.delete()
        return Response({'message': 'Сертифікат успішно видалено'}, status=status.HTTP_204_NO_CONTENT)

