$(function(){
  $('.test_invoice').click(function(event){
    var invoiceId = event.target.dataset.invoiceId;
    $.post("/test_no_fiscal/" + invoiceId , {});
  });
});
