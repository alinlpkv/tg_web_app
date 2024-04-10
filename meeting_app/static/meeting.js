

$(document).ready(function() {
    let tg = window.Telegram.WebApp;
    tg.expand();

    //    if (tg.initData == '') {
    //        $('body').empty();
    //    }

    fetchData();

});


async function fetchData() {
    let user_id = 342297636;
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

