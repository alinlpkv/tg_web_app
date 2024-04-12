let tg = window.Telegram.WebApp;

//if (tg.initDataUnsafe == '') {
//    $('body').empty();
//}

//let user_id = tg?.initDataUnsafe?.user?.id || 342297636;
let user_id = tg?.initDataUnsafe?.user?.id;

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
        let query = `?user_id=${user_id}&theme=${user_data.theme}&` +
                    `date_start=${user_data.date_start}&date_end=${user_data.date_end}&` +
                    `description=${user_data.description}&timezone=${user_data.timezone}`;

        console.log(query);
        fetch(`http://localhost:8020/meeting/create${query}`)
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
    if ($('#theme').val().trim() === '') {
        event.preventDefault();
        $('#errorMessageTheme').text('Заполните тему встречи');
        return;
    }

    let meeting_data = {
        theme: $('#theme').val(),
        date_start: $('#date_start').val(),
        date_end: $('#date_end').val() || '',
        description: $('#description').val() || '',
        timezone: new Date().getTimezoneOffset()
    };

    postData(meeting_data).
        then(function(response) {
            console.log('Данные успешно отправлены на сервер');
            $('form')[0].reset();
            window.location.href = 'https://alinlpkv.github.io/tg_web_app/meeting_app/templates/meeting.html';
        })
        .catch(function(error) {
            console.error('Ошибка при отправке данных на сервер:', error);
        });

});
