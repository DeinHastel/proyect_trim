from django.db import models

class Clientes(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=65)
    telefono = models.CharField(max_length=15)
    class Meta:
        db_table = 'clientes'

class Proveedores(models.Model):
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=65)
    telefono = models.CharField(max_length=15)
    class Meta:
        db_table = 'proveedores'

class Producto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20)
    foto = models.CharField(max_length=255)
    proveedor = models.ForeignKey(to='proveedores', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    class Meta:
        db_table = "producto"
        
class Factura(models.Model):
        fecha = models.CharField(max_length=255)
        total = models.BigIntegerField()
        cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
        class Meta:
            db_table="factura"
            
class FacturaHasProductos(models.Model):
        factura = models.ForeignKey(Factura,  on_delete=models.CASCADE)
        producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
        cantidad = models.IntegerField()
        class Meta:
            db_table="facturahasproductos"        