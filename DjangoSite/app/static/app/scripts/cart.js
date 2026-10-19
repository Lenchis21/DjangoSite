document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.quantity').forEach(counter => {
        const input = counter.querySelector('.quantity__input');
        const minus = counter.querySelector('.quantity__btn--minus');
        const plus = counter.querySelector('.quantity__btn--plus');

        const itemId = counter.dataset.id;
        const price = parseFloat(counter.dataset.price) || 0;

        function recalculate() {
            let qty = parseInt(input.value);
            let rowSubtotal = qty * price;

            // 1. Обновляем сумму в строке
            const subtotalEl = document.getElementById(`subtotal-${itemId}`);
            if (subtotalEl) subtotalEl.innerText = rowSubtotal.toFixed(2);

            // 2. Пересчитываем общий итог
            let total = 0;
            document.querySelectorAll('.quantity').forEach(c => {
                const q = parseInt(c.querySelector('.quantity__input').value);
                const p = parseFloat(c.dataset.price) || 0;
                total += q * p;
            });

            const totalEl = document.getElementById('cart-total');
            if (totalEl) totalEl.innerText = total.toFixed(2);
        }

        plus.addEventListener('click', () => {
            let value = parseInt(input.value);
            input.value = ++value;
            minus.classList.remove('min');
            recalculate(); // Пересчитываем визуально
        });

        minus.addEventListener('click', () => {
            let value = parseInt(input.value);
            if (value > 1) {
                input.value = --value;
                if (value === 1) minus.classList.add('min');
                recalculate(); // Пересчитываем визуально
            }
        });
    });
});