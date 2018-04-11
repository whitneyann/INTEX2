$(function(){
  // $("#id_quantity").closest('p').hide()
  // $("#id_reorder_trigger").closest('p').hide()
  // $("#id_reorder_quantity").closest('p').hide()
  $("#id_pid").closest('p').hide()
  $("#id_max_rental_days").closest('p').hide()
  $("#id_rental_date").closest('p').hide()
  $("#id_due_date").closest('p').hide()
  $("#id_retire_date").closest('p').hide()


  $("#id_type").on("change", function(event)
  {
    if(event.target.value == "BulkProduct")
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
    if(event.target.value == "IndividualProduct")
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
    if(event.target.value == "RentalProduct")
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
