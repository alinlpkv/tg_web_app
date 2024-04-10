
$(document).ready(function() {
    let tg = window.Telegram.WebApp;
    tg.expand();

    //    if (tg.initData == '') {
    //        $('body').empty();
    //    }

    fetchData();

});


async function fetchData() {
    let user_id = 34229763;
    try {
        const response = await fetch("http://localhost:8000/meeting/" + user_id);
        const responseData = await response.json();
        const deleteElement = document.querySelector("#container");
        deleteElement.innerHTML = '';

        console.log(responseData)

        $.each(responseData, function(index, meeting) {
            $('#meetingTable tbody').append('<tr><td>' + meeting.theme + '</td><td>' + meeting.date_start + '</td></tr>');
        });
        if (responseData.length > 0) {
            $('#noMeeting').text('');
        };
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    }
};


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