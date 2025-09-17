document.addEventListener("DOMContentLoaded", function() {
    // Updating Shipping and Total price depending on the Payment methods (cod outside or cod inside)
    // toggle Outside cod field and Inside cod field
    // format total price with commas

    const codOutside = document.getElementById("cod_outside");
    const codInside = document.getElementById("cod_inside");
    const outsideCodField = document.getElementById("outside-cod-field");
    const insideCodField = document.getElementById("inside-cod-field");
    const transactionInput = document.getElementById("transaction_id");

    const subtotalEl = document.getElementById("subtotal");
    const shippingEl = document.getElementById("shipping");
    const totalEl = document.getElementById("total");

    // read the raw numeric subtotal from data attribute (no commas)
    const subtotal = parseInt(subtotalEl.dataset.subtotal) || 0;

    function toggleOutsideCodField() {
        if (codOutside.checked) {
            outsideCodField.style.display = "block";
            transactionInput.setAttribute("required", "required");
        } else {
            outsideCodField.style.display = "none";
            transactionInput.removeAttribute("required");
            transactionInput.value = "";
        }
    }

    function toggleInsideCodField() {
        if (codInside.checked) {
            insideCodField.style.display = "block";
            transactionInput.setAttribute("required", "required");
        } else {
            insideCodField.style.display = "none";
            transactionInput.removeAttribute("required");
            transactionInput.value = "";
        }
    }

    function formatAmount(n) {
        // format with commas
        return Number(n).toLocaleString("en-US");
    }

    function updateShippingAndTotal() {
        let shipping = 0;
        if (codOutside.checked) {
            shipping = 100;
        } else if (codInside.checked) {
            shipping = 60;
        }
        shippingEl.textContent = shipping;
        const total = subtotal + shipping;
        totalEl.textContent = formatAmount(total);
    }

    toggleOutsideCodField();
    toggleInsideCodField();
    updateShippingAndTotal();

    [codOutside, codInside].forEach(radio => {
        radio.addEventListener("change", function() {
            toggleOutsideCodField();
            toggleInsideCodField();
            updateShippingAndTotal();
        });
    });


    // District search filter
    // Show districts in the dropdown as user types

    const districtSearch = document.getElementById("districtSearch");
    const districtOptions = document.querySelectorAll(".district-option");
    const districtInput = document.getElementById("districtInput");
    const districtDropdown = document.getElementById("districtDropdown");

    districtOptions.forEach(option => {
        option.addEventListener("click", function(e) {
            e.preventDefault();
            districtDropdown.textContent = this.textContent;
            districtInput.value = this.textContent;
        });
    });

    districtSearch.addEventListener("keyup", function() {
        const filter = this.value.toLowerCase();
        districtOptions.forEach(option => {
            const text = option.textContent.toLowerCase();
            option.style.display = text.includes(filter) ? "" : "none";
        });
    });
});
