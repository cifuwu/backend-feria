from rest_framework import status
from .serializers import (ImagenSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage
from storage.models import Imagen




PAGE_SIZE_IMAGENES = 20

class CustomPagination(PageNumberPagination):
    page_size = PAGE_SIZE_IMAGENES
    page_size_query_param = 'page_size'
    max_page_size = 200

    def paginate_queryset(self, queryset, request):
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        #cantidad de páginas
        paginas = paginator.num_pages

        #cantidad de items por página
        largo_pagina = page_size

        #número de página actual
        pagina_actual = int(page_number)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            return {"code": 400, "data": "pagina inválida", "paginas": paginas, "pagina_actual": pagina_actual, "imagenes": []}

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True


        imagenes_serializadas = ImagenSerializer(list(self.page), many=True)


        data = {
            "code": 200,
            "paginas": paginas,
            "pagina_actual": pagina_actual,
            "largo_pagina": largo_pagina,
            "imagenes": imagenes_serializadas.data
        }
        self.request = request
        return data
    


class imagenAPI(APIView):
    pagination_class = CustomPagination

    def get(self, request, pk=None):

        imagenes = Imagen.objects.all()


        imagenes_paginadas = self.pagination_class().paginate_queryset(imagenes, request)


        return Response(imagenes_paginadas, status=status.HTTP_200_OK)
    

    def post(self, request):
        data = request.data 

        fotos_serializadas = ImagenSerializer(data=data)

        if  fotos_serializadas.is_valid():
            fotos_serializadas.save()

            return Response( {"code": 201, "data": fotos_serializadas.data}, status=status.HTTP_201_CREATED)
        return Response( {"code": 400, "errores": fotos_serializadas.errors}, status=status.HTTP_400_BAD_REQUEST)
        