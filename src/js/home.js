$(document).ready(function() {
    // $(".ticket_modal").height($(".ticket_img_wrapper").height());
    var ticket_models = $(".ticket_modal")
    ticket_models.each(function(index, ele) {
        $(this).css("left", index * 3.33 + "%")
    })

    var num = 20 - parseInt($(".remain_cheer_num").eq(0).text());

    ticket_models.filter(":lt("+ num +")").addClass('hide')
});