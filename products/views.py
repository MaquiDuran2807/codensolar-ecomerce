from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# importar jsonresponse
from django.http import HttpRequest, HttpResponse, JsonResponse,FileResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse_lazy, reverse
from .utils import *
from os import system
from .classes import *
from functools import reduce
# comentado porque no dejaba iniciar el servidor revisar
# from .pdf import create_pdf
from .send_mail import send_mail
from django.http import HttpResponseRedirect
from django.core.cache import cache

# Create your views here.

class vistaprueba(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request):
        print(request.body)
        data=json.loads(request.body)
        if data==[]:
            #borrar cache
            cache.delete(request.user.username)
            return JsonResponse({"error":"no hay datos"})
        usuario=request.user
        print(usuario.username)
        if data == {}:
            data=cache.get(usuario.username)
            if data==None:
                return JsonResponse({"error":"no hay datos"})
        cache.set(usuario.username,data,5000)
        products_consumptions=[]
        total_consumo_productos=0
        productos=[]
        for d in data:
            print(d)
            product=Products.objects.get(id=d["product_id"])
            calculo_diario=product.consume*d["hours"]
            porcentaje_perdidas=(Category.objects.get(id=product.category_id).perdida)
            calculo_perdidas=(calculo_diario*porcentaje_perdidas)/100
            total_consumo_productos+=(calculo_diario+calculo_perdidas)*d["amount"]
            comsumtion={
                "consumption_hr":product.consume,
                "consumption_day":calculo_diario,
                "loss_percentaje":porcentaje_perdidas,
                "loss_consumption":calculo_perdidas,
                "total_consumption_day":calculo_diario+calculo_perdidas,
                "tota_xcantidad":(calculo_diario+calculo_perdidas)*d["amount"],
            }
            print(comsumtion,"comsumtion=====================")
            products_consumptions.append(comsumtion)
            productos.append({
                "amount":d["amount"],
                "name":product.name,
                "price":product.price,
                "id":product.id,
                "hours_used":d["hours"],
            })
        # traer una lista de todos los paneles
        paneles=list(SolarPanel.objects.all().values())
        paneles=sorted(paneles, key=lambda panel: panel["production"],reverse=False)
        # traer una lista de todas las baterias
        baterias=list(Battery.objects.all().values())
        # traer una lista de todos los inversores

        panel_apropiado=0
        contador_paneles=0
        while panel_apropiado==0:
            contador_paneles +=1
            for p in paneles:
                pdrocuccion=(p["production"]*4)*contador_paneles
                if pdrocuccion>=total_consumo_productos:
                    panel_apropiado=p
                    break
            
        panel_need={
            "amount": contador_paneles,
            "production": {
            "production_hr":panel_apropiado["production"] ,
            "production_day":panel_apropiado["production"]*4 ,
            "total_production_day": pdrocuccion
        },
        "name": panel_apropiado["name"],
        "price": panel_apropiado["price"],
        }
        bateria_apropiada=0
        contardor_baterias=0
        voltage_sistema=Voltage.objects.get(id=panel_apropiado["voltage_id"]).voltage
        baterias=sorted(baterias, key=lambda bateria: bateria["capacity"],reverse=False)
        loss_bat=calculo_diario*0.65
        while bateria_apropiada==0:
            contardor_baterias +=1
            for b in baterias:
                capacidad=b["capacity"]*voltage_sistema*contardor_baterias
                print(b,"bateria ====================== ",capacidad, Voltage.objects.get(id=b["voltage_id"]).voltage,total_consumo_productos*2,contardor_baterias)
                if Voltage.objects.get(id=b["voltage_id"]).voltage==12 and capacidad>=total_consumo_productos*2 :
                    bateria_apropiada=b
                    break
        if voltage_sistema==24:
            contardor_baterias *=2
        bateria_apropiada={
            "amount": contardor_baterias,
            "capacity": capacidad,
            "name": bateria_apropiada["name"],
            "price": bateria_apropiada["price"],
        }

        #regulador 
        reguladores=list(Reguladores.objects.all().values())
        reguladores=sorted(reguladores, key=lambda regulador: regulador["amperios"],reverse=False)
        regulador_apropiado=0
        amp_requerido=(panel_apropiado["production"]/voltage_sistema)*contador_paneles
        print(amp_requerido,"amp_requerido")
        
        for r in reguladores:
            if r["amperios"]>=amp_requerido:
                regulador_apropiado=r
                break
        if regulador_apropiado==0:
            regulador_apropiado=reguladores[-1]
        regulador_apropiado={
            "amount": 1,
            "name": regulador_apropiado["name"],
            "price": regulador_apropiado["price"],
        }
        #breakers
        breakers=list(Breakers.objects.all().values())
        breakers=sorted(breakers, key=lambda breaker: breaker["amps"],reverse=False)
        breaker_apropiado=0
        for be in breakers:
            if be["amps"]>=amp_requerido:
                breaker_apropiado=be
                break
        if breaker_apropiado==0:
            breaker_apropiado=breakers[-1]
        breaker_apropiado={
            "amount": 3,
            "name": breaker_apropiado["name"],
            "price": breaker_apropiado["price"],    
        }
        #cables encauchetados
        cables_encauchetados=list(RubberizedCables.objects.all().values())
        cables_encauchetados=sorted(cables_encauchetados, key=lambda cable: cable["supported_amperage"],reverse=False)
        cable_encauchetado_apropiado=0
        
        for c in cables_encauchetados:
            if c["supported_amperage"]>=amp_requerido:
                cable_encauchetado_apropiado=c
                break
        if cable_encauchetado_apropiado==0:
            cable_encauchetado_apropiado=cables_encauchetados[-1]
        cable_encauchetado_apropiado={
            "amount": 10,
            "name": cable_encauchetado_apropiado["name"],
            "price": cable_encauchetado_apropiado["price"],
        }
        #soporte de panel
        soporte_panel=list(PanelSupports.objects.all().values())
        soporte_panel={
            "amount": contador_paneles,
            "name": soporte_panel[0]["name"],
            "price": soporte_panel[0]["price"],
        }
        #modulo centralizado
        modulo_centralizado=list(CentralizedModule.objects.all().values())
        modulo_centralizado={
            "amount": 1,
            "name": modulo_centralizado[0]["name"],
            "price": modulo_centralizado[0]["price"],
        }
        #unidad de potencia
        unidad_potencia=list(UnityPower.objects.all().values())
        unidad_potencia=sorted(unidad_potencia, key=lambda unidad: unidad["max_ampers_supported"],reverse=False)
        unidad_potencia_adeacuada=0
        for u in unidad_potencia:
            print(u["max_ampers_supported"],u["min_ampers_supported"],b["capacity"])
            if u["max_ampers_supported"]>=b["capacity"] and u["min_ampers_supported"]<=b["capacity"]:
                unidad_potencia_adeacuada=u
                break
        if unidad_potencia_adeacuada==0:
            unidad_potencia_adeacuada={
                "amount": 0,
                "name": "no hay unidad de potencia adecuada",
                "price": 0,
            }
        else:
            unidad_potencia_adeacuada={
                "amount": 1,
                "name": unidad_potencia_adeacuada["name"],
                "price": unidad_potencia_adeacuada["price"],
            }
        #terminal
        terminal=list(Terminals.objects.all().values())
        terminal={
            "amount": 1,
            "name": terminal[0]["name"],
            "price": terminal[0]["price"],
        }
        #conector
        list_pares=[]
        for i in range(0,20,2):
            list_pares.append(i)
        conector=list(Connectors.objects.all().values())
        for c in list_pares:
            if c==contador_paneles:
                conector_apropiado={
                    "amount": c/2,
                    "name": conector[0]["name"],
                    "price": conector[0]["price"],
                }
                break
            else:
                conector_apropiado={
                    "amount": 0,
                    "name": "no hay conector apropiado",
                    "price": 0,
                }
        #cable vehicular
        vehicleCables=list(VehicleCables.objects.all().values())
        vehicleCables=sorted(vehicleCables, key=lambda cable: cable["supported_amperage"],reverse=False)
        cable_vehicular_apropiado=0
        
        for ch in vehicleCables:
            if ch["supported_amperage"]>=amp_requerido:
                cable_vehicular_apropiado=ch
                break
        if cable_vehicular_apropiado==0:
            cable_vehicular_apropiado=vehicleCables[-1]
        cable_vehicular_apropiado={
            "amount": 10,
            "name": cable_vehicular_apropiado["name"],
            "price": cable_vehicular_apropiado["price"],
        }
        #electric material
        electric_material=list(ElectricMaterials.objects.all().values())
        electric_material={
            "amount": 1,
            "name": electric_material[0]["name"],
            "price": electric_material[0]["price"],
        }
        #cable de tierra
        groundCable=list(GroundSecurityKits.objects.all().values())
        groundCable={
            "amount": 1,
            "name": groundCable[0]["name"],
            "price": groundCable[0]["price"],
        }


        print(f"""       ===============================
        **data**
        {data}
         **productos consumidos**
            {products_consumptions}
        **consumo diario total**
        {total_consumo_productos}
        **paneles**
        {panel_apropiado}
        **baterias**
        bateria {b},capacidad {capacidad},
        total_consumo_productos {calculo_diario},contardor_baterias {contardor_baterias}
        **amp_requerido**
        {amp_requerido}
        ** amp bat **
        {b["capacity"]}
        **regulador**
        {regulador_apropiado}
        **breaker**
        {breaker_apropiado}
        **cable encauchetado**
        {cable_encauchetado_apropiado}
        **soporte panel**
        {soporte_panel}
        **modulo centralizado**
        {modulo_centralizado}
        **unidad de potencia**
        {unidad_potencia_adeacuada}
        **terminal**
        {terminal}
        **conector**
        {conector_apropiado}
        **cable vehicular**
        {cable_vehicular_apropiado}
        **material electrico**
        {electric_material}
        **cable de tierra**
        {groundCable}
               ================================= """)
        return JsonResponse({"consumptions":products_consumptions,
                             "panel_needed":panel_need,
                             "battery_needed":bateria_apropiada,
                             "regulator_needed":regulador_apropiado,
                             "breaker_needed":breaker_apropiado,
                             "rubberized_cable_needed":cable_encauchetado_apropiado,
                             "panel_support_needed":soporte_panel,
                             "centralized_modules_needed":modulo_centralizado,
                             "power_units_needed":unidad_potencia_adeacuada,
                             "terminals_needed":terminal,
                             "connector_needed":conector_apropiado,
                             "vehicle_cable_needed":cable_vehicular_apropiado,
                             "electric_materials_needed":electric_material,
                             "ground_security_kit_needed":groundCable,
                             "products":data,
                             "productos":productos,
                             },safe=False)

