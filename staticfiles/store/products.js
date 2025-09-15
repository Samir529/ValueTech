// Filter section

// Price Range live update
$("#priceRange").on("input", function() {
$("#priceValue").text($(this).val());
applyFilters();
});

// Checkbox and category clicks
$(".filter, .category-pill").on("change click", function() {
$(".category-pill").removeClass("active-pill");
$(this).addClass("active-pill");
applyFilters();
});

// AJAX filter
function applyFilters() {
let price = $("#priceRange").val();
let availability = [];
$(".filter:checked").each(function() {
  availability.push($(this).val());
});
let category = $(".active-pill").data("category");

$.ajax({
  url: "{% url 'filter_products' %}",
  data: {
    price: price,
    availability: availability.join(","),
    category: category,
  },
  success: function(data) {
    $("#product-list").html(data.html);
  }
});
}
