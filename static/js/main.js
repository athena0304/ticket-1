//counts up or down depending on date entered in //format at the bottom
// window.DOMContentLoaded = function() {
  $(document).ready(function() {
    function counter(date) {
  var theDate = new Date(date);
  var _second = 1000;
  var _minute = _second * 60;
  var _hour = _minute * 60;
  var _day = _hour * 24;
  var timer;

  function count() {
    var now = new Date();
    if (theDate > now) {
      var distance = theDate - now;
      if (distance < 0) {
        clearInterval(timer);
        return;
      }
    } else {
      var distance = now - theDate;
      if (distance < 0) {
        clearInterval(timer);
        return;
      }
    }
    var days = Math.floor(distance / _day);
    var hours = Math.floor((distance % _day) / _hour);
    if (hours < 10) {
      hours = '0' + hours;
    }
    var minutes = Math.floor((distance % _hour) / _minute);
    if (minutes < 10) {
      minutes = '0' + minutes;
    }
    var seconds = Math.floor((distance % _minute) / _second);
    if (seconds < 10) {
      seconds = '0' + seconds;
    }
    var daytext = '';
    if (days > 1) {
      daytext = ' days ';
    } else {
      daytext = ' day ';
    }
    if (days > 0) {
      // document.getElementById('counter').innerHTML = '<span class="days">' + days + '</span>' + '<span class="hours">' + hours + '</span>' + '<span class="minutes">' + minutes + '</span>' + '<span class="seconds">' + seconds + '</span>';
      document.querySelector(".days").innerHTML = days;
      document.querySelector(".hours").innerHTML = hours;
      document.querySelector(".minutes").innerHTML = minutes;
      document.querySelector(".seconds").innerHTML = seconds;

    } else {
      // document.getElementById('counter').innerHTML = '<span class="hours">' + hours + '</span>' + '<span class="minutes">' + minutes + '</span>' + '<span class="seconds">' + seconds + '</span>';
    }
  }
  timer = setInterval(count, 1000);
}

counter('06/17/2016 19:30:00 GMT-0400 (EDT)');
  });

// }



$(document).ready(function() {
    // $(".ticket_modal").height($(".ticket_img_wrapper").height());
    var ticket_models = $(".ticket_modal")
    ticket_models.each(function(index, ele) {
        $(this).css("left", index * 3.33 + "%")
    })

    var num = 15;

    ticket_models.filter(":lt(5)").addClass('hide')
});