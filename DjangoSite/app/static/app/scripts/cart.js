document.addEventListener('DOMContentLoaded', function () {
    // Получаем токен CSRF (нужен для Django)
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    if (!csrfToken) {
        console.error('CSRF token не найден!');
    }

    function updateCart(itemId, action) {
        console.log(`Отправка запроса: ID=${itemId}, action=${action}`); // Для отладки

        const formData = new FormData();
        formData.append('action', action);
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch(`/cart/ajax/update/${itemId}/`, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка сервера: ' + response.status);
                return response.json();
            })
            .then(data => {
                console.log('Ответ сервера:', data); // Для отладки

                if (data.status === 'deleted') {
                    location.reload();
                } else {
                    document.getElementById(`qty-${itemId}`).innerText = data.quantity;
                    document.getElementById(`subtotal-${itemId}`).innerText = data.subtotal;
                    document.getElementById('cart-total').innerText = data.total;
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    }

    // Находим все кнопки и вешаем на них события
    const btnPlusList = document.querySelectorAll('.btn-plus');
    const btnMinusList = document.querySelectorAll('.btn-minus');

    console.log(`Найдено кнопок ПЛЮС: ${btnPlusList.length}`);
    console.log(`Найдено кнопок МИНУС: ${btnMinusList.length}`);

    btnPlusList.forEach(btn => {
        btn.addEventListener('click', function () {
            updateCart(this.dataset.id, 'plus');
        });
    });

    btnMinusList.forEach(btn => {
        btn.addEventListener('click', function () {
            updateCart(this.dataset.id, 'minus');
        });
    });
});