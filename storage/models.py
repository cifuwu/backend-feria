from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64


# Create your models here.



class Imagen(models.Model):
	imagen = models.ImageField(upload_to='imagenes')
	miniatura = models.ImageField(upload_to='imagenes', blank=True, null=True)
	grande = models.ImageField(upload_to='imagenes', blank=True, null=True)


	fecha_subida = models.DateTimeField('fecha subida', auto_now_add=True)

	width = models.IntegerField('ancho', null=True, blank=True)
	height = models.IntegerField('alto', null=True, blank=True)

	blurBase64 = models.CharField('blur', null=True, blank=True, max_length=800)


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

