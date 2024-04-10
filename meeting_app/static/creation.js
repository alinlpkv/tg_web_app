
$(document).ready(function() {
    let tg = window.Telegram.WebApp;

    if (tg.initDataUnsafe == '') {
        $('body').empty();
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


function postData(user_data) {
    return new Promise(function(resolve, reject) {
        let tg = window.Telegram.WebApp;
//        let user_id = tg.initDataUnsafe.user.id
        let user_id = 342297636;
        let query = "?user_id=" + user_id + "&" + "theme=" + user_data.theme +"&" + "date_start="+ user_data.date_start + "&" + "date_end="+ user_data.date_end + "&" +"description=" + user_data.description +  "&" +"timezone=" + user_data.timezone;
        console.log(query);
        fetch("http://localhost:8020/meeting/create" + query)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка при отправке данных на сервер: ' + response.statusText);
                }
                return response.text();
            })
            .then(data => {
                resolve(data);
            })
            .catch(error => {
                reject(error);
            });
    });
};


$('#create').click(function(event) {
    event.preventDefault();

    $('#errorMessageDateStart').text('');
    $('#errorMessageTheme').text('');

    if ($('#date_start').val() === '') {
        event.preventDefault();
        $('#errorMessageDateStart').text('Заполните время начала встречи');
        return;
    }
    if ($('#theme').val() === '') {
        event.preventDefault();
        $('#errorMessageTheme').text('Заполните тему встречи');
        return;
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

    postData(meeting_data).
        then(function(response) {
            console.log('Данные успешно отправлены на сервер');
            $('form')[0].reset();
            location.href = 'https://alinlpkv.github.io/tg_web_app/meeting_app/templates/meeting.html';
        })
        .catch(function(error) {
            console.error('Ошибка при отправке данных на сервер:', error);
        });

//    event.preventDefault();
});