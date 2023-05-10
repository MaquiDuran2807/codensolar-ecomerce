from .models import *
import math

class Product:
  """this class is used to format product

  Returns:
      str: inf just so u know
  """
  default_hours={
  #idcategory:hours
        3:24,
        4:24
  }
  loss = 69
  
  def __init__(self,id,hours_in_use=0,amount=1):
    self.real_product = Products.objects.filter(id=id).values()[0]
    
    self.id = id
    self.hours_in_use = Product.default_hours[ self.real_product["category_id"] ] if hours_in_use == 0 else hours_in_use
    self.amount = amount
    
  def __str__(self):
    return f"""
--
ID:{self.id} ({self.real_product["name"]}) 
Hours to use:{self.hours_in_use}
Amount:{self.amount} 
--
"""

class RequirementQuote:
  """this is a a class that generates a quotation of the requirement asked from the products
  """
  def __init__(self,type_of_requirement,id,amount=1):
    
    self.id = id
    self.amount = amount
    
    
    if type_of_requirement == "panel":
      self.sun_hours = 4
      self.requirement = SolarPanel.objects.get(id=id)
      self.voltage = self.requirement.voltage.voltage
      self.production = {
        'production_hr': self.requirement.production,
        'production_day': self.requirement.production * self.sun_hours,
        'total_production_day': (self.requirement.production * self.sun_hours) * self.amount
      }
      
    elif type_of_requirement == "battery":
      self.requirement = Battery.objects.get(id=id)
      self.capacity = self.requirement.capacity
      self.voltage = self.requirement.voltage.voltage
      
    elif type_of_requirement == "regulator":
      self.requirement = Reguladores.objects.get(id=id)
      
    elif type_of_requirement == "breaker":
      self.requirement = Breakers.objects.get(id=id)
      
    elif type_of_requirement == "rubberized_cable":
      self.requirement = RubberizedCables.objects.get(id=id)
      
    elif type_of_requirement == "vehicle_cable":
      self.requirement = VehicleCables.objects.get(id=id)
      
    elif type_of_requirement == "panel_support":
      self.requirement = PanelSupports.objects.get(id=id)
      
    elif type_of_requirement == "battery_support":
      self.requirement = BatterySupports.objects.get(id=id)
      
    elif type_of_requirement == "ground_security_kit":
      self.requirement = GroundSecurityKits.objects.get(id=id)
      
    elif type_of_requirement == "connector":
      self.requirement = Connectors.objects.get(id=id)
      
    elif type_of_requirement == "terminal":
      self.requirement = Terminals.objects.get(id=id)
      
    elif type_of_requirement == "centralized_module":
      self.requirement = CentralizedModule.objects.get(id=id)
      
    elif type_of_requirement == "unity_power":
      self.requirement = UnityPower.objects.get(id=id)
      
    elif type_of_requirement == "electric_materials":
      self.requirement = ElectricMaterials.objects.get(id=id)
      
    else:
      raise Exception("Not a valid type_of_requierment")
    
    self.name = self.requirement.name
    self.price = self.requirement.price
    del self.requirement

  def __str__(self):
    return f"{self.amount} {self.name} is/are needed"
    
