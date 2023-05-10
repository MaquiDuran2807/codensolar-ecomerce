from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    perdida= models.FloatField(blank=True, null=True, default=39)
    image = models.ImageField(upload_to='media/category',blank=True, null=True)

    def __str__(self):
        return str(self.id) +") "+self.name

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

class Kits (models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    panel = models.ForeignKey(SolarPanel, on_delete=models.CASCADE)
    panel_amount = models.IntegerField()
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE)
    battery_amount = models.IntegerField()
    def __str__(self):
        return "kit del producto "+ str(self.product)
    
class HomeKits (models.Model):
    name = models.CharField(max_length=25,default="KIT - SOLAR---CODEN")
    panel = models.ForeignKey(SolarPanel, on_delete=models.CASCADE)
    panel_amount = models.IntegerField()
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE)
    battery_amount = models.IntegerField()
    def __str__(self):
        return f"{str(self.id)}) {self.name}"
    
class HomeKits_Products (models.Model):
    kit = models.ForeignKey(HomeKits, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.kit} -> {self.product}({str(self.amount)})"