# prueba

class PdfViewPage(View):
    template_name       = 'products/html/nuevos/pdfgpt.html'
    def get(self,request):

        return render(
            request,
            self.template_name,
            {"productos":{
            "id":1,
            "name":"mla",
            "imagen":"producto.image.url",
            "price":"producto.price",
            "amount":2,
            "total":2
        }}
            )    

class ShoppingCar(LoginRequiredMixin, View):
    template_name       = 'products/html/nuevos/NVProducts.html'
    paginate_by         = 5
    login_url           = reverse_lazy('users_app:user-login')
    def get(self,request):
        products= list(Products.objects.all().values())
        usuario=request.user
        # products = list(filter(lambda p : p["category_id"] == 3 or p["category_id"] == 4, products))
        
        for p in products:
            print("~"*80)
            print(p)
            print("~"*80)
        
        return render(
            request,
            self.template_name,
            {
                "products":products,
                "usuario":usuario
            }
            )
    
class ProductListView(LoginRequiredMixin,ListView):
    template_name       = 'products/html/nuevos/NVProducts1.html'
    model               = Products
    context_object_name = 'products'
    paginate_by         = 5
    login_url           = reverse_lazy('users_app:user-login')

    def get_queryset(self):
        print("get_queryset=====================")
        id = self.kwargs['id']
        print(id)
        if list(Products.objects.filter(category=id).values())==[]:
            print("existe")
            return Products.objects.all()
        return Products.objects.filter(category=id)
    


    def get_context_data(self, **kwargs):
        print("get_context_data=====================")
        id = self.kwargs['id']
        print(id)
        productos = Products.objects.filter(category=id)
        print(productos, "productos=====================")
        context = super().get_context_data(**kwargs)
        usuario=self.request.user
        context['usuario'] = usuario
        context['productos'] = productos
        print(context, "contexto")
        return context
    
    
