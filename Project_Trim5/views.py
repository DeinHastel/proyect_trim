from django.db import connection
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from .models import Clientes, Proveedores, Producto, Factura, FacturaHasProductos
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
def home(request):
    return render(request,"home/home.html")

#region clientes
def insertar_cliente(request):
    if not request.user.is_authenticated:
        return redirect("/usuario/login")
    if request.method=="POST":
        if request.POST.get("documento") and request.POST.get("nombre") and request.POST.get("telefono"):
            cliente = Clientes()

            cliente.documento = request.POST.get("documento")
            cliente.nombre = request.POST.get("nombre")
            cliente.telefono = request.POST.get("telefono")
            cliente.save()
            return redirect("/")

    else:
        return render(request, "clientes/insertar.html")

def listado_clientes(request):
    if not request.user.is_authenticated:
        return redirect("/usuario/login")
    clientes = Clientes.objects.all()
    
    return render(request, "clientes/listado.html", {"clientes": clientes})

def actualizar_cliente(request, id):
    if request.method=="POST":
        if request.POST.get("nombre") and request.POST.get("documento") and request.POST.get("telefono"):
            clientes = Clientes.objects.get(id=id)
            clientes.id = id
            clientes.nombre = request.POST.get("nombre")
            clientes.documento = request.POST.get("documento")
            clientes.telefono = request.POST.get("telefono")
            clientes.save()

            return redirect("/clientes/listado")
    else: 
        consulta = Clientes.objects.filter(id=id)
        
        return render(request,'clientes/actualizar.html',{"consulta":consulta})
def borrar_cliente(request, id):
    
    borrar = Clientes.objects.get(id=id)
    #interno SQL delete from bla bla
    borrar.delete()
    return redirect("/clientes/listado")

def consultarclienteapi(request,documento):
    cliente = Clientes.objects.filter(documento=documento)
    jsoncliente = serialize('json', cliente)
    return HttpResponse(jsoncliente, content_type="application/json")
#endregion

#region proveedores
def insertar_proveedores(request):
    if request.method=="POST":
        if request.POST.get("documento") and request.POST.get("nombre") and request.POST.get("telefono"):
            proveedores = Proveedores()

            proveedores.documento = request.POST.get("documento")
            proveedores.nombre = request.POST.get("nombre")
            proveedores.telefono = request.POST.get("telefono")
            proveedores.save()
            return redirect("/proveedores/listado")

    else:
        return render(request, "proveedores/insertar.html")
def listado_proveedores(request):
    proveedores = Proveedores.objects.all()
    
    return render(request, "proveedores/listado.html", {"proveedores": proveedores})

def actualizar_proveedor(request, id):
    if request.method=="POST":
        if request.POST.get("nombre") and request.POST.get("documento") and request.POST.get("telefono"):
            proveedores = Proveedores.objects.get(id=id)
            proveedores.id = id
            proveedores.nombre = request.POST.get("nombre")
            proveedores.documento = request.POST.get("documento")
            proveedores.telefono = request.POST.get("telefono")
            proveedores.save()

            return redirect("/proveedores/listado")
    else: 
        consulta = Proveedores.objects.filter(id=id)
        
        return render(request,'proveedores/actualizar.html',{"consulta":consulta})
def borrar_proveedor(request, id):
    
    borrar = Proveedores.objects.get(id=id)
    #interno SQL delete from bla bla
    borrar.delete()
    return redirect("/proveedores/listado")
#endregion

#region producto
def insertar_producto(request):
    if request.method=="POST":
        if request.POST.get("nombre") and request.POST.get("precio") and request.POST.get("descripcion") and request.POST.get("codigo") and request.POST.get("proveedores") and request.FILES["foto"] :
            productos = Producto()

            productos.nombre = request.POST.get("nombre")
            productos.precio = request.POST.get("precio")
            productos.descripcion = request.POST.get("descripcion")
            productos.codigo = request.POST.get("codigo")
            productos.foto = request.FILES["foto"]
            productos.proveedor = Proveedores.objects.get(id=request.POST.get("proveedores") )
            imagen = FileSystemStorage()

            imagen.save(productos.foto.name,productos.foto)
            insertar = connection.cursor()

            insertar.execute("call insertar_producto('"+productos.nombre+"','"+productos.precio+"','"+productos.descripcion+"','"+productos.codigo+"','"+productos.foto.name+"','"+request.POST.get("proveedores")+"')")
            return redirect("/productos/insertar")
        


    else:
        consulta = Proveedores.objects.all()
        return render(request, "productos/insertar.html", {"consulta":consulta})
    
def listado_productos(request):
    productos = Producto()
    productos = connection.cursor()
    productos.execute("call listado_productos")
    
    return render(request, "productos/listar.html", {"productos": productos})

def inactivar_producto(request,id):
    producto = Producto()
    producto = connection.cursor()
    
    producto.execute("call inactivar_producto('"+str(id)+"')")
    
    return redirect("/productos/listado")

def activar_producto(request,id):
    producto = Producto()
    producto = connection.cursor()
    
    producto.execute("call activar_producto('"+str(id)+"')")
    
    return redirect("/productos/listado")

def listado_productos_inactivos(request):
    productos = Producto()
    productos = connection.cursor()
    productos.execute("call listado_productos_inactivos")
    
    return render(request, "productos/listar_inactivos.html", {"productos": productos})

    
