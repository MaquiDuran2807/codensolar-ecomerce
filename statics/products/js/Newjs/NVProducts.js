const inputs = document.querySelectorAll(".horas-sol-producto");
const quoteTemplate = document.getElementById("quote-template").content;
const quoteContainer = document.querySelector(".acumulador-cotizador");
let productsToquote = [];


inputs.forEach(div => {
  div.querySelector("input").addEventListener('change', ()=>{
    div.querySelector("strong").textContent = div.querySelector("input").value;
  })
  div.querySelector("input").value = 24;
  div.querySelector("strong").textContent = div.querySelector("input").value;
});

// functions------

async function addToQuote(product,hours_used=24) {
  hours_used =  parseInt((document.getElementById(`product°${product.id}`)).querySelector("input").value);
  // console.log(hours_used);
  const clone = document.importNode(quoteTemplate, true);

  clone.querySelector(".quote").id = "_"+product.id;
  clone.querySelector(".eliminar-cotizador").addEventListener('click',()=>delFromProducts(product.id));
  clone.querySelector(".titulo-producto-cotizador").textContent = product.name;
  clone.querySelector(".precio-unitario").textContent = "$"+formatearNumero(product.price).toString();
  clone.querySelector(".horas-uso-cotizador").textContent = hours_used;

  const consumptions = await fetch("http://127.0.0.1:8000/products/cotizacion",{
          method: "POST",
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([{
          'product_id': product.id,
          'hours': hours_used
          }]),
      }).then((response) => response.json()).then((quotation) =>quotation.consumptions[0])
      
  clone.querySelector(".consumo-hora-cotizador").textContent = consumptions.consumption_hr;
  clone.querySelector(".consumo-dia-cotizador").textContent = consumptions.consumption_day;
  clone.querySelector(".porcentaje-perdidas-cotizador").textContent = consumptions.loss_percentaje+" % perdidas: "+consumptions.loss_consumption;
  clone.querySelector(".total-consumo-cotizador").textContent = consumptions.total_consumption_day;

  quoteContainer.appendChild(clone);
  // MISSING FIX
  productsToquote.push(
    {
      product_id:product.id,
      hours:hours_used
    }
  );
  makeQuote()
}

function delFromProducts(id) {
  productsToquote = productsToquote.filter((obj) => obj.product_id != id);
  quoteContainer.querySelector(`#_${id}`).remove();
  makeQuote();
}

