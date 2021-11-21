from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from certificate.serializers import CertificateSerializer

properties = {
                "id": openapi.Schema(description='id id certificate', type=openapi.TYPE_INTEGER),
                'username': openapi.Schema(description='name, only chars', type=openapi.TYPE_STRING),
                'birth_date': openapi.Schema(description='date of birth', type=openapi.FORMAT_DATE),
                'start_date': openapi.Schema(description='start date of certificate', type=openapi.FORMAT_DATE),
                'end_date': openapi.Schema(description='end date of certificate', type=openapi.FORMAT_DATE),
                'international_passport': openapi.Schema(description='passoport code, AA###### - format(A-letters, '
                                                                     '#-numbers', type=openapi.TYPE_STRING),
                'vaccine': openapi.Schema(description="vaccine, from list - ['pfizer', 'moderna', 'AstraZeneca']",
                                          type=openapi.TYPE_STRING),
            }
example = {
                'username': 'name',
                "birth_date": "2001-1-1",
                "start_date": "2001-5-1",
                "end_date": "2001-6-1",
                "international_passport": "aa000000",
                "vaccine": "pfizer"
            }


def list_post():
    return swagger_auto_schema(
        operation_description="post new certificate",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'birth_date', 'start_date', 'end_date', 'international_passport', 'vaccine'],

            properties=properties,
            example=example),
            responses={
                201: openapi.Response(
                    description="certificate added successful",
                    examples={
                        'application/json': {
                            'message': str(example),
                            'status': '201'}
                    }
                ),
                400: openapi.Response(
                    description="certificate invalid",
                    examples={
                        'application/json': {
                            'message': "ab1 : не є ім'ям",
                            'status': '400'}
                    }
                )
            }
    )


def list_delete():
    return swagger_auto_schema(
        operation_description="remove all certificates",
        responses={
            204: openapi.Response(
                description="certificates deleted",
                examples={
                    'application/json':{
                    'message': f'{5} сертифікатів успішно видалено',
                    'status': '204'}
                }
            )
        }
    )


def detail_put():
    return swagger_auto_schema(
        operation_description="change certificate by id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'birth_date', 'start_date', 'end_date', 'international_passport', 'vaccine'],
            properties=properties,
            example=example
        ),
        responses={
            200: openapi.Response(
                description="certificate changed successful",
                examples={
                    'application/json': {
                        'message': str(example),
                        'status': '200'}
                }
            ),
            400: openapi.Response(
                description="certificate invalid",
                examples={
                    'application/json': {
                        'message':  "ab1 : не є ім'ям",
                        'status': '400'}
                }
            ),
            404: openapi.Response(
                description="invalid id",
                examples={
                    'application/json': {
                        'message': "сертифікату з таким ід не існує",
                        'status': '404'}
                }
            )
        },
        tags=['detail']
    )


def detail_get():
    return swagger_auto_schema(
        operation_description="return certificate by id",
        tags=['detail'],
        responses={
                    200: openapi.Response(
                        description="success",
                        examples={
                            'application/json': {
                                'message': str(example),
                                'status': '200'}
                        }
                    ),
                    404: openapi.Response(
                        description="invalid id",
                        examples={
                            'application/json': {
                                'message': "сертифікату з таким ід не існує",
                                'status': '404'}
                        }
                    )
        }
    )


def detail_delete():
    return swagger_auto_schema(
        operation_description="delete certificate by id",
        tags=['detail'],
        responses={
            204: openapi.Response(
                description="certificate deleted",
                examples={
                    'application/json': {
                        'message': f'сертифікат успішно видалено',
                        'status': '204'}
            }
            ),
            404: openapi.Response(
                description="invalid id",
                examples={
                    'application/json': {
                        'message': "сертифікату з таким ід не існує",
                        'status': '404'}
                }
            )
        }
    )