def actualizar_producto(request, id):
    if request.method=="POST":
        if request.POST.get("nombre") and request.POST.get("precio") and request.POST.get("descripcion") and request.POST.get("codigo") and request.POST.get("proveedores") :
            productos = Producto()

            productos.nombre = request.POST.get("nombre")
            productos.precio = request.POST.get("precio")
            productos.descripcion = request.POST.get("descripcion")
            productos.codigo = request.POST.get("codigo")
            productos.proveedor = Proveedores.objects.get(id=request.POST.get("proveedores") )
            try: 
                if request.FILES["foto"]:
                    unproducto = Producto.objects.get(id= id)
                    fs = FileSystemStorage()
                    fs.delete(unproducto.foto)
                    productos.foto = request.FILES["foto"]
                    fs.save(productos.foto.name,productos.foto)
                    actualizar = connection.cursor()
                    actualizar.execute("call actualizar_producto('"+str(id)+"','"+productos.nombre+"','"+productos.precio+"','"+productos.descripcion+"','"+productos.codigo+"','"+productos.foto.name+"','"+request.POST.get("proveedores")+"')")
                    return redirect("/productos/listado")
            except:
                actualizar = connection.cursor()
                actualizar.execute("call actualizar_producto('"+str(id)+"','"+productos.nombre+"','"+productos.precio+"','"+productos.descripcion+"','"+productos.codigo+"','"+request.POST.get("foto_vieja")+"','"+request.POST.get("proveedores")+"')")
                return redirect("/productos/listado")
                print()
            
                        
        


    else:
        proveedor = Proveedores.objects.all()
        producto = Producto.objects.filter(id=id)
        return render(request, "productos/actualizar.html",{"producto":producto, "proveedor":proveedor} )
#endregion

#region factura

def insertar_factura(request):
    if request.method=="POST": 
        if request.POST.get("idcliente") and request.POST.get("fechafactura") and request.POST.get("totalfacturainput") and request.POST.get("idproductotabla[]") and request.POST.get("cantidadproductotabla[]") :
            factura = Factura()
            factura.fecha = request.POST.get("fechafactura")
            factura.total = request.POST.get("totalfacturainput")
            factura.cliente = Clientes.objects.get(id=request.POST.get("idcliente"))
            factura.save()
            
            consulta = connection.cursor()
            consulta.execute("call consulta_ultima_factura()")
            idfacturaultimo = 0
            for c in consulta:
                idfacturaultimo = c[0]
            
            arrayidproducto = request.POST.getlist("idproductotabla[]")
            arraycantidadproducto = request.POST.getlist("cantidadproductotabla[]")
            
            for p in range(0,len(arrayidproducto),1):
                facturahasproductos = FacturaHasProductos()
                facturahasproductos.factura = Factura.objects.get(id=idfacturaultimo)
                facturahasproductos.producto = Producto.objects.get(id=arrayidproducto[p])
                facturahasproductos.cantidad = arraycantidadproducto[p]
                facturahasproductos.save()
            
            return redirect("/factura/listado")
            
    else:
        producto = Producto.objects.all()
        return render(request,'factura/infactura.html',{'producto':producto})
    
def listado_factura(request):
    factura = Factura.objects.all()
    
    return render(request, "factura/lisfactura.html", {"factura": factura})

def borrar_factura(request, id):
    
    borrar = Factura.objects.get(id=id)
    #interno SQL delete from bla bla
    borrar.delete()
    return redirect("/factura/listado")

def actualizar_factura(request, id):
    if request.method=="POST":
        if request.POST.get("nombre") and request.POST.get("documento") and request.POST.get("telefono"):
            clientes = Clientes.objects.get(id=id)
            clientes.id = id
            clientes.nombre = request.POST.get("nombre")
            clientes.documento = request.POST.get("documento")
            clientes.telefono = request.POST.get("telefono")
            clientes.save()

            return redirect("/clientes/listado")
    else: 
        consulta = Clientes.objects.filter(id=id)
        
        return render(request,'clientes/actualizar.html',{"consulta":consulta})

def detalle_factura(request, idFactura):
    
    detalle = connection.cursor()
    detalle.execute("call detalle_factura('"+str(idFactura)+"')")
    return render(request,"factura/details.html",{"detalles":detalle})
#endregion


#region usuarios
def insertar_usuario(request):
    
    if request.method == "POST":
        if request.POST.get("username") and request.POST.get("correo") and request.POST.get("nombre") and request.POST.get("pass") and request.POST.get("apellido"):
            usuario = User.objects.create_user(request.POST.get("username"),request.POST.get("correo"),request.POST.get("pass"))
            
            usuario.first_name = request.POST.get("nombre")
            usuario.last_name = request.POST.get("apellido")
            usuario.save()
            
            return redirect("/usuario/login")
    
    else:
        return render(request,"usuarios/insertar.html")
    
def loginusuario(request):
    if request.method == "POST":
        if request.POST.get("username") and request.POST.get("pass"):
            usuario = authenticate(username= request.POST.get("username"), password=request.POST.get("pass"))
            if usuario is not None:
                login(request, usuario)
                return redirect("/")
            else:
                mensaje= "usuario o contraseña incorrectos"
                return render(request, "usuarios/login.html", {"mensaje":mensaje})
    else:
        return render(request,"usuarios/login.html")
def logoutusuario(request):
    logout(request)
    return redirect("/usuario/login")
#endregion