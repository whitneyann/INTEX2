$(function(){
  // $("#id_quantity").closest('p').hide()
  // $("#id_reorder_trigger").closest('p').hide()
  // $("#id_reorder_quantity").closest('p').hide()
  $("#id_pid").closest('p').hide()
  $("#id_max_rental_days").closest('p').hide()
  $("#id_rental_date").closest('p').hide()
  $("#id_due_date").closest('p').hide()
  $("#id_retire_date").closest('p').hide()
  $("#id_type").closest('p').hide()


  $(function()
  {
    if($('#id_type').val() == "BulkProduct")
    {
      $("#id_quantity").closest('p').show()
      $("#id_reorder_trigger").closest('p').show()
      $("#id_reorder_quantity").closest('p').show()
      $("#id_pid").closest('p').hide()
      $("#id_max_rental_days").closest('p').hide()
      $("#id_rental_date").closest('p').hide()
      $("#id_due_date").closest('p').hide()
      $("#id_retire_date").closest('p').hide()
    }
    if($('#id_type').val() == "IndividualProduct")
    {
      $("#id_pid").closest('p').show()
      $("#id_quantity").closest('p').hide()
      $("#id_reorder_trigger").closest('p').hide()
      $("#id_reorder_quantity").closest('p').hide()
      $("#id_max_rental_days").closest('p').hide()
      $("#id_rental_date").closest('p').hide()
      $("#id_due_date").closest('p').hide()
      $("#id_retire_date").closest('p').hide()
    }
    if($('#id_type').val() == "RentalProduct")
    {
      $("#id_quantity").closest('p').hide()
      $("#id_reorder_trigger").closest('p').hide()
      $("#id_reorder_quantity").closest('p').hide()
      $("#id_pid").closest('p').hide()
      $("#id_max_rental_days").closest('p').show()
      $("#id_rental_date").closest('p').show()
      $("#id_due_date").closest('p').show()
      $("#id_retire_date").closest('p').show()
    }
  })});
