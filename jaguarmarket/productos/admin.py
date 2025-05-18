from django.contrib import admin
from .models import Producto, Categoria
from django.utils.html import format_html

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'publicado_por', 'precio', 'ver_imagen')
    readonly_fields = ('ver_imagen',)

    def ver_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="80" style="border-radius:5px;">', obj.imagen.url)
        return 'Sin imagen'

    ver_imagen.short_description = 'Imagen'

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
