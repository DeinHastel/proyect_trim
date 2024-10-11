"""
URL configuration for Project_Trim5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, insertar_cliente, listado_clientes, actualizar_cliente, borrar_cliente, consultarclienteapi
from .views import insertar_proveedores, listado_proveedores, actualizar_proveedor, borrar_proveedor
from .views import insertar_producto, listado_productos, inactivar_producto, listado_productos_inactivos, activar_producto, actualizar_producto
from .views import insertar_factura, listado_factura, borrar_factura, actualizar_factura, detalle_factura
from .views import insertar_usuario, loginusuario, logoutusuario
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home),
    path("clientes/insertar",insertar_cliente),
    path("clientes/listado",listado_clientes),
    path("clientes/actualizar/<int:id>",actualizar_cliente),
    path("clientes/borrar/<int:id>",borrar_cliente),
    path("cliente/api/<int:documento>", consultarclienteapi),

    path("proveedores/insertar",insertar_proveedores),
    path("proveedores/listado",listado_proveedores),
    path("proveedores/actualizar/<int:id>",actualizar_proveedor),
    path("proveedores/borrar/<int:id>",borrar_proveedor),

    path("productos/insertar", insertar_producto),
    path("productos/listado", listado_productos),
    path("productos/listado_inactivos", listado_productos_inactivos),
    path("productos/inactivar/<int:id>", inactivar_producto),
    path("productos/activar/<int:id>", activar_producto),
    path("productos/actualizar/<int:id>", actualizar_producto ),
    
    path("factura/insertar", insertar_factura),
    path("factura/listado", listado_factura),
    path("factura/borrar/<int:id>", borrar_factura),
    path("factura/actualizar/<int:id>", actualizar_factura),
    path("factura/detalle/<int:idFactura>", detalle_factura),
    
    path("usuario/insertar", insertar_usuario),
    path("usuario/login", loginusuario),
    path("usuario/logout", logoutusuario),
    #path("factura/listado", listado_factura),
    #path("factura/borrar/<int:id>", borrar_factura),
    #path("factura/actualizar/<int:id>", actualizar_factura),
    #path("factura/detalle/<int:idFactura>", detalle_factura),
    
]
