

$(document).ready(function() {
    let tg = window.Telegram.WebApp;
    tg.expand();

    if (tg.initData == '') {
        $('body').empty();
    }

    let user_id = tg.initDataUnsafe.user.id

    fetchData(user_id);

});


async function fetchData(id_) {
    let user_id = id_;
    try {
        const response = await fetch("http://localhost:8020/meeting/show/" + user_id);
        const responseData = await response.json();

        if (responseData.length == 0) {
            const deleteElement = document.querySelector("#container");
            deleteElement.innerHTML = '';
        }

        console.log(responseData);
        console.log(responseData[0].theme);

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