class ProductView(View):
    
    
    # dispatch para no pedir csrf token
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,request):
        products=list(Products.objects.all().values())
        # products = list(Battery.objects.filter(capacity=200).values())
        print(products)
        return JsonResponse(products,safe=False)
    
    # this were just tests
    
    # def post(self, request):
    #     print(dir(request))
    #     return JsonResponse({"message":"hola"},safe=False)
    
    # def put(self, request):
    #     print(request.body)
    #     return JsonResponse({"message":"hola"},safe=False)
    
    # def delete(self, request):
    #     # print(json.loads(request.body))
    #     return JsonResponse({"message":"hola"},safe=False)

class GetObj(View):
  def get(self, request,obj, id):
    system("cls")
    
    if obj == "panel":
        obj = SolarPanel.objects.get(id=id).__dict__
    elif obj == "battery":
        obj = Battery.objects.get(id=id).__dict__
    elif obj == "regulators":
        obj = Reguladores.objects.get(id=id).__dict__
    elif obj == "inversor":
        obj = Inversores.objects.get(id=id).__dict__
    elif obj == "support":
        obj = soportes.objects.get(id=id).__dict__
    elif obj == "unity_power":
        obj = UnidadPotencia.objects.get(id=id).__dict__
    elif obj == "breaker":
        obj = Breakers.objects.get(id=id).__dict__
    elif obj == "rubberized_cable":
        obj = RubberizedCables.objects.get(id=id).__dict__
    elif obj == "vehicle_cable":
        obj = VehicleCables.objects.get(id=id).__dict__
    elif obj == "panel_support":
        obj = PanelSupports.objects.get(id=id).__dict__
    elif obj == "battery_support":
        obj = BatterySupports.objects.get(id=id).__dict__
    elif obj == "ground_security_kit":
        obj = GroundSecurityKits.objects.get(id=id).__dict__
    elif obj == "connector":
        obj = Connectors.objects.get(id=id).__dict__
    else:
        raise Exception("no a valid object")

    del obj["_state"]
    print(obj)
    return JsonResponse({"obj":obj})

