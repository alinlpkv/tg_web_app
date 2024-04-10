
$(document).ready(function() {
    let tg = window.Telegram.WebApp;
    tg.expand();

    //    if (tg.initData == '') {
    //        $('body').empty();
    //    }

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


async function postData(user_data) {
      let tg = let tg = window.Telegram.WebApp;
      console.log(tg.InitData);
//    console.log(user_data)
//    let user_id = 342297636;
//    try {
//        const response = await fetch("http://localhost:8020/meeting/create");
//        const responseData = await response.text();
//        console.log(responseData)
//
//        if (responseData === 'OK') {
//            console.log('ok')
//        }
//    console.log('finish');
//
//    } catch (error) {
//        console.error("Ошибка при получении данных:", error);
//    }
};


$('form').submit(function(event) {
    $('#errorMessageDateStart').text('');
    $('#errorMessageTheme').text('');

//    if ($('#date_start').val() === '') {
//        event.preventDefault();
//        $('#errorMessageDateStart').text('Заполните время начала встречи');
//    }
    if ($('#theme').val() === '') {
        event.preventDefault();
        $('#errorMessageTheme').text('Заполните тему встречи');
    }

    let theme = $('#theme').val();
    let date_start = $('#date_start').val();
    let date_end = $('#date_end').val();
    let description = $('#description').val();
    var currentTime = new Date();
    var offset = currentTime.getTimezoneOffset();

    let meeting_data = {
        theme: theme,
        date_start: date_start,
        date_end: date_end,
        description: description,
        timezone: offset
    };

    postData(meeting_data);

});