$(function(){
  $('#invoice').submit(function(e){
    e.preventDefault();
    // var dataJson = JSON.stringify($('#invoice').serializeArray());
    // var cliente = [{"factura"}];
    // Campos
    var razonSocial = $("input[name=social]").val();
    var ruc = $("input[name=ruc]").val();
    var direccion = $("input[name=direccion]").val();
    var telefono = $("input[name=telefono]").val();
    var tax = $("input[name=tax]").val();

    // list product
    var razonSocial = $("input[name=tax]").val();
    var razonSocial = $("input[name=tax]").val();
    var razonSocial = $("input[name=tax]").val();

    var jsonData ={
      "factura": {
        "cliente": {
          "empresa":razonSocial,
          "direccion":direccion,
          "telefono":telefono,
          "ruc":ruc
        },
        "productos": [
          {
            "nombre":"Dummy Donson",
            "cantidad":1,
            "tasa":1,
            "precio":23124123123
          }
        ]
      }
    };
    // crear iteracion con each para que pueda leer cada textarea y hacer los push al json de los articulos
    // es un ejemplo el que esta abajo de este comentario
    jsonData.factura["productos"].push(
      {
        "nombre":"Dummy Donson",
        "cantidad":1,
        "tasa":1,
        "precio":23124123123
      }
    );

    console.log(jsonData);
  });






var wrapper = $("#article_box"); //Fields wrapper
$("#add").click(function(e){
  e.preventDefault();

  $(wrapper).append(
    '<div class="form-group col-md-4">' +
      '<div class="form-group col-md-12">'+
        '<label for="inputCity">Precio</label>'+
        '<div class="input-group mb-2">'+
          '<div class="input-group-prepend">' +
            '<div class="input-group-text">$</div>'+
          '<input type="number" class="form-control" id="inlineFormInputGroup" name="precio">'+
          '</div>'+
        '</div>'+
      '</div>'+ //end 4 md precio
      '<div class="form-group col-md-12">'+
        '<label for="inputCity">Cantidad</label>'+
        '<select class="custom-select" name="cantidad">'+
          '<option selected>Select</option>'+
          '<option value="1">1</option>'+
          '<option value="2">2</option>'+
          '<option value="3">3</option>'+
        '</select>'+
      '</div>'+ // end Cantidad
    '</div>'+ // end first block
    '<div class="form-group col-md-8">'+
      '<label for="inputCity">Articulo</label>'+
      '<textarea class="form-control" id="exampleFormControlTextarea1" rows="5" name="articulo"></textarea>'+
    '</div>'
  );

});

});
