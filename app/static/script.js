$(document).ready(function() {
        let tg = window.Telegram.WebApp;
        tg.expand();

        $('#create').click(function() {
            let meeting_name = $('#meeting_name').val();
            let meeting_description = $('#meeting_description').val();
            let meeting_date = $('#datetimepicker1').find('input').val(); // Здесь исправление

            let data = {
                meeting_name: meeting_name,
                meeting_description: meeting_description,
                meeting_date: meeting_date
            };

            tg.sendData(JSON.stringify(data));
            tg.close();
        });

        $('#datetimepicker1').datetimepicker({
            locale: moment.locale('ru')
        });
    });