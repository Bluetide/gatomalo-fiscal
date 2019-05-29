$(function(){
    //var audio = new Audio('{{ url_for('static', filename='audio/gatomalo.mp3') }}');
    // Sad Trombone by Joe Lamb. CC Attribution. Source: http://soundbible.com/1830-Sad-Trombone.html
    //var audio2 = new Audio('{{ url_for('static', filename='audio/sad.mp3') }}');
  //Test Invoice
  $('.test_invoice').click(function(event){
    const invoiceId = event.target.dataset.invoiceId;
    $.post("/test_no_fiscal/" + invoiceId , {});
  });
  //Get Fiscal ID Modal
  // Setup the invoice ID dialog when the user clicks a Credit Note button
          
  var getFiscalIDDialog = $('#getFiscalIDDialog');

  getFiscalIDDialog.on('show.bs.modal', function(event){
    var button = $(event.relatedTarget);
    $("#getFiscalIDDialog #invoice_id").val(button.data("id"));
  });
  // Setup the POST for the Invoice ID dialog
  $("#getFiscalIDDialog .submit").click(function(){
    getFiscalIDDialog.modal('hide');
    myApp.showPleaseWait();
    $.post("/nota_credito", $("#getFiscalIDDialog .form").serialize())
      .done(function(data){ myApp.hidePleaseWait(); location.reload(true); })
      .error(function(data){ alert(data.responseText); })
      ;
  });
  // Setup 'Print' Button
  $('.print_button').click(function(evn){
    if (confirm('Confirmar impresion de factura')) {
        myApp.showPleaseWait();
        $.get('/print_gatomalo/' + $(evn.toElement).data('id'))
        .done(function(data){ 
          console.log(data); 
          myApp.hidePleaseWait(); 
          location.reload(true); 
        })
        .error(function(data){ 
          console.log(data);
          alert(data.status); 
        });
        } else {
                return false;
        }
  });

  //Modal and Progres Bar setting
	var myApp;
	myApp = myApp || (function () {
	    var pleaseWaitDiv = $('#pleaseWaitDialog')
	    return {
		showPleaseWait: function() {
		    pleaseWaitDiv.modal();
		    $(".progress-bar").animate({width: "100%"}, 5000);
		},
		hidePleaseWait: function () {
		    pleaseWaitDiv.modal('hide');
		},

	    };
  })();
});


