from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.core.exceptions import ValidationError
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile
import io


# Create your models here.


class Imagen(models.Model):
	imagen = models.ImageField(upload_to='imagenes')
	miniatura = models.ImageField(upload_to='imagenes', blank=True, null=True)
	grande = models.ImageField(upload_to='imagenes', blank=True, null=True)


	fecha_subida = models.DateTimeField('fecha subida', auto_now_add=True)

	width = models.IntegerField('ancho', null=True, blank=True)
	height = models.IntegerField('alto', null=True, blank=True)

	descripcion = models.CharField('descripcion', default='', max_length=300)

	nombre = models.CharField('nombre', default='', max_length=200)

	blurBase64 = models.CharField('blur', null=True, blank=True, max_length=800)


	class Meta:
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imagenes'
		ordering = ['-id']  


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		# Abre la imagen original

		img = Image.open(self.imagen)

		if(not(self.width)):
			ancho_original, alto_original = img.size
			self.width = ancho_original
			self.height = alto_original
			self.save()

		nombre = "imagen"


		if(not(self.blurBase64)):
			maximo = (15,15)

			img_blur = img.copy()
			
			img_blur.thumbnail(maximo)
			buffer = BytesIO()
			img_blur.save(buffer, format='webp')
			image_data = buffer.getvalue()
			base64_encoded = base64.b64encode(image_data).decode('utf-8')
			if(len(base64_encoded)<770):
				inicio = 'data:image/png;base64,'
				self.blurBase64 = inicio+base64_encoded
				self.save()
			
			buffer.close()


		if(not(self.miniatura)):
			maximo = (300,300)

			img_small = img.copy()
			
			img_small.thumbnail(maximo)
			buffer = BytesIO()
			img_small.save(buffer, format='webp', quality=80)
			self.miniatura.save(nombre+'_pequeno.webp', InMemoryUploadedFile(buffer, None, nombre, 'image/webp', buffer.tell, None))
			buffer.close()

		if(not(self.grande)):
			maximo = (1000,1000)

			img_small = img.copy()
			
			img_small.thumbnail(maximo)
			buffer = BytesIO()
			img_small.save(buffer, format='webp', quality=80)
			self.grande.save(nombre+'_pequeno.webp', InMemoryUploadedFile(buffer, None, nombre, 'image/webp', buffer.tell, None))
			buffer.close()


class Miniatura(models.Model):
	imagen = models.ImageField(upload_to='imagenes')
	miniatura = models.ImageField(upload_to='imagenes', blank=True, null=True)
	grande = models.ImageField(upload_to='imagenes', blank=True, null=True)


	fecha_subida = models.DateTimeField('fecha subida', auto_now_add=True)

	width = models.IntegerField('ancho', null=True, blank=True)
	height = models.IntegerField('alto', null=True, blank=True)

	descripcion = models.CharField('descripcion', default='', max_length=300)

	nombre = models.CharField('nombre', default='', max_length=50)

	blurBase64 = models.CharField('blur', null=True, blank=True, max_length=800)


	class Meta:
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imagenes'
		ordering = ['-id']  


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		# Abre la imagen original

		img = Image.open(self.imagen)

		if(not(self.width)):
			ancho_original, alto_original = img.size
			self.width = ancho_original
			self.height = alto_original
			self.save()

		nombre = "imagen"


		if(not(self.blurBase64)):
			maximo = (15,15)

			img_blur = img.copy()
			
			img_blur.thumbnail(maximo)
			buffer = BytesIO()
			img_blur.save(buffer, format='webp')
			image_data = buffer.getvalue()
			base64_encoded = base64.b64encode(image_data).decode('utf-8')
			if(len(base64_encoded)<770):
				inicio = 'data:image/png;base64,'
				self.blurBase64 = inicio+base64_encoded
				self.save()
			
			buffer.close()


		if(not(self.miniatura)):
			maximo = (300,300)

			img_small = img.copy()
			
			img_small.thumbnail(maximo)
			buffer = BytesIO()
			img_small.save(buffer, format='webp', quality=80)
			self.miniatura.save(nombre+'_pequeno.webp', InMemoryUploadedFile(buffer, None, nombre, 'image/webp', buffer.tell, None))
			buffer.close()

		if(not(self.grande)):
			maximo = (1000,1000)

			img_small = img.copy()
			
			img_small.thumbnail(maximo)
			buffer = BytesIO()
			img_small.save(buffer, format='webp', quality=80)
			self.grande.save(nombre+'_pequeno.webp', InMemoryUploadedFile(buffer, None, nombre, 'image/webp', buffer.tell, None))
			buffer.close()




def validate_video_file(file):
		valid_mime_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mpeg']
		file_mime_type = file.file.content_type
		if file_mime_type not in valid_mime_types:
				raise ValidationError('Unsupported file type. Only MP4, AVI, MOV, and MPEG are allowed.')

class Video(models.Model):
		video = models.FileField(upload_to='videos/')
		descripcion = models.CharField('descripcion', default='', max_length=300)
		nombre = models.CharField('nombre', default='', max_length=200)
		miniatura = models.ForeignKey(Miniatura, null=True, blank=True, on_delete=models.SET_NULL)

		def create_thumbnail(self):
				if not self.video:
						return
				
				video_path = self.video.path

				# Use moviepy to extract a frame from the video
				clip = VideoFileClip(video_path)
				frame = clip.get_frame(1.00)  # Get frame at 1 second
				image = Image.fromarray(frame)

				# Save the image to a BytesIO object
				thumb_io = io.BytesIO()
				image.save(thumb_io, format='webp')

				# Create a ContentFile from the BytesIO object
				thumb_file = ContentFile(thumb_io.getvalue(), 'miniatura.webp')

				aux = Miniatura(imagen=thumb_file, nombre=f'{self.id}_miniatura.webp')
				aux.save()
				
				self.miniatura=aux
				self.save()
				
				thumb_io.close()


		def save(self, *args, **kwargs):
				
				# First save to ensure the instance has an ID
				if not self.pk:
						super().save(*args, **kwargs)

				# Then create the thumbnail
				if not self.miniatura:
						self.create_thumbnail()

				# Save again to update the instance with the thumbnail
				super().save(*args, **kwargs)	




class Audio(models.Model):
    audio = models.FileField(upload_to='audios/')
    descripcion = models.CharField('descripcion', default='', max_length=300)
    nombre = models.CharField('nombre', default='', max_length=200)
		
	# class Meta:
	# 	verbose_name = 'Audio'
	# 	verbose_name_plural = 'Audios'
	# 	ordering = ['-id']  

	
	