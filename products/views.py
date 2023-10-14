from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .classes import *
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
            print(data,"cache desde el if data=={}")
            if data==None:
                return JsonResponse({"error":"no hay datos"})
        
        try:
            if data[0]["borrar"]==True:
                cache.delete(request.user.username)
                return JsonResponse({"message":"borrado"})
        except:
            print("no hay borrar")
        cache.set(usuario.username,data,timeout=900)
        products_consumptions=[]
        total_consumo_productos=0
        productos=[]
        inversor_need={
            "amount":0,
            "name":"",
            "price":0,
        }
        precios_productos=0
        for d in data:
            print(d)
            product=Products.objects.get(id=d["product_id"])
            calculo_diario=product.consume*d["hours"]
            porcentaje_perdidas=(Category.objects.get(id=product.category_id).perdida)
            calculo_perdidas=(calculo_diario*porcentaje_perdidas)/100
            total_consumo_productos+=(calculo_diario+calculo_perdidas)*d["amount"]
            precios_productos+=product.price*d["amount"]
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
            print(d["product_id"],"id producto 18 es inversor antes de if")
            if product.category_id==19:
                print("entro al if inversor",d["product_id"],d,product.category_id)
                inversor=Inversores.objects.get(id=11)
                inversor_need={
                    "amount":1,
                    "name":inversor.name,
                    "price":inversor.price,
                
                }
                
        # PANEL APROPIADO=======================================================

        panel_need,panel_apropiado,contador_paneles=paneles(total_consumo_productos)

        # VOLTAJE DEL SISTEMA===================================================

        voltage_sistema=Voltage.objects.get(id=panel_apropiado["voltage_id"]).voltage

        # BATERIAS APROPIADAS===================================================

        bateria_apropiada=baterias(calculo_diario ,total_consumo_productos,voltage_sistema)

        # AMPERIOS REQUERIDOS====================================================

        amp_requerido=(panel_apropiado["production"]/voltage_sistema)*contador_paneles

        # REGULADOR APROPIADO===================================================

        regulador_apropiado=regulador(amp_requerido)
        
        # BREAKER APROPIADO======================================================

        breaker_apropiado=breaker(amp_requerido)

        # CABLE ENCAUCHETADO APROPIADO===========================================

        cable_encauchetado_apropiado=cables_encauchetados(amp_requerido)

        # SOPORTE PANEL APROPIADO================================================

        soporte_panel=Soporte_panel(contador_paneles)

        # MODULO CENTRALIZADO====================================================

        modulo_centralizado=Modulo_centralizado()

        # UNIDAD DE POTENCIA=====================================================

        unidad_potencia_adeacuada=Unidad_potencia(bateria_apropiada,voltage_sistema)

        # TERMINAL================================================================

        terminal=Terminal()

        # CONECTOR================================================================

        conector_apropiado=Conector(contador_paneles)

        # CABLE VEHICULAR========================================================

        cable_vehicular_apropiado=Cable_vehicular(amp_requerido)

        # MATERIAL ELECTRICO=====================================================

        electric_material=Electric_material()

        # CABLE DE TIERRA========================================================

        groundCable=Cable_tierra()

        # rack de baterias========================================================

        rack_bateria=rack_baterias(bateria_apropiada["amount"])
        respuesta={"consumptions":products_consumptions,
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
                             "eliminar_requirements":data[-1]["eliminar_requeimientos"],
                             "rack_bateria":rack_bateria,
                             "inversor":inversor_need,
                             }

        totalPrecios=panel_need["price"]+bateria_apropiada["price"]+regulador_apropiado["price"]+breaker_apropiado["price"]+cable_encauchetado_apropiado["price"]+soporte_panel["price"]+modulo_centralizado["price"]+unidad_potencia_adeacuada["price"]+terminal["price"]+conector_apropiado["price"]+cable_vehicular_apropiado["price"]+electric_material["price"]+groundCable["price"]+rack_bateria["price"]+inversor_need["price"]
        respuesta["totalPrecios"]=totalPrecios
        respuesta["totalConsumo"]=total_consumo_productos
        total_final=panel_need["price"]*panel_need["amount"]+bateria_apropiada["price"]*bateria_apropiada["amount"]+regulador_apropiado["price"]*regulador_apropiado["amount"]+breaker_apropiado["price"]*breaker_apropiado["amount"]+cable_encauchetado_apropiado["price"]*cable_encauchetado_apropiado["amount"]+soporte_panel["price"]*soporte_panel["amount"]+modulo_centralizado["price"]*modulo_centralizado["amount"]+unidad_potencia_adeacuada["price"]*unidad_potencia_adeacuada["amount"]+terminal["price"]*terminal["amount"]+conector_apropiado["price"]*conector_apropiado["amount"]+cable_vehicular_apropiado["price"]*cable_vehicular_apropiado["amount"]+electric_material["price"]*electric_material["amount"]+groundCable["price"]*groundCable["amount"]+rack_bateria["price"]*rack_bateria["amount"]+inversor_need["price"]*inversor_need["amount"]
        premium= total_final-modulo_centralizado["price"]*modulo_centralizado["amount"]
        basic=total_final-unidad_potencia_adeacuada["price"]*unidad_potencia_adeacuada["amount"]
        respuesta["total_final_premiun"]=premium
        respuesta["total_final_basic"]=basic
        respuesta["total_precios"]=precios_productos


        print(f"""       ===============================
        **data**
        {data}
         **productos consumidos**
            {products_consumptions}
        **consumo diario total**
        {total_consumo_productos}
        **paneles**
        {panel_need}
        **baterias**
        bateria {bateria_apropiada},
        total_consumo_productos {calculo_diario}
        **amp_requerido**
        {amp_requerido}
        ** amp bat **
        {bateria_apropiada["capacity"]}
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
        inverosr
        {inversor_need}
        **rack bateria**
        {rack_bateria}
        **total precios**
        {totalPrecios}
        **total consumo**
        {total_consumo_productos}
        **total final**
        {total_final}

               ================================= """)
        print(data[-1]["eliminar_requeimientos"],"eliminar requirements")
        
        

        llaves=["panel_needed","battery_needed","regulator_needed","breaker_needed","rubberized_cable_needed","panel_support_needed","centralized_modules_needed","power_units_needed","terminals_needed","connector_needed","vehicle_cable_needed","electric_materials_needed","ground_security_kit_needed","rack_bateria","inversor"]
        for i in llaves:
            if i in data[-1]["eliminar_requeimientos"]:
                print(i,"esta es la i =====================")
                respuesta[i]["price"]=0
        
       


        cache.set(f"respuesta{usuario.username}",respuesta,timeout=900)
        return JsonResponse(respuesta,safe=False)

# prueba

class PdfViewPage(View):
    
    def get(self,request):
        usuario=request.user
        data  = cache.get(f"respuesta{usuario.username}")
        print(f"sending email...a {usuario} y la data es {data}")
        pdf   = generate_pdf_view('products/html/nuevos/pdfgpt.html',data)
        return HttpResponse(pdf, content_type='application/pdf')

        

class ShoppingCar(LoginRequiredMixin, ListView):
    template_name       = 'products/html/nuevos/NVProducts1.html'
    model               = Products
    context_object_name = 'products'
    paginate_by         = 4
    login_url           = reverse_lazy('users_app:user-login')

    def get_queryset(self):
        print("get_queryset=====================")
        id = self.kwargs['id']
        print(id)
        if list(Products.objects.filter(category=id).values())==[]:
            print("existe")
            
            return Products.objects.all().order_by("category")
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
    
class ShowCategoryView(View):
    def get(self,request):
        categories=list(ShowCategory.objects.all().values())
        categorias=list(Category.objects.all().values())
        print(categories)
        
        return JsonResponse({"botones":categories,"categorias":categorias},safe=False)
    
    
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
        print(pdf_send)
        nombre= pdf_send["name"]
        apellido= pdf_send["lastname"]
        email = pdf_send["email"]
        usuario=request.user
        data  = cache.get(f"respuesta{usuario.username}")
        print(f"sending email...a {email} y la data es {data}")
        pdf   = generate_pdf(email,'products/html/nuevos/pdfgpt.html',data,nombre,apellido)
        return JsonResponse({"msg":"sended"})
    

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
        

class ShowVideos(View):
    def get(self,request):
        usuario=request.user
        Cuenta=0
        try:
            Cuenta=cache.get(usuario.username+"video")
            print(Cuenta)
            if Cuenta==None:
                Cuenta=0
                cache.set(usuario.username+"video",Cuenta)
                print("se creo la cuenta")
            else:
                Cuenta+=1
                cache.set(usuario.username,Cuenta,1)
                print("se sumo a la cuenta")
        except Exception as e:
            print(e)
        print(Cuenta)
        print(usuario.username+"video")

        if Cuenta>=0:
            return JsonResponse({"msg":False})
        else:
            return JsonResponse({"msg":True})
