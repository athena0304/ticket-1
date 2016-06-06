$(document).ready(function() {
    // $(".ticket_modal").height($(".ticket_img_wrapper").height());
    var ticket_models = $(".ticket_modal")
    ticket_models.each(function(index, ele) {
        $(this).css("left", index * 3.33 + "%")
    })

    var num = 20 - parseInt($(".remain_cheer_num").eq(0).text());

    ticket_models.filter(":lt("+ num +")").addClass('hide');

    $(".info").on("click", function(){
        layer.open({
            title: [
            '长按关注官方账号',
            'background-color:#182f52; color:#fff;'
            ],
            content:"<img src='/static/img/qrcode.png'></img><p>长按关注G-STEPS街舞社可随时咨询问题</p>",
        })
    })

});