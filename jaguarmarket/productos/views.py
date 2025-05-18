from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, PerfilUsuarioForm, ProductoForm, CustomPasswordChangeForm 
from .models import PerfilUsuario, Producto, Categoria
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from .models import Mensaje




def bienvenida(request):
    return render(request, 'productos/bienvenida.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()  
            perfil = usuario.perfilusuario  
            perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)

            if perfil_form.is_valid():
                perfil_form.save()
                login(request, usuario)
                return redirect('home')
    else:
        form = RegistroForm()
        perfil_form = PerfilUsuarioForm()

    return render(request, 'productos/registro.html', {
        'form': form,
        'perfil_form': perfil_form
    })



def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'productos/login.html')

@login_required
def logout_usuario(request):
    logout(request)
    return redirect('home')

@login_required
def perfil_usuario(request):
    perfil = request.user.perfilusuario
    return render(request, 'productos/perfil_usuario.html', {
        'usuario': request.user,
        'perfil': perfil
    })

@login_required
def publicar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.publicado_por = request.user
            producto.save()
            return redirect('perfil_usuario')
    else:
        form = ProductoForm()
    return render(request, 'productos/publicar_producto.html', {'form': form})

@login_required
def mis_productos(request):
    productos = Producto.objects.filter(publicado_por=request.user)
    return render(request, 'productos/mis_productos.html', {'productos': productos})

@login_required
def explorar_productos(request):
    productos = Producto.objects.exclude(publicado_por=request.user)
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('q')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    return render(request, 'productos/explorar_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'busqueda': busqueda,
    })

@login_required
def editar_mi_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, publicado_por=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mis_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, publicado_por=request.user)
    producto.delete()
    return redirect('mis_productos')


@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    vendedor = producto.publicado_por
    perfil = getattr(vendedor, 'perfilusuario', None)
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'vendedor': vendedor,
        'perfil': perfil,
    })


@login_required
def chat(request, user_id):
    if request.user.id == user_id:
        raise Http404("No puedes chatear contigo mismo.")

    otro = get_object_or_404(User, pk=user_id)

    # Obtener mensajes entre ambos
    mensajes = Mensaje.objects.filter(
        (Q(emisor=request.user) & Q(receptor=otro)) |
        (Q(emisor=otro) & Q(receptor=request.user))
    ).order_by('timestamp')

    # 🔴 MARCAR MENSAJES COMO LEÍDOS
    Mensaje.objects.filter(emisor=otro, receptor=request.user, leido=False).update(leido=True)

    if request.method == 'POST':
        texto = request.POST.get('mensaje', '').strip()
        if texto:
            Mensaje.objects.create(
                emisor=request.user,
                receptor=otro,
                contenido=texto,
                timestamp=timezone.now()
            )
            return redirect('chat', user_id=otro.id)

    return render(request, 'productos/chat.html', {
        'otro': otro,
        'mensajes': mensajes
        
    })

@login_required
def mensajes_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    otro     = producto.publicado_por if request.user != producto.publicado_por else get_object_or_404(User, pk=request.POST.get('destinatario', producto.publicado_por.id))

    # Filtrar solo mensajes de este producto y entre estos dos usuarios
    qs = Mensaje.objects.filter(producto=producto).filter(
        Q(emisor=request.user, receptor=otro) | Q(emisor=otro, receptor=request.user)
    )

    # Marcar como leídos los recibidos
    qs.filter(receptor=request.user, leido=False).update(leido=True)

    if request.method == 'POST':
        texto = request.POST.get('mensaje','').strip()
        if texto:
            Mensaje.objects.create(
                producto=producto,
                emisor=request.user,
                receptor=otro,
                contenido=texto
            )
            return redirect('mensajes_producto', producto_id=producto.id)

    return render(request, 'productos/mensajes_producto.html', {
        'producto': producto,
        'mensajes': qs,
        'otro': otro
    })



@login_required
def mis_conversaciones(request):
    # Productos del vendedor que tienen al menos un mensaje
    productos = Producto.objects.filter(
        publicado_por=request.user,
        mensajes__isnull=False
    ).distinct()
    return render(request, 'productos/mis_conversaciones.html', {
        'productos': productos
    })

@login_required
def mis_chats(request):
    # Chats donde el usuario es emisor o receptor, agrupados por producto
    chats = Mensaje.objects.filter(
        Q(emisor=request.user) | Q(receptor=request.user)
    ).values('producto').distinct()

    # Para cada chat, obtenemos el producto y el conteo de mensajes no leídos
    conversaciones = []
    for entry in chats:
        prod = Producto.objects.get(pk=entry['producto'])
        pendientes = Mensaje.objects.filter(
            producto=prod,
            receptor=request.user,
            leido=False
        ).count()
        conversaciones.append({
            'producto': prod,
            'pendientes': pendientes
        })

    return render(request, 'productos/mis_chats.html', {
        'conversaciones': conversaciones
    })

@login_required
def editar_perfil(request):
    perfil = request.user.perfilusuario
    if request.method == 'POST':
        pform = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
        pass_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        # primero actualizamos teléfono/foto
        if 'perfil_submit' in request.POST and pform.is_valid():
            pform.save()
            messages.success(request, 'Datos de perfil actualizados.')
            return redirect('perfil_usuario')

        # luego actualizamos contraseña
        if 'password_submit' in request.POST and pass_form.is_valid():
            user = pass_form.save()
            update_session_auth_hash(request, user)  # evita logout
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('perfil_usuario')
    else:
        pform      = PerfilUsuarioForm(instance=perfil)
        pass_form  = CustomPasswordChangeForm(user=request.user)

    return render(request, 'productos/editar_perfil.html', {
        'pform': pform,
        'pass_form': pass_form
    })


def home(request):
    if request.user.is_authenticated:
        # Si está logueado, le mostramos su dashboard personalizado
        return render(request, 'productos/home_auth.html', {
            'usuario': request.user
        })
    # Si no, la bienvenida genérica
    return render(request, 'productos/bienvenida.html')


def acerca(request):
    return render(request, 'productos/acerca.html')

def estudio_factibilidad(request):
    return render(request, 'productos/estudio_factibilidad.html')

def estudio_mercado(request):
    return render(request, 'productos/estudio_mercado.html')

def estudios_sociologicos(request):
    return render(request, 'productos/estudios_sociologicos.html')

def estudios_etnograficos(request):
    return render(request, 'productos/estudios_etnograficos.html')

def estudios_axiologicos(request):
    return render(request, 'productos/estudios_axiologicos.html')