class ProductQuote:
  default_hours={
  #idcategory:hours
        3:24,
        4:24
    }
  default_amount={
  #idcategory:hours
        10:10,
        11:5
    }
  loss_percentaje={
  #idcategory:loss_precentaje
        3:69,
        4:69,
        
        19:29,
        20:29,
        21:29,
    }
  def __init__(self, id, amount,hours_used=0):
    """this class
    generates a complete quote of a product,
    creating a quote for each requirement needed

    Args:
        id (int): id of the product 
        amount (int): amount of products to quote
        hours_used (int): amount of hours to 
    """
    # ------------------------------------------------------------------------------------------------------------------ INFO
    
    self.id = id
    self.product = Products.objects.get(id=self.id)
    self.amount = amount
    self.hours_used = ProductQuote.default_hours[ self.product.category.id ] if hours_used == 0 else hours_used
    
    # ------------------------------------------------------------------------------------------------------------------ REQUIRES
    
    try: kit = Kits.objects.get(product=self.id) #the corresponding kit
    except: kit = 0
    print(kit)
    
    # -------------------------------Panel & battery quote
    
    if kit != 0:
      print("there is a kit")
      panel_id=kit.panel_id
      panel_amount=kit.panel_amount
      battery_id=kit.battery_id
      battery_amount=kit.battery_amount

    else:
      print("there isn't a kit")
      day_consumption = self.product.consume*self.hours_used
      total_day_consumption = day_consumption + ( day_consumption*(ProductQuote.loss_percentaje[self.product.category.id]/100))
      sun_hours = 4
      
      ideal_panel = SolarPanel.objects\
      .filter(production__gte=(total_day_consumption/sun_hours))\
      .order_by("production")\
      [0]
      panel_id=ideal_panel.id
      panel_amount = 1
      
      
      _12v_batteries = Battery.objects.filter(voltage=1).order_by("capacity")
      # print("batteries: ",_12v_batteries)
      
      battery_amount = 1
      if ideal_panel.voltage.voltage >= 12: battery_amount = 2
      
      ideal_battery=list(
        filter(
          lambda battery :((battery.capacity*battery.voltage.voltage)*0.65)*(battery_amount)>=total_day_consumption
          ,_12v_batteries))[0]
      
      battery_id = ideal_battery.id
      
    self.panel_needed = RequirementQuote(
      "panel",
      panel_id,
      panel_amount
    )
    self.battery_needed = RequirementQuote(
      "battery",
      battery_id,
      battery_amount
    )
    
    # -------------------------------regulator & breaker needed
    
    watts_to_support = (self.panel_needed.production["production_hr"] * self.panel_needed.amount) / self.panel_needed.voltage # total wtts / voltage
    print("watts_to_support:",watts_to_support,"\n")
    
    # MISSING FIX IN DB (NO KINDS SHE SAID)
    try:regulator_id = Reguladores.objects.filter(amperios__gte = watts_to_support).order_by("amperios")[0].id 
    except:regulator_id = Reguladores.objects.order_by("-amperios")[0].id
    self.regulator_needed = RequirementQuote(
      "regulator",
      regulator_id
    )
    
    try:breaker_id = Breakers.objects.filter(amps__gte = watts_to_support).order_by("-amps")[0].id 
    except:breaker_id = Breakers.objects.order_by("-amps")[0].id
      
    self.breaker_needed = RequirementQuote(
      "breaker",
      breaker_id,
      3
    )
    
    # -------------------------------cables
    
    try: rubberized_cable_id = (RubberizedCables.objects.filter(supported_amperage__gte=watts_to_support).order_by("supported_amperage"))[0].id
    except: rubberized_cable_id = (RubberizedCables.objects.order_by("-supported_amperage"))[0].id
    self.rubberized_cables_needed = RequirementQuote(
      "rubberized_cable",
      rubberized_cable_id,
      ProductQuote.default_amount[RubberizedCables.objects.get(id=rubberized_cable_id).category.id] #default amount for the cables
    )
    
    try:vehicle_cable_id = (VehicleCables.objects.filter(supported_amperage__gte=watts_to_support).order_by("supported_amperage"))[0].id
    except: vehicle_cable_id = (VehicleCables.objects.order_by("-supported_amperage"))[0].id
    self.vehicle_cables_needed = RequirementQuote(
      "vehicle_cable",
      vehicle_cable_id,
      ProductQuote.default_amount[VehicleCables.objects.get(id=vehicle_cable_id).category.id] #default amount for the cables
    )
    
    # -------------------------------panel supports
    
    self.panel_supports_needed = RequirementQuote(
      "panel_support",
      1,
      panel_amount
    )
    
    # -------------------------------battery supports
    # MISSING FIX (IDK HOW TO CHOOSE OR WICH B.S. EXISTS)
    self.battery_supports_needed = RequirementQuote(
      "battery_support",
      1,
      1
    )
    
    # -------------------------------ground security kit
    
    self.ground_security_kit_needed = RequirementQuote(
      "ground_security_kit",
      1,
      1
    )
    
    # -------------------------------connectors
    output_pairs = panel_amount
    connectors_needed = 0
    while output_pairs > 1:
      print("entre al while")
      x = output_pairs // 2
      output_pairs = x
      connectors_needed += x*2
    
    self.connectors_needed = RequirementQuote(
      "connector",
      1,
      connectors_needed
    )
      
    # -------------------------------terminals
    self.terminals_needed = RequirementQuote(
      "terminal",
      1,
      2
    )
  


    # -------------------------------centralized_module
    self.centralized_modules_needed = RequirementQuote(
      "centralized_module",
      1,
      1
    )
  
    # -------------------------------unity_power
    unity_power_id = 1
    battery = Battery.objects.get(id=battery_id)
    print("category: ",self.product.category.id)
    if self.product.category.id in [3,4]:
      print("capacity: ",battery.capacity)
      try:
        unity_power_id = UnityPower.objects\
        .exclude(id=4)\
        .filter(max_ampers_supported__gte=battery.capacity)\
        .order_by("max_ampers_supported")[0].id
      except:
        unity_power_id = UnityPower.objects\
        .exclude(id=4)\
        .order_by("max_ampers_supported")[0].id
      
    else:
      unity_power_id = 4
      
      
    self.power_units_needed = RequirementQuote(
      "unity_power",
      unity_power_id,
      1
    )
  
    # -------------------------------electric_materials
    # MISSING FIX (IDK HOW TO CHOOSE OR WICH B.S. EXISTS)
    self.electric_materials_needed = RequirementQuote(
      "electric_materials",
      1,
      1
    )

    # ------------------------------------------------------------------------------------------------------------------ COST
    
    self.consumption = {
    'consumption_hr': self.product.consume,
    'consumption_day': self.product.consume * self.hours_used,
    'loss_percentaje': ProductQuote.loss_percentaje[self.product.category.id],
    'loss_consumption': round((self.product.consume * self.hours_used) * (ProductQuote.loss_percentaje[self.product.category.id]/100), 2),
    'total_consumption_day': round((self.product.consume * self.hours_used) + (round((self.product.consume * self.hours_used) * (ProductQuote.loss_percentaje[self.product.category.id]/100), 2)), 2)
}
