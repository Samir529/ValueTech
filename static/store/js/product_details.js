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


// Product's Extra images, Sizes, Color etc.
let currentIndex = 0;
const images = [...document.querySelectorAll('.thumb-img')].map(img => img.src);

function changeImage(src) {
    document.getElementById('mainProductImage').src = src;
    document.getElementById('modalImage').src = src;
    currentIndex = images.indexOf(src);
}

function prevImage() {
    if (currentIndex > 0) currentIndex--;
    else currentIndex = images.length - 1;
    document.getElementById('modalImage').src = images[currentIndex];
}

function nextImage() {
    if (currentIndex < images.length - 1) currentIndex++;
    else currentIndex = 0;
    document.getElementById('modalImage').src = images[currentIndex];
}

// Disable color buttons until size is selected
const sizeBtns = document.querySelectorAll(".size-btn");
const colorBtns = document.querySelectorAll(".color-btn");

if (sizeBtns.length > 0 && colorBtns.length > 0) {
    colorBtns.forEach(btn => btn.disabled = true);

    sizeBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            sizeBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            colorBtns.forEach(c => c.disabled = false);
        });
    });
}
