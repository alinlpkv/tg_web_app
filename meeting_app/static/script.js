
$(document).ready(function() {
    let tg = window.Telegram.WebApp;
    tg.expand();

//    if (tg.initData == '') {
//        $('body').empty();
//    }

});

var currentTime = new Date();
var offset = currentTime.getTimezoneOffset();
$('#timezoneOffset').val(offset);

$('form').submit(function(event) {
    $('#errorMessageDateStart').text('');
    $('#errorMessageTheme').text('');

    if ($('#date_start').val() === '') {
        event.preventDefault();
        $('#errorMessageDateStart').text('Заполните время начала встречи');
    }
    if ($('#theme').val() === '') {
        event.preventDefault();
        $('#errorMessageTheme').text('Заполните тему встречи');
    }
});

$('#datetimepicker1').datetimepicker({
    locale: moment.locale('ru')
});
$('#datetimepicker2').datetimepicker({
    locale: moment.locale('ru'),
});

$("#datetimepicker1").on("dp.change", function (e) {
    $('#datetimepicker1').data("DateTimePicker").minDate(moment().toDate());

    var minDateValue = moment(e.date).add(1, 'minutes');
    if (!isNaN(minDateValue))  {
        $('#datetimepicker2').data("DateTimePicker").minDate(minDateValue);
    }

    var selectedTime1 = moment(e.date);
    var selectedTime2 = $('#datetimepicker2').data("DateTimePicker").date();
    if (selectedTime1.isAfter(selectedTime2)) {
        $('#datetimepicker2').data("DateTimePicker").clear();
    }
});