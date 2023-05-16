const inputs = document.querySelectorAll(".horas-sol-producto");
const quoteTemplate = document.getElementById("quote-template").content;
const quoteContainer = document.querySelector(".acumulador-cotizador");
let contador=0;
let productsToquote = [];
let cotizacion_enviar;
let mas_cantidad=false

inputs.forEach(div => {
  div.querySelector("input").addEventListener('change', ()=>{
    div.querySelector("strong").textContent = div.querySelector("input").value;
  })
  div.querySelector("input").value = 24;
  div.querySelector("strong").textContent = div.querySelector("input").value;
});

// functions------

async function addToQuote(product_id1,product_name,product_price ,hours_used=24) {
  console.log(product_id1,product_name ,product_price ,"=======================================");
  inputhoras=`product°${product_id1}`;
  console.log(inputhoras);
  hours_used =  parseInt((document.getElementById(inputhoras)).querySelector("input").value);
  console.log(hours_used)
  if (productsToquote.find((obj) => obj.product_id == product_id1)) {
    console.log("ya existe",product_id1);
    new_amount = productsToquote.find((obj) => obj.product_id == product_id1);
    new_amount.amount ++;
    console.log(new_amount,"new_amount",productsToquote,"productsToquote");
    mas_cantidad=true;
  }else{
    productsToquote.push(
      {
        amount:1,
        product_id:product_id1,
        hours:hours_used
      }
    );
  }
  console.log(productsToquote,"productsToquote");

  const consumptions = await fetch("http://127.0.0.1:8000/products/vista_prueba",{
          method: "POST",
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([
          ...productsToquote,
          ]),
          
      },console.log(`hiso la peticion con ${product_id1} y ${hours_used}`)).then((response) => response.json()).then((quotation) =>quotation);
    console.log(consumptions,"consumptions");
  
  // MISSING FIX
  cotizacion_enviar=consumptions;
  makeQuote(consumptions,product_id1,product_name,product_price,hours_used)
}

function delFromProducts(id) {
  productsToquote = productsToquote.filter((obj) => obj.product_id != id);
  //productsToquote.find((obj) => obj.product_id == id).remove;
  console.log(productsToquote,"productsToquote");
  quoteContainer.querySelector(`#_${id}`).remove();
  eliminarProducto(productsToquote);
  
  //makeQuote();
}

async function makeQuote(quotation,product_id,product_name,product_price,hours_used) {
  let quoteReturn;
      // datos productos
      
      if (mas_cantidad==false) {
        console.log("mas cantidad");
        
        let consumptions=quotation.consumptions[contador]
        contador++;
        console.log(consumptions,"consumption en makeQuote",contador);
      const clone = document.importNode(quoteTemplate, true);
      clone.querySelector(".quote").id += "_"+product_id;
      clone.querySelector(".eliminar-cotizador").addEventListener('click',()=>delFromProducts(product_id));
      clone.querySelector(".titulo-producto-cotizador").textContent += product_name;
      clone.querySelector(".precio-unitario").textContent += "$"+formatearNumero(product_price).toString();
      clone.querySelector(".horas-uso-cotizador").textContent += hours_used;
      clone.querySelector(".consumo-hora-cotizador").textContent += consumptions.consumption_hr;
      clone.querySelector(".consumo-dia-cotizador").textContent += consumptions.consumption_day;
      clone.querySelector(".porcentaje-perdidas-cotizador").textContent += consumptions.loss_percentaje+" % perdidas: "+consumptions.loss_consumption;
      clone.querySelector(".total-consumo-cotizador").textContent += consumptions.total_consumption_day;
      quoteContainer.appendChild(clone);
      }
      mas_cantidad=false;
        
      
        

      
      //
      // seccion paneles
      let total_panel=quotation.panel_needed.price*quotation.panel_needed.amount;
      document.querySelector(".paneles-requeridos1").textContent = ` ${quotation.panel_needed.amount}`;
      document.querySelector(".paneles-tipo-requeridos1").textContent = quotation.panel_needed.name;
      document.querySelector(".paneles-precio-requeridos1").textContent = quotation.panel_needed.price;
      document.querySelector(".paneles-precio-requeridos2").textContent = ` ${total_panel}`;
      //

      // seccion baterias
      console.log(quotation.battery_needed.name,"bateria");
      document.querySelector(".baterias-requeridos1").textContent = quotation.battery_needed.amount;
      document.querySelector(".baterias-tipo-requeridos").textContent = quotation.battery_needed.name;
      document.querySelector(".baterias-precio-requeridos1").textContent = quotation.battery_needed.price;
      document.querySelector(".baterias-precio-requeridos2").textContent = quotation.battery_needed.price*quotation.battery_needed.amount;

      //
  
      document.querySelector(".reguladores-requeridos").textContent = quotation.regulator_needed.amount;
      document.querySelector(".reguladores-tipo-requeridos").textContent = quotation.regulator_needed.name;
      document.querySelector(".reguladores-precio-requeridos").textContent = quotation.regulator_needed.price;
      // document.querySelector(".reguladores-precio-total-requeridos").textContent = quotation.regulators_needed[0].price*quotation.regulators_needed[0].amount;
     
      // 
        
      
      // 
        
      document.querySelector(".breakers-requeridos").textContent = quotation.breaker_needed.amount;
      document.querySelector(".breakers-tipo-requeridos").textContent = quotation.breaker_needed.name;
      document.querySelector(".breakers-precio-requeridos").textContent = quotation.breaker_needed.price;
      // document.querySelector(".breakers-precio-total-requeridos").textContent = quotation.breakers_needed[0].price*quotation.breakers_needed[0].amount;
        
      document.querySelector(".cables-requeridos").textContent = quotation.rubberized_cable_needed.amount;
      document.querySelector(".cables-tipo-requeridos").textContent = quotation.rubberized_cable_needed.name;
      document.querySelector(".cables-precio-requeridos").textContent = quotation.rubberized_cable_needed.price;
      document.querySelector(".cables-precio-total-requeridos").textContent = quotation.rubberized_cable_needed.price*quotation.rubberized_cable_needed.amount;
        
      document.querySelector(".soportes-sobre-techo-requeridos").textContent = quotation.panel_support_needed.amount;
      document.querySelector(".soportes-sobre-techo-tipo-requeridos").textContent = quotation.panel_support_needed.name;
      document.querySelector(".soportes-sobre-techo-precio-requeridos").textContent = quotation.panel_support_needed.price;
      document.querySelector(".soportes-sobre-techo-precio-total-requeridos").textContent = quotation.panel_support_needed.price*quotation.panel_support_needed.amount;
        
      document.querySelector(".modulos-centralizados-requeridos").textContent = quotation.centralized_modules_needed.amount;
      document.querySelector(".modulos-centralizados-tipo-requeridos").textContent = quotation.centralized_modules_needed.name;
      document.querySelector(".modulos-centralizados-precio-requeridos").textContent = quotation.centralized_modules_needed.price;
      document.querySelector(".modulos-centralizados-precio-total-requeridos").textContent = quotation.centralized_modules_needed.price*quotation.centralized_modules_needed.amount;
        
      document.querySelector(".unidad-de-potencia-requeridos").textContent = quotation.power_units_needed.amount;
      document.querySelector(".unidad-de-potencia-tipo-requeridos").textContent = quotation.power_units_needed.name;
      document.querySelector(".unidad-de-potencia-precio-requeridos").textContent = quotation.power_units_needed.price;
      document.querySelector(".unidad-de-potencia-precio-total-requeridos").textContent = quotation.power_units_needed.price*quotation.power_units_needed.amount;
        
      document.querySelector(".terminales-MC4-requeridos").textContent = quotation.terminals_needed.amount;
      document.querySelector(".terminales-MC4-tipo-requeridos").textContent = quotation.terminals_needed.name;
      document.querySelector(".terminales-MC4-precio-requeridos").textContent = quotation.terminals_needed.price;
      document.querySelector(".terminales-MC4-precio-total-requeridos").textContent = quotation.terminals_needed.price*quotation.terminals_needed.amount;
      
      document.querySelector(".conectores-en-y-requeridos").textContent = quotation.connector_needed.amount;
      document.querySelector(".conectores-en-y-tipo-requeridos").textContent = quotation.connector_needed.name;
      document.querySelector(".conectores-en-y-precio-requeridos").textContent = quotation.connector_needed.price;
      document.querySelector(".conectores-en-y-precio-total-requeridos").textContent = quotation.connector_needed.price*quotation.connector_needed.amount;
      
      document.querySelector(".cable-vehicular-requeridos").textContent = quotation.vehicle_cable_needed.amount;
      document.querySelector(".cable-vehicular-tipo-requeridos").textContent = quotation.vehicle_cable_needed.name;
      document.querySelector(".cable-vehicular-precio-requeridos").textContent = quotation.vehicle_cable_needed.price;
      document.querySelector(".cable-vehicular-precio-total-requeridos").textContent = quotation.vehicle_cable_needed.price*quotation.vehicle_cable_needed.amount;
        
      document.querySelector(".materiales-electricos-requeridos").textContent = quotation.electric_materials_needed.amount;
      document.querySelector(".materiales-electricos-tipo-requeridos").textContent = quotation.electric_materials_needed.name;
      document.querySelector(".materiales-electricos-precio-requeridos").textContent = quotation.electric_materials_needed.price;
      document.querySelector(".materiales-electricos-precio-total-requeridos").textContent = quotation.electric_materials_needed.price*quotation.electric_materials_needed.amount;
      
      document.querySelector(".kit-puesta-a-tierra-requeridos").textContent = quotation.ground_security_kit_needed.amount;
      document.querySelector(".kit-puesta-a-tierra-tipo-requeridos").textContent = quotation.ground_security_kit_needed.name;
      document.querySelector(".kit-puesta-a-tierra-precio-requeridos").textContent = quotation.ground_security_kit_needed.price;
      document.querySelector(".kit-puesta-a-tierra-precio-total-requeridos").textContent = quotation.ground_security_kit_needed.price*quotation.ground_security_kit_needed.amount;
      
      return quoteReturn
  
}
function createandsendpdf(nombre, email,apellido) {
  console.log("enviando pdf", nombre, email);
  alert("Se enviará a su correo el pdf en unos segundos");
  fetch("http://127.0.0.1:8000/products/sendQuote", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ 
      "name": nombre,
      "lastname": apellido,
      "email": email,
      "data": cotizacion_enviar
    })
}
  // va a recibir un pdf 
  ).then(response => response.json()).then(data => {
    console.log(data);
    // alerta
    alert("Se ha enviado el pdf a su correo", data);
  }) 
}