class CotizacionView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request):
        system("cls")
        #get the products and save them in a variable
            #it's expected to get a request like this: 
            # [
                # {"product_id":3,"amount":1,"hours":2}
                # {"product_id":4,"amount":2,"hours":24}
                # {...}
                # ...
            # ] 
            # you can left hours without specify and it will get the default value for that category
            # you can left hours without specify and it will get 1
        data = json.loads(request.body)
        print(data)
        #------------------------------------------------------------------------------------ 
        
        # format each product with default values if it's needed
        products = []
        for row in data:
            try:
                products.append(
                    Product(
                        row["product_id"],
                        row["hours"] if "hours" in row else 0,
                        row["amount"] if "amount" in row else 1,
                        )
                )
            except IndexError as e:
              print('Exception: ',e)
              return JsonResponse({"msg":f"an error ocurred: {e} \n The id of product you sent, doesn't exists"})
        
        #------------------------------------------------------------------------------------ 
        
        #make quote for each product ----------------------------------------------------------------------------- 
        
        quotes = []
        for product in products:
            quotes.append(
                ProductQuote(
                    product.id,
                    product.amount,
                    product.hours_in_use
                )
            )
        
        
        # just print info
        for obj in quotes:
            # print(obj)
            quote = vars(obj)
            for k in quote:
                print(k," \t : \t ",quote[k])
            print("~"*80)

    
        final_quote = {}
        
        final_quote["panels_needed"] = [quote.panel_needed.__dict__ for quote in quotes]
        final_quote["batteries_needed"] = [quote.battery_needed.__dict__ for quote in quotes]
        final_quote["regulators_needed"] = [quote.regulator_needed.__dict__ for quote in quotes]
        final_quote["breakers_needed"] = [quote.breaker_needed.__dict__ for quote in quotes]
        final_quote["rubberized_cables_needed"] = [quote.rubberized_cables_needed.__dict__ for quote in quotes]
        final_quote["vehicle_cables_needed"] = [quote.vehicle_cables_needed.__dict__ for quote in quotes]
        final_quote["panel_supports_needed"] = [quote.panel_supports_needed.__dict__ for quote in quotes]
        final_quote["battery_supports_needed"] = [quote.battery_supports_needed.__dict__ for quote in quotes]
        final_quote["ground_security_kit_needed"] = [quote.ground_security_kit_needed.__dict__ for quote in quotes]
        final_quote["connectors_needed"] = [quote.connectors_needed.__dict__ for quote in quotes]
        final_quote["terminals_needed"] = [quote.terminals_needed.__dict__ for quote in quotes]
        final_quote["centralized_modules_needed"] = [quote.centralized_modules_needed.__dict__ for quote in quotes]
        final_quote["power_units_needed"] = [quote.power_units_needed.__dict__ for quote in quotes]
        final_quote["electric_materials_needed"] = [quote.electric_materials_needed.__dict__ for quote in quotes]
        final_quote["consumptions"] = [quote.consumption for quote in quotes]
        final_quote["total_consumption"] = reduce(lambda prev, current: prev + current, [quote.consumption["total_consumption_day"] for quote in quotes])# - 169.5
        final_quote["productions"] = [quote.panel_needed.production for quote in quotes]
        final_quote["total_production"] = reduce(lambda prev, current: prev + current, [quote.panel_needed.production["total_production_day"] for quote in quotes])


        #adding================================================================================================================================
        print("\nadding")
        print("="*80)
        
        #adding panels --------------------------------------------------
        
        ideal_panel = sorted(
                [quote.panel_needed for quote in quotes],
                key = lambda panel : panel.production["production_hr"],
                reverse=True
                )[0]
        
        
        while final_quote["total_production"] > ideal_panel.production["total_production_day"]: ideal_panel = RequirementQuote("panel",ideal_panel.id,ideal_panel.amount + 1)
        final_quote["panel_needed"] = ideal_panel.__dict__
        print("~"*60,"\npanel")
        print(final_quote["panel_needed"])
        print(final_quote["panel_needed"]["production"]["total_production_day"] ," - ",final_quote["total_consumption"])
        
        #adding battery --------------------------------------------------

        def elegir_bateria(day_consume, consume_voltaje):
        # Obtener todas las baterías
            baterias = Battery.objects.exclude(voltage=3).exclude(voltage=2)
            
            # las desempaqueto por id,precio,,voltaje,bateria
            unpacked_batteries = [
                {
        
                    "id":bateria.id,
                    "price":bateria.price,
                    "voltaje":bateria.voltage.voltage,
                    "capacity":(bateria.capacity*bateria.voltage.voltage)*0.65,
                    
                } for bateria in baterias
                ]
            # Ordenar la lista de capacidades y precios de menor a mayor precio
            unpacked_batteries.sort(key=lambda bateria: bateria["price"])
            # Inicializar las variables de la combinación de baterías
            ideal_battery = None
            # ideal_batteries_amount = 9**9
            ideal_batteries_price = 99**9
            # Recorrer la lista de capacidades y precios
            for battery in unpacked_batteries:
                # Calcular cuántas baterías se necesitan para cubrir la cantidad requerida
                batteries_needed = math.ceil(day_consume*2 / battery["capacity"])
                if consume_voltaje == 24 and ( batteries_needed%2 != 0 and battery["voltaje"]==12): batteries_needed += 1
                
                # Si esta combinación es más barata que la anterior, reemplazarla
                if (batteries_needed * battery["price"]) <= ideal_batteries_price:
                    ideal_battery = battery
                    ideal_battery["amount"]=batteries_needed
            return ideal_battery
        
        
        ideal_battery = elegir_bateria(final_quote["total_production"],ideal_panel.voltage)
        ideal_battery = RequirementQuote("battery", ideal_battery["id"] , ideal_battery["amount"])
        final_quote["battery_needed"] = ideal_battery.__dict__
        print("~"*60,"\nbattery")
        print(final_quote["battery_needed"])
        print(((final_quote["battery_needed"]["capacity"]*12)*final_quote["battery_needed"]["amount"])*0.65
            ," - ",final_quote["total_consumption"])
        
        #adding regulador & breaker --------------------------------------------------
        
        total_watts_to_support = (ideal_panel.production["production_hr"] * ideal_panel.amount) / ideal_panel.voltage # total wtts / voltage
        
        
        try:regulator_id = Reguladores.objects.filter(amperios__gte = total_watts_to_support).order_by("amperios")[0].id 
        except:regulator_id = Reguladores.objects.order_by("-amperios")[0].id
        
        ideal_regulator = RequirementQuote("regulator",regulator_id)
        final_quote["regulator_needed"]=ideal_regulator.__dict__
        
        
        try:breaker_id = Breakers.objects.filter(amps__gte = total_watts_to_support).order_by("amps")[0].id 
        except:breaker_id = Breakers.objects.order_by("-amps")[0].id
        
        ideal_breaker = RequirementQuote("breaker",breaker_id)
        final_quote["breaker_needed"]=ideal_breaker.__dict__
        
        print("~"*60,"\nregulator & breaker")
        print(final_quote["regulator_needed"])
        print(final_quote["breaker_needed"])
        print("\ntotal_watts_to_support: ",total_watts_to_support)
        
        #adding rubberized_cable & vehicle_cable --------------------------------------------------
        
        try: rubberized_cable_id = (RubberizedCables.objects.filter(supported_amperage__gte=total_watts_to_support).order_by("supported_amperage"))[0].id
        except: rubberized_cable_id = (RubberizedCables.objects.order_by("-supported_amperage"))[0].id
        ideal_rubberized_cable = RequirementQuote(
        "rubberized_cable",
        rubberized_cable_id,
        ProductQuote.default_amount[RubberizedCables.objects.get(id=rubberized_cable_id).category.id] #default amount for the cables
        )
        final_quote["rubberized_cable_needed"]=ideal_rubberized_cable.__dict__
    
        try:vehicle_cable_id = (VehicleCables.objects.filter(supported_amperage__gte=total_watts_to_support).order_by("supported_amperage"))[0].id
        except: vehicle_cable_id = (VehicleCables.objects.order_by("-supported_amperage"))[0].id
        ideal_vehicle_cable = RequirementQuote(
        "vehicle_cable",
        vehicle_cable_id,
        ProductQuote.default_amount[RubberizedCables.objects.get(id=vehicle_cable_id).category.id] #default amount for the cables
        )
        final_quote["vehicle_cable_needed"]=ideal_vehicle_cable.__dict__
        
        print("~"*60,"\nrubberized & vehicle cables")
        print(final_quote["rubberized_cable_needed"])
        print(final_quote["vehicle_cable_needed"])
    
        #adding panel supports --------------------------------------------------
        
        ideal_panel_support = RequirementQuote("panel_support",1,ideal_panel.amount)
        final_quote["panel_support_needed"]=ideal_panel_support.__dict__
        
        print("~"*60,"\npanel support")
        print(final_quote["panel_support_needed"])
        
        #adding connectors --------------------------------------------------
        output_pairs = ideal_panel.amount
        connectors_needed = 0
        while output_pairs > 1:
            x = output_pairs // 2
            output_pairs = x
            connectors_needed += x*2
            
        ideal_connector = RequirementQuote("connector",1,connectors_needed)
        final_quote["connector_needed"]=ideal_connector.__dict__
        
        print("~"*60,"\nconnector")
        print(final_quote["connector_needed"])
        
        #adding unity power --------------------------------------------------
        
        there_is_a_big_power_unity = any([quote.power_units_needed.id !=4 for quote in quotes])
        
        if there_is_a_big_power_unity:
            # print("capacity: ",ideal_battery.capacity)
            try:
                unity_power_id = UnityPower.objects\
                .exclude(id=4)\
                .filter(max_ampers_supported__gte=ideal_battery.capacity)\
                .order_by("max_ampers_supported")[0].id
            except:
                unity_power_id = UnityPower.objects\
                .exclude(id=4)\
                .order_by("max_ampers_supported")[0].id
        
        else:
            unity_power_id = 4
        
        ideal_unity_power = RequirementQuote(
        "unity_power",
        unity_power_id,
        1
        )
        
        final_quote["unity_power_needed"]=ideal_unity_power.__dict__
        print("~"*60,"\nunity_power")
        print(final_quote["unity_power_needed"])
    
        # ================================================================================================================================
        return JsonResponse(
            final_quote
            ,safe=False)
       
