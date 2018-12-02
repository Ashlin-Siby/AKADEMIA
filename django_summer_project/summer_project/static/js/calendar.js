
$(document).ready(function(){
  $('.hello-week__header').click(function() {
    var monthLabel = $('.hello-week__label').text();
    var month = monthLabel.substr(0, 3);
    showCalEvents(month);
    $(".eventsEntry").load(" .eventsEntry");

  });
  $('.hello-week__day').click(function() {
    var inner = this.innerHTML;
    var monthLabel = $(".hello-week__label").text();
    var month = monthLabel.substr(0, 3);
    if(inner.length == 1){
      showEventsToday("0" + this.innerHTML, month);
    }
    else{
      showEventsToday(this.innerHTML, month);
    }
 });
});

$(document).click(function(){

  $('.hello-week__day').click(function() {
    var inner = this.innerHTML;
    var monthLabel = $(".hello-week__label").text();
    var month = monthLabel.substr(0, 3);
    if(inner.length == 1){
      showEventsToday("0" + this.innerHTML, month);
    }
    else{
      showEventsToday(this.innerHTML, month);
    }
 });
});


function showCalEvents(month) {

  var cur = "";
  console.log(history.pushState(cur, '',month));
}

function showEventsToday(date, month) {
  $('.hello-week__day').attr('onclick',window.location.href="eventsToday/" + date + "/" + month);
}
