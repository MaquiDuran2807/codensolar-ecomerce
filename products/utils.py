from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from io import BytesIO
import os
from xhtml2pdf import pisa
from .models import Products
from django.conf import settings
#importar datetime
from datetime import datetime


def generate_pdf(email,templete,data,nombre,apellido):
    product=[]
    print(data,"esto es data=====================================================================================================")
    contador=0
    totalp=0
    totalup=0
    total_consumo_hr=0
    total_consumo_day=0
    total_perdidas=0
    total_consumo=0
    for i in data["products"]:
        producto= Products.objects.get(id=i["product_id"])
        dir_ip = "http://54.173.145.183/"
        productos={
            "id":producto.id,
            "name":producto.name,
            "imagen":producto.image,
            "price":producto.price,
            "amount":i["amount"],
            "total":producto.price*i["amount"],
            "consumo_h":data["consumptions"][contador]["consumption_hr"],
            "consumo_D":data["consumptions"][contador]["consumption_day"] ,
            "porcentaje":data["consumptions"][contador]["loss_percentaje"] ,
            "perdidas":data["consumptions"][contador]["loss_consumption"],
            "total_MP":data["consumptions"][contador]["total_consumption_day"],    
        }
        product.append(productos)
        totalp+=producto.price*i["amount"]
        totalup +=producto.price
        total_consumo_hr +=data["consumptions"][contador]["consumption_hr"]
        total_consumo_day +=data["consumptions"][contador]["consumption_day"]
        total_perdidas +=data["consumptions"][contador]["loss_consumption"]
        contador+=1
    consumos={
        "total_consumo_hr":round(total_consumo_hr, 2),
        "total_consumo_day":round(total_consumo_day,2),
        "total_perdidas":round(total_perdidas,2),   
        "total_consumo":round(total_consumo_day+total_perdidas,2),
    }
    panel={
        "panel":data["panel_needed"]["name"],
        "panel_precio_u":data["panel_needed"]["price"],
        "amount":data["panel_needed"]["amount"],
        "panel_precio_t":data["panel_needed"]["price"]*data["panel_needed"]["amount"],
        "panel_potencia":data["panel_needed"]["production"] ["production_hr"],
        "panel_potencia_dia":data["panel_needed"]["production"]["production_day"]*data["panel_needed"]["amount"] ,
    }
    bateria={
        "bateria":data["battery_needed"]["name"],
        "bateria_precio_u":data["battery_needed"]["price"],
        "amount":data["battery_needed"]["amount"],
        "bateria_precio_t":data["battery_needed"]["price"]*data["battery_needed"]["amount"],
        "bateria_capacidad":data["battery_needed"]["capacity"] ,
        "bateria_capacidad_t":data["battery_needed"]["capacity"]/data["battery_needed"]["amount"],
    }
    
    # pruebas 
    
    regulador={
        "regulador":data["regulator_needed"]["name"],
        "regulador_precio_u":data["regulator_needed"]["price"],
        "amount":data["regulator_needed"]["amount"],
        "regulador_precio_t":data["regulator_needed"]["price"]*data["regulator_needed"]["amount"],
        # verificar
    }
    
    breakers={
        "breakers":data["breaker_needed"]["name"],
        "breakers_precio_u":data["breaker_needed"]["price"],
        "amount":data["breaker_needed"]["amount"],
        "breakers_precio_t":data["breaker_needed"]["price"]*data["breaker_needed"]["amount"],
        # verificar
    }
    rubberized_cable_needed = {
        "rubberized_cable_needed":data["rubberized_cable_needed"]["name"],
        "rubberized_cable_needed_precio_u":data["rubberized_cable_needed"]["price"],
        "amount":data["rubberized_cable_needed"]["amount"],
        "rubberized_cable_needed_precio_t":data["rubberized_cable_needed"]["price"]*data["rubberized_cable_needed"]["amount"],
        # verificar
    }
    soporte_panel = {
        "soporte_panel":data["panel_support_needed"]["name"],
        "soporte_panel_precio_u":data["panel_support_needed"]["price"],
        "amount":data["panel_support_needed"]["amount"],
        "soporte_panel_precio_t":data["panel_support_needed"]["price"]*data["panel_support_needed"]["amount"],
        # verificar
    }
    centralized_modules_needed = {
        "centralized_modules_needed":data["centralized_modules_needed"]["name"],
        "centralized_modules_needed_precio_u":data["centralized_modules_needed"]["price"],
        "amount":data["centralized_modules_needed"]["amount"],
        "centralized_modules_needed_precio_t":data["centralized_modules_needed"]["price"]*data["centralized_modules_needed"]["amount"],
        # verificar
    }
    power_units_needed= {
        "power_units_needed":data["power_units_needed"]["name"],
        "power_units_needed_precio_u":data["power_units_needed"]["price"],
        "amount":data["power_units_needed"]["amount"],
        "power_units_needed_precio_t":data["power_units_needed"]["price"]*data["power_units_needed"]["amount"],
        # verificar
    }
    terminals_needed= {
        "terminals_needed":data["terminals_needed"]["name"],
        "terminals_needed_precio_u":data["terminals_needed"]["price"],
        "amount":data["terminals_needed"]["amount"],
        "terminals_needed_precio_t":data["terminals_needed"]["price"]*data["terminals_needed"]["amount"],
        # verificar
    }
    connector_needed= {
        "connector_needed":data["connector_needed"]["name"],
        "connector_needed_precio_u":data["connector_needed"]["price"],
        "amount":data["connector_needed"]["amount"],
        "connector_needed_precio_t":data["connector_needed"]["price"]*data["connector_needed"]["amount"],
        # verificar
    }
    vehicle_cable_needed= {
        "vehicle_cable_needed":data["vehicle_cable_needed"]["name"],
        "vehicle_cable_needed_precio_u":data["vehicle_cable_needed"]["price"],
        "amount":data["vehicle_cable_needed"]["amount"],
        "vehicle_cable_needed_precio_t":data["vehicle_cable_needed"]["price"]*data["vehicle_cable_needed"]["amount"],
        # verificar
    }
    electric_materials_needed= {
        "electric_materials_needed":data["electric_materials_needed"]["name"],
        "electric_materials_needed_precio_u":data["electric_materials_needed"]["price"],
        "amount":data["electric_materials_needed"]["amount"],
        "electric_materials_needed_precio_t":data["electric_materials_needed"]["price"]*data["electric_materials_needed"]["amount"],
        # verificar
    }
    ground_security_kit_needed= {
        "ground_security_kit_needed":data["ground_security_kit_needed"]["name"],
        "ground_security_kit_needed_precio_u":data["ground_security_kit_needed"]["price"],
        "amount":data["ground_security_kit_needed"]["amount"],
        "ground_security_kit_needed_precio_t":data["ground_security_kit_needed"]["price"]*data["ground_security_kit_needed"]["amount"],
        # verificar
    }
    total = {
        "total":totalp+panel["panel_precio_t"]+bateria["bateria_precio_t"]+regulador["regulador_precio_t"]+breakers["breakers_precio_t"]+rubberized_cable_needed["rubberized_cable_needed_precio_t"]+soporte_panel["soporte_panel_precio_t"]+centralized_modules_needed["centralized_modules_needed_precio_t"]+power_units_needed["power_units_needed_precio_t"]+terminals_needed["terminals_needed_precio_t"]+connector_needed["connector_needed_precio_t"]+vehicle_cable_needed["vehicle_cable_needed_precio_t"]+electric_materials_needed["electric_materials_needed_precio_t"]+ground_security_kit_needed["ground_security_kit_needed_precio_t"],
        "total_u": totalup+panel["panel_precio_u"]+bateria["bateria_precio_u"]+regulador["regulador_precio_u"]+breakers["breakers_precio_u"]+rubberized_cable_needed["rubberized_cable_needed_precio_u"]+soporte_panel["soporte_panel_precio_u"]+centralized_modules_needed["centralized_modules_needed_precio_u"]+power_units_needed["power_units_needed_precio_u"]+terminals_needed["terminals_needed_precio_u"]+connector_needed["connector_needed_precio_u"]+vehicle_cable_needed["vehicle_cable_needed_precio_u"]+electric_materials_needed["electric_materials_needed_precio_u"]+ground_security_kit_needed["ground_security_kit_needed_precio_u"]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    }

    # Obtener la plantilla HTML
    template = get_template(templete)
    html = template.render({"productos":product,"p":panel,"b":bateria,"r":regulador,"br":breakers,"rc":rubberized_cable_needed,"sp":soporte_panel,"cm":centralized_modules_needed,"pu":power_units_needed,"tr":terminals_needed,"co":connector_needed,"vc":vehicle_cable_needed,"em":electric_materials_needed,"gsk":ground_security_kit_needed,"total":total,"consumos":consumos,"direccion_ip":dir_ip})
    # Crear un archivo PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # Adjuntar el archivo PDF a un correo electrónico y enviarlo
    hoy = datetime.now()
    email = EmailMessage(
        f'Cotización de productos {hoy}',
        f'Hola {nombre} {apellido}, adjunto la cotización de los productos solicitados.',
        'informacion@codensolar.com',
        [email]
    )
    email.attach('archivo.pdf', result.getvalue(), 'application/pdf')
    email.send()
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def generate_pdf_view(templete,data):
    product=[]
    print(data,"esto es data=====================================================================================================")
    contador=0
    totalp=0
    totalup=0
    total_consumo_hr=0
    total_consumo_day=0
    total_perdidas=0
    total_consumo=0
    for i in data["products"]:
        producto= Products.objects.get(id=i["product_id"])
        dir_ip = "http://54.173.145.183/"
        productos={
            "id":producto.id,
            "name":producto.name,
            "imagen":producto.image,
            "price":producto.price,
            "amount":i["amount"],
            "total":producto.price*i["amount"],
            "consumo_h":data["consumptions"][contador]["consumption_hr"],
            "consumo_D":data["consumptions"][contador]["consumption_day"] ,
            "porcentaje":data["consumptions"][contador]["loss_percentaje"] ,
            "perdidas":data["consumptions"][contador]["loss_consumption"],
            "total_MP":data["consumptions"][contador]["total_consumption_day"],    
        }
        product.append(productos)
        totalp+=producto.price*i["amount"]
        totalup +=producto.price
        total_consumo_hr +=data["consumptions"][contador]["consumption_hr"]
        total_consumo_day +=data["consumptions"][contador]["consumption_day"]
        total_perdidas +=data["consumptions"][contador]["loss_consumption"]
        contador+=1
    consumos={
        "total_consumo_hr":round(total_consumo_hr, 2),
        "total_consumo_day":round(total_consumo_day,2),
        "total_perdidas":round(total_perdidas,2),   
        "total_consumo":round(total_consumo_day+total_perdidas,2),
    }
    panel={
        "panel":data["panel_needed"]["name"],
        "panel_precio_u":data["panel_needed"]["price"],
        "amount":data["panel_needed"]["amount"],
        "panel_precio_t":data["panel_needed"]["price"]*data["panel_needed"]["amount"],
        "panel_potencia":data["panel_needed"]["production"] ["production_hr"],
        "panel_potencia_dia":data["panel_needed"]["production"]["production_day"]*data["panel_needed"]["amount"] ,
    }
    bateria={
        "bateria":data["battery_needed"]["name"],
        "bateria_precio_u":data["battery_needed"]["price"],
        "amount":data["battery_needed"]["amount"],
        "bateria_precio_t":data["battery_needed"]["price"]*data["battery_needed"]["amount"],
        "bateria_capacidad":data["battery_needed"]["capacity"] ,
        "bateria_capacidad_t":data["battery_needed"]["capacity"]/data["battery_needed"]["amount"],
    }
    
    # pruebas 
    
    regulador={
        "regulador":data["regulator_needed"]["name"],
        "regulador_precio_u":data["regulator_needed"]["price"],
        "amount":data["regulator_needed"]["amount"],
        "regulador_precio_t":data["regulator_needed"]["price"]*data["regulator_needed"]["amount"],
        # verificar
    }
    
    breakers={
        "breakers":data["breaker_needed"]["name"],
        "breakers_precio_u":data["breaker_needed"]["price"],
        "amount":data["breaker_needed"]["amount"],
        "breakers_precio_t":data["breaker_needed"]["price"]*data["breaker_needed"]["amount"],
        # verificar
    }
    rubberized_cable_needed = {
        "rubberized_cable_needed":data["rubberized_cable_needed"]["name"],
        "rubberized_cable_needed_precio_u":data["rubberized_cable_needed"]["price"],
        "amount":data["rubberized_cable_needed"]["amount"],
        "rubberized_cable_needed_precio_t":data["rubberized_cable_needed"]["price"]*data["rubberized_cable_needed"]["amount"],
        # verificar
    }
    soporte_panel = {
        "soporte_panel":data["panel_support_needed"]["name"],
        "soporte_panel_precio_u":data["panel_support_needed"]["price"],
        "amount":data["panel_support_needed"]["amount"],
        "soporte_panel_precio_t":data["panel_support_needed"]["price"]*data["panel_support_needed"]["amount"],
        # verificar
    }
    centralized_modules_needed = {
        "centralized_modules_needed":data["centralized_modules_needed"]["name"],
        "centralized_modules_needed_precio_u":data["centralized_modules_needed"]["price"],
        "amount":data["centralized_modules_needed"]["amount"],
        "centralized_modules_needed_precio_t":data["centralized_modules_needed"]["price"]*data["centralized_modules_needed"]["amount"],
        # verificar
    }
    power_units_needed= {
        "power_units_needed":data["power_units_needed"]["name"],
        "power_units_needed_precio_u":data["power_units_needed"]["price"],
        "amount":data["power_units_needed"]["amount"],
        "power_units_needed_precio_t":data["power_units_needed"]["price"]*data["power_units_needed"]["amount"],
        # verificar
    }
    terminals_needed= {
        "terminals_needed":data["terminals_needed"]["name"],
        "terminals_needed_precio_u":data["terminals_needed"]["price"],
        "amount":data["terminals_needed"]["amount"],
        "terminals_needed_precio_t":data["terminals_needed"]["price"]*data["terminals_needed"]["amount"],
        # verificar
    }
    connector_needed= {
        "connector_needed":data["connector_needed"]["name"],
        "connector_needed_precio_u":data["connector_needed"]["price"],
        "amount":data["connector_needed"]["amount"],
        "connector_needed_precio_t":data["connector_needed"]["price"]*data["connector_needed"]["amount"],
        # verificar
    }
    vehicle_cable_needed= {
        "vehicle_cable_needed":data["vehicle_cable_needed"]["name"],
        "vehicle_cable_needed_precio_u":data["vehicle_cable_needed"]["price"],
        "amount":data["vehicle_cable_needed"]["amount"],
        "vehicle_cable_needed_precio_t":data["vehicle_cable_needed"]["price"]*data["vehicle_cable_needed"]["amount"],
        # verificar
    }
    electric_materials_needed= {
        "electric_materials_needed":data["electric_materials_needed"]["name"],
        "electric_materials_needed_precio_u":data["electric_materials_needed"]["price"],
        "amount":data["electric_materials_needed"]["amount"],
        "electric_materials_needed_precio_t":data["electric_materials_needed"]["price"]*data["electric_materials_needed"]["amount"],
        # verificar
    }
    ground_security_kit_needed= {
        "ground_security_kit_needed":data["ground_security_kit_needed"]["name"],
        "ground_security_kit_needed_precio_u":data["ground_security_kit_needed"]["price"],
        "amount":data["ground_security_kit_needed"]["amount"],
        "ground_security_kit_needed_precio_t":data["ground_security_kit_needed"]["price"]*data["ground_security_kit_needed"]["amount"],
        # verificar
    }
    total = {
        "total":totalp+panel["panel_precio_t"]+bateria["bateria_precio_t"]+regulador["regulador_precio_t"]+breakers["breakers_precio_t"]+rubberized_cable_needed["rubberized_cable_needed_precio_t"]+soporte_panel["soporte_panel_precio_t"]+centralized_modules_needed["centralized_modules_needed_precio_t"]+power_units_needed["power_units_needed_precio_t"]+terminals_needed["terminals_needed_precio_t"]+connector_needed["connector_needed_precio_t"]+vehicle_cable_needed["vehicle_cable_needed_precio_t"]+electric_materials_needed["electric_materials_needed_precio_t"]+ground_security_kit_needed["ground_security_kit_needed_precio_t"],
        "total_u": totalup+panel["panel_precio_u"]+bateria["bateria_precio_u"]+regulador["regulador_precio_u"]+breakers["breakers_precio_u"]+rubberized_cable_needed["rubberized_cable_needed_precio_u"]+soporte_panel["soporte_panel_precio_u"]+centralized_modules_needed["centralized_modules_needed_precio_u"]+power_units_needed["power_units_needed_precio_u"]+terminals_needed["terminals_needed_precio_u"]+connector_needed["connector_needed_precio_u"]+vehicle_cable_needed["vehicle_cable_needed_precio_u"]+electric_materials_needed["electric_materials_needed_precio_u"]+ground_security_kit_needed["ground_security_kit_needed_precio_u"]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    }

    # Obtener la plantilla HTML
    template = get_template(templete)
    html = template.render({"productos":product,"p":panel,"b":bateria,"r":regulador,"br":breakers,"rc":rubberized_cable_needed,"sp":soporte_panel,"cm":centralized_modules_needed,"pu":power_units_needed,"tr":terminals_needed,"co":connector_needed,"vc":vehicle_cable_needed,"em":electric_materials_needed,"gsk":ground_security_kit_needed,"total":total,"consumos":consumos,"direccion_ip":dir_ip})
    # Crear un archivo PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # Adjuntar el archivo PDF a un correo electrónico y enviarlo
    hoy = datetime.now()
    
    return HttpResponse(result.getvalue(), content_type='application/pdf')
