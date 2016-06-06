$(document).ready(function() {
    // $(".ticket_modal").height($(".ticket_img_wrapper").height());
    var ticket_models = $(".ticket_modal")
    ticket_models.each(function(index, ele) {
        $(this).css("left", index * 3.33 + "%")
    })

    var num = 15;

    ticket_models.filter(":lt(5)").addClass('hide')
});
