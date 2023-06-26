from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    perdida= models.FloatField(blank=True, null=True, default=39)
    image = models.ImageField(upload_to='media/category',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class ShowCategory (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name= models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.category.name

class Products (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    voltage = models.ManyToManyField("products.Voltage")
    description = models.TextField()
    consume = models.IntegerField()
    caracteristicas = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/Otros')

    def __str__(self):
        return str(str(self.id))+") "+self.name
        
class Otros (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/otros')

    def __str__(self):
        return str(self.id) +") "+self.name
    
class Voltage(models.Model):
    """
    this is an small table to save the voltages
    Args:
        models (_type_): _description_
    """
    voltage = models.IntegerField()
    
    def __str__(self):
        return str(self.voltage)
    

# ===========================================================================

class SolarPanel (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    voltage = models.ForeignKey("products.Voltage", on_delete=models.CASCADE)
    description = models.TextField()
    production = models.IntegerField()
    image = models.ImageField (upload_to='media/SolarPanel',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name

class Battery (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    voltage = models.ForeignKey("products.Voltage", on_delete=models.CASCADE)
    description = models.TextField()
    capacity = models.IntegerField()
    image = models.ImageField(upload_to='media/Battery',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class Reguladores (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amperios = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/Reguladores',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class Inversores (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vatios = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/Inversores')

    def __str__(self):
        return str(self.id) +") "+self.name
    
class soportes (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/soportes')

    def __str__(self):
        return str(self.id) +") "+self.name

class UnidadPotencia (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/UnidadPotencia')

    def __str__(self):
        return str(self.id) +") "+self.name    

class Breakers (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    amps = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/breakers',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class RubberizedCables (models.Model):
    name = models.CharField(max_length=50)
    supported_amperage = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/RubberizedCables',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class VehicleCables (models.Model):
    name = models.CharField(max_length=50)
    supported_amperage = models.IntegerField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/VehicleCables',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class PanelSupports (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/PanelSupport',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class BatterySupports (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/BatterySupports',blank=True, null=True)
    
    def __str__(self):
        return str(self.id) +") "+self.name

class GroundSecurityKits (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/GroundSecurityKits',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name
    
class Connectors (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/Connectors',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name + f" ${self.price}"
    
class Terminals (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/Terminals',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name + f" ${self.price}"
    
class CentralizedModule (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/CentralizedModule',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name + f" ${self.price}"
    
class UnityPower (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='unity_powers')
    battery_kids_supported = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='unity_powers_battery_kids')
    max_ampers_supported = models.IntegerField()
    min_ampers_supported = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/UnityPower',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name + f" ${self.price}"
    
class ElectricMaterials (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/UnityPower',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name + f" ${self.price}"

# ===========================================================================

class KitHogar (models.Model):
    name = models.CharField(max_length=50)
    productos = models.ManyToManyField(Products, related_name='kit_hogar')
    panel= models.ForeignKey(SolarPanel, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    panel_cantidad = models.IntegerField(blank=True,null=True)
    bateria = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    bateria_cantidad = models.IntegerField(blank=True,null=True)
    regulador= models.ForeignKey(Reguladores, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    breakers= models.ForeignKey(Breakers, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    breakers_cantidad = models.IntegerField(default=3,blank=True,null=True)
    cable= models.ForeignKey(RubberizedCables, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    cable_cantidad = models.IntegerField(default=10,blank=True,null=True)
    cable_vehicular= models.ForeignKey(VehicleCables, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    cablevehicular_cantidad = models.IntegerField(default=10,blank=True,null=True)
    panel_suport= models.ForeignKey(PanelSupports, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    panel_suport_cantidad = models.IntegerField(blank=True,null=True)
    unidad_de_potencia= models.ForeignKey(UnityPower, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    modulo_centralizado= models.ForeignKey(CentralizedModule, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    puesta_tierra= models.ForeignKey(GroundSecurityKits, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    conectores= models.ForeignKey(Connectors, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    conectores_cantidad = models.IntegerField(blank=True,null=True)
    terminales= models.ForeignKey(Terminals, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    material_electrico= models.ForeignKey(ElectricMaterials, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    inversor= models.ForeignKey(Inversores, on_delete=models.CASCADE, related_name='kit_hogar',blank=True,null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='media/KitHogar',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name + f" ${self.price}"