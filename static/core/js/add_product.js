// Search category in existing category field with Select2
$(document).ready(function () {
    // Applying Select2 only on existing_category field
    $('#id_existing_category').select2({
      placeholder: "Select or search category",
      allowClear: true,
      width: '100%'
    });
});
