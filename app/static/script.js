const tg = window.Telegram.WebApp;
tg.expand();


let user_name = document.getElementById("user_name");
user_name.innerText = tg.initDataUnsafe.user.first_name;

let create = document.getElementById("create");
create.addEventListener("click", () => {
    let meeting_name = document.getElementById("meeting_name").value;
    let meeting_description = document.getElementById("meeting_description").value;
    let meeting_date = document.getElementById("meeting_date").value;

    let data = {
        meeting_name: meeting_name,
        meeting_description: meeting_description,
        meeting_date: meeting_date
    };

    tg.sendData(JSON.stringify(data));
    tg.close();
});
