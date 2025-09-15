// Quantity
document.addEventListener("DOMContentLoaded", function () {
    const qtyInput = document.getElementById("quantityInput");
    const hiddenQty = document.getElementById("buyNowQuantity");

    document.getElementById("increaseQty").addEventListener("click", function () {
        qtyInput.value = parseInt(qtyInput.value) + 1;
        hiddenQty.value = qtyInput.value;
    });

    document.getElementById("decreaseQty").addEventListener("click", function () {
        let current = parseInt(qtyInput.value);
        if (current > 1) {
            qtyInput.value = current - 1;
            hiddenQty.value = qtyInput.value;
        }
    });

    // Keep hiddenQty in sync if user types manually
    qtyInput.addEventListener("input", function () {
        let val = parseInt(qtyInput.value);
        if (isNaN(val) || val < 1) val = 1;
        qtyInput.value = val;
        hiddenQty.value = val;
    });
});