// Funciones auxiliares ----------------------------------------
function formatearNumero(numero, lenguaje = "es") {
  // Crear un objeto Intl.NumberFormat con el lenguaje y las opciones deseadas
  let formateador = new Intl.NumberFormat(lenguaje, {
    useGrouping: true, // Usar agrupación de miles
    minimumFractionDigits: 0, // No mostrar decimales
    maximumFractionDigits: 0 // No mostrar decimales
  });
  // Devolver el número formateado como una cadena
  return formateador.format(numero);
}

function eliminarProducto(prod){
  fetch("http://127.0.0.1:8000/products/vista_prueba",{
  method: "POST",
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(prod),
})
.then(response => response.json())
.then(data => {
  console.log(data);
  if (data.error == "no hay datos") {
    alert("No hay productos")
    //actualizar la pagina
    
    
  }
  window.location.reload();

})
}



const consumptions =  fetch("http://127.0.0.1:8000/products/vista_prueba",{
  method: "POST",
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({}),
}).then(response => response.json()).then(data => {
  console.log(data)
  contador_productos = 0;
  data.productos.forEach(element => {
    productsToquote.push(
      {
        amount:element.amount,
        product_id:element.id,
        hours:element.hours_used
      }
    );
    makeQuote(data, element.id, element.name, element.price, element.hours_used)
    cotizacion_enviar= data;
  });
  
  return data
}).catch(error => {
  console.log(error)
})