class PdfView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request):
        print("generating pdf...")
        data = json.loads(request.body)
        batteries_ids = [(battery["id"]) for battery in data["batteries_needed"]]
        batteries = []
        
        for battery_id in batteries_ids:
            battery = Battery.objects.get(id=battery_id).__dict__
            del battery["_state"]
            batteries.append(battery)
            
        regulators_ids = [(regulator["id"]) for regulator in data["regulators_needed"]]
        regulators = []
        for regulator_id in regulators_ids:
            regulator = Reguladores.objects.get(id=regulator_id).__dict__
            del regulator["_state"]
            regulators.append(regulator)
            
        breakers_ids = [(breaker["id"]) for breaker in data["breakers_needed"]]
        breakers = []
        for breaker_id in breakers_ids:
            breaker = Breakers.objects.get(id=breaker_id).__dict__
            del breaker["_state"]
            breakers.append(breaker)
            
        others = {
            "batteries":batteries,
            "regulators":regulators,
            "breakers":breakers,
        }
        
        data["others"] = others
        print(data)
        # create_pdf(data,"pdf.pdf")
        pdf = open("pdf.pdf","rb")
        return FileResponse(pdf)
    
class SendEmail(View):
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request):
        pdf_send= json.loads(request.body)
        email = pdf_send["email"]
        data  = pdf_send["data"]
        print(f"sending email...a {email} y la data es {data}")
        pdf   = generate_pdf(email,'products/html/nuevos/pdfgpt.html',data)
        return JsonResponse({"msg":pdf})
    

class GeneratePdf(View):
        
        def get (self,request):
            print("generating pdf...")
            data={}
            """data = json.loads(request.body)"""
            pdf= render_to_pdf('products/html/nuevos/pdf-imprimir.html',data)
            return HttpResponse(pdf,content_type='application/pdf')


        """try:


            send_mail(email,
                    "una nueva prueba",
                    "super prueba desde api",
                    pdf,)        
            return JsonResponse({"msg":"sended"})
        except Exception as e:
            print('An exception occurred: ',e)
            return JsonResponse({"msg":f"couldn't be sended: {e}"})"""
