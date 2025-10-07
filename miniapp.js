// Инициализация Telegram WebApp
const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
    // Нижняя системная кнопка Telegram
    tg.MainButton.setText("Отправить");
    tg.MainButton.show();
    tg.MainButton.onClick(() => sendBooking());
}

const form = document.getElementById("tgForm");

// Отправка по HTML-кнопке
form.addEventListener("submit", (e) => {
    e.preventDefault();
    sendBooking();
});

function sendBooking() {
    const data = Object.fromEntries(new FormData(form).entries());

    // Мини-валидация
    if (!data.name || !data.phone || !data.service || !data.date || !data.time) {
        alert("Пожалуйста, заполните все обязательные поля.");
        return;
    }

    const payload = JSON.stringify({ type: "booking", data });

    if (tg) {
        tg.sendData(payload); // отправка в бот
        tg.close();           // закрываем мини-приложение
    } else {
        alert("Данные (демо вне Telegram): " + payload);
    }
}
