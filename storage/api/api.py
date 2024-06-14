from rest_framework import status
from .serializers import ImagenSerializer, VideoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage
from storage.models import Imagen, Video
import mimetypes







class FileUploadAPI(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        mime_type, _ = mimetypes.guess_type(file.name)
        if not mime_type:
            return Response({'error': 'Cannot determine file type'}, status=status.HTTP_400_BAD_REQUEST)

        if mime_type.startswith('image'):
            print('imagen')

            foto_serializada = ImagenSerializer(data={'imagen': file})

            if  foto_serializada.is_valid():
                foto_serializada.save()

                return Response( {"code": 201, "data": foto_serializada.data}, status=status.HTTP_201_CREATED)
            
            print(foto_serializada.errors)
            
            return Response( {"code": 400, "errores": foto_serializada.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            
        elif mime_type.startswith('video'):
            print('video')

            video_serializado = VideoSerializer(data={'video': file})

            if  video_serializado.is_valid():
                video_serializado.save()

                return Response( {"code": 201, "data": video_serializado.data}, status=status.HTTP_201_CREATED)
            
            print(video_serializado.errors)
            
            return Response( {"code": 400, "errores": video_serializado.errors}, status=status.HTTP_400_BAD_REQUEST)
            

        elif mime_type.startswith('audio'):
            print('audio')
        else:
            print('archivo desconocido')




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
    

    def delete(self, request, pk=None):
        if(pk!=None):
            try:
                instancia = Imagen.objects.get(pk=pk)
                instancia.delete()
                return Response({'code': 200, 'data':'imagen eliminada correctamente'},status=status.HTTP_200_OK)
            except Imagen.DoesNotExist:
                return Response({'code': 400, 'data':'imagen no encontrada'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'code': 400, 'data':'indique el id de la imagen'},status=status.HTTP_400_BAD_REQUEST)
        


PAGE_SIZE_VIDEOS = 20

class CustomPaginationVideo(PageNumberPagination):
    page_size = PAGE_SIZE_VIDEOS
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
            return {"code": 400, "data": "pagina inválida", "paginas": paginas, "pagina_actual": pagina_actual, "videos": []}

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True


        videos_serializados = VideoSerializer(list(self.page), many=True)


        data = {
            "code": 200,
            "paginas": paginas,
            "pagina_actual": pagina_actual,
            "largo_pagina": largo_pagina,
            "videos": videos_serializados.data
        }
        self.request = request
        return data
      


class videoAPI(APIView):
    pagination_class = CustomPaginationVideo

    def get(self, request, pk=None):

        videos = Video.objects.all()


        videos_paginados = self.pagination_class().paginate_queryset(videos, request)


        return Response(videos_paginados, status=status.HTTP_200_OK)
    

    def post(self, request):
        data = request.data 

        videos_serializados = VideoSerializer(data=data)

        if videos_serializados.is_valid():
            videos_serializados.save()

            return Response( {"code": 201, "data": videos_serializados.data}, status=status.HTTP_201_CREATED)
        return Response( {"code": 400, "errores": videos_serializados.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None):
        if(pk!=None):
            try:
                instancia = Video.objects.get(pk=pk)
                instancia.delete()
                return Response({'code': 200, 'data':'video eliminado correctamente'},status=status.HTTP_200_OK)
            except Imagen.DoesNotExist:
                return Response({'code': 400, 'data':'video no encontrado'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'code': 400, 'data':'indique el id del video'},status=status.HTTP_400_BAD_REQUEST)
        