async function makeQuote() {
  let quoteReturn;
  if (productsToquote.length >= 1) {
    fetch("http://127.0.0.1:8000/products/cotizacion",{
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify([
          ...productsToquote
        ]),
    })
    .then((response) => response.json())
    .then(async (quotation) =>{
      console.log(quotation);
  
      document.querySelector(".reguladores-requeridos").textContent = quotation.regulator_needed.amount;
      document.querySelector(".reguladores-tipo-requeridos").textContent = quotation.regulator_needed.name;
      document.querySelector(".reguladores-precio-requeridos").textContent = quotation.regulator_needed.price;
      // document.querySelector(".reguladores-precio-total-requeridos").textContent = quotation.regulators_needed[0].price*quotation.regulators_needed[0].amount;
        
      document.querySelector(".paneles-requeridos").textContent = quotation.panel_needed.amount;
      document.querySelector(".paneles-tipo-requeridos").textContent = quotation.panel_needed.name;
      document.querySelector(".paneles-precio-requeridos").textContent = quotation.panel_needed.price;
      // document.querySelector(".paneles-precio-total-requeridos").textContent = quotation.panels_needed[0].price*quotation.panels_needed[0].amount;
        
      document.querySelector(".baterias-requeridos").textContent = quotation.battery_needed.amount;
      document.querySelector(".baterias-tipo-requeridos").textContent = quotation.battery_needed.name;
      document.querySelector(".baterias-precio-requeridos").textContent = quotation.battery_needed.price;
      // document.querySelector(".baterias-precio-total-requeridos").textContent = quotation.batteries_needed[0].price*quotation.batteries_needed[0].amount;
        
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
        
      document.querySelector(".modulos-centralizados-requeridos").textContent = quotation.centralized_modules_needed[0].amount;
      document.querySelector(".modulos-centralizados-tipo-requeridos").textContent = quotation.centralized_modules_needed[0].name;
      document.querySelector(".modulos-centralizados-precio-requeridos").textContent = quotation.centralized_modules_needed[0].price;
      document.querySelector(".modulos-centralizados-precio-total-requeridos").textContent = quotation.centralized_modules_needed[0].price*quotation.centralized_modules_needed[0].amount;
        
      document.querySelector(".unidad-de-potencia-requeridos").textContent = quotation.power_units_needed[0].amount;
      document.querySelector(".unidad-de-potencia-tipo-requeridos").textContent = quotation.power_units_needed[0].name;
      document.querySelector(".unidad-de-potencia-precio-requeridos").textContent = quotation.power_units_needed[0].price;
      document.querySelector(".unidad-de-potencia-precio-total-requeridos").textContent = quotation.power_units_needed[0].price*quotation.power_units_needed[0].amount;
        
      document.querySelector(".terminales-MC4-requeridos").textContent = quotation.terminals_needed[0].amount;
      document.querySelector(".terminales-MC4-tipo-requeridos").textContent = quotation.terminals_needed[0].name;
      document.querySelector(".terminales-MC4-precio-requeridos").textContent = quotation.terminals_needed[0].price;
      document.querySelector(".terminales-MC4-precio-total-requeridos").textContent = quotation.terminals_needed[0].price*quotation.terminals_needed[0].amount;
      
      document.querySelector(".conectores-en-y-requeridos").textContent = quotation.connector_needed.amount;
      document.querySelector(".conectores-en-y-tipo-requeridos").textContent = quotation.connector_needed.name;
      document.querySelector(".conectores-en-y-precio-requeridos").textContent = quotation.connector_needed.price;
      document.querySelector(".conectores-en-y-precio-total-requeridos").textContent = quotation.connector_needed.price*quotation.connector_needed.amount;
      
      document.querySelector(".cable-vehicular-requeridos").textContent = quotation.vehicle_cable_needed.amount;
      document.querySelector(".cable-vehicular-tipo-requeridos").textContent = quotation.vehicle_cable_needed.name;
      document.querySelector(".cable-vehicular-precio-requeridos").textContent = quotation.vehicle_cable_needed.price;
      document.querySelector(".cable-vehicular-precio-total-requeridos").textContent = quotation.vehicle_cable_needed.price*quotation.vehicle_cable_needed.amount;
        
      document.querySelector(".materiales-electricos-requeridos").textContent = quotation.electric_materials_needed[0].amount;
      document.querySelector(".materiales-electricos-tipo-requeridos").textContent = quotation.electric_materials_needed[0].name;
      document.querySelector(".materiales-electricos-precio-requeridos").textContent = quotation.electric_materials_needed[0].price;
      document.querySelector(".materiales-electricos-precio-total-requeridos").textContent = quotation.electric_materials_needed[0].price*quotation.electric_materials_needed[0].amount;
      
      document.querySelector(".kit-puesta-a-tierra-requeridos").textContent = quotation.ground_security_kit_needed[0].amount;
      document.querySelector(".kit-puesta-a-tierra-tipo-requeridos").textContent = quotation.ground_security_kit_needed[0].name;
      document.querySelector(".kit-puesta-a-tierra-precio-requeridos").textContent = quotation.ground_security_kit_needed[0].price;
      document.querySelector(".kit-puesta-a-tierra-precio-total-requeridos").textContent = quotation.ground_security_kit_needed[0].price*quotation.ground_security_kit_needed[0].amount;
        
      // document.querySelector(".rack-soporte-baterias-requeridos").textContent = quotation.battery_supports_needed[0].amount;
      // document.querySelector(".rack-soporte-baterias-tipo-requeridos").textContent = quotation.battery_supports_needed[0].name;
      // document.querySelector(".rack-soporte-baterias-precio-requeridos").textContent = quotation.battery_supports_needed[0].price;
  
  
      // quoteContainer.querySelector(`#_${id}`).querySelector("#horas_sol").textContent = quotation.productions[0].sun_hours
      // quoteContainer.querySelector(`#_${id}`).querySelector("#consumo_dia").textContent = quotation.consumptions[0].consumption_day
      // quoteContainer.querySelector(`#_${id}`).querySelector("#porcentaje_perdidas").textContent = "%"+ quotation.consumptions[0].loss_percentage.toString()
      // quoteContainer.querySelector(`#_${id}`).querySelector("#cantidad_consumo").textContent = quotation.consumptions[0].total_consumption
      
      // const panel = await fetch(`http://127.0.0.1:8000/products/panel/${quotation.panels_needed[0].id}`).then(response=>response.json()).then(panel => panel.panel);
      // const regulator = await fetch(`http://127.0.0.1:8000/products/regulator/${quotation.regulators_needed[0].id}`).then(response=>response.json()).then(regulator => regulator.regulator);
      // const battery = await fetch(`http://127.0.0.1:8000/products/battery/${quotation.batteries_needed[0].id}`).then(response=>response.json()).then(battery => battery.battery);
      // const breaker = await fetch(`http://127.0.0.1:8000/products/breaker/${quotation.breakers_needed[0].id}`).then(response=>response.json()).then(breaker => breaker.breaker);
  
      // // console.log(quotation);
      // quote.querySelector("#paneles_requeridos").textContent = quotation.panels_needed[0].amount;
      // quote.querySelector("#paneles_tipo").textContent = panel.name;
      // quote.querySelector("#paneles_precio").textContent = "$ "+formatearNumero(panel.price);
      
      // quote.querySelector("#reguladores_requeridos").textContent = quotation.regulators_needed[0].amount;
      // quote.querySelector("#reguladores_tipo").textContent = regulator.name;
      // quote.querySelector("#reguladores_precio").textContent = "$ "+formatearNumero(regulator.price);
      
      // quote.querySelector("#baterias_requeridos").textContent = quotation.batteries_needed[0].amount;
      // quote.querySelector("#baterias_tipo").textContent = battery.name;
      // quote.querySelector("#baterias_precio").textContent = "$ "+formatearNumero(battery.price);
      
      // quote.querySelector("#breakers_requeridos").textContent = quotation.breakers_needed[0].amount;
      // quote.querySelector("#breakers_tipo").textContent = breaker.name;
      // quote.querySelector("#breakers_precio").textContent = "$ "+formatearNumero(breaker.price);
      
      // quote.querySelector("#precio_acumulado").textContent = "$ "+formatearNumero(
      //     breaker.price+
      //     regulator.price+
      //     panel.price+
      //     battery.price
      //     );
      return quoteReturn
    })
    .catch((error) => {
        console.log(error);
    })
  }else{
    window.location.reload();
  }

  
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