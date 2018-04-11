$(function(context) {
    return function()
    {
        container = $("#ajax_container");
        container.load("/catalog/index.products/" + context.catid + "/");


        $("#pLeft").click(function(){
            previous = Number($("#Page").text())-1;
            if (previous > 0){
                container.load("/catalog/index.products/" + context.catid + "/" + previous);
                $("#Page").text(previous);
            }

        })


        $("#pRight").click(function(){
            next = Number($("#Page").text())+1;
            total = Number(context.pagenum);
            if (next <= total){
                container.load("/catalog/index.products/" + context.catid + "/" + next);
                $("#Page").text(next);
            }

        })

        $("#name").each(function () {
            if ($(this).attr('href') === window.location.pathname) {
                $(this).css('color', 'orange');
            }
        });



    }
 }(DMP_CONTEXT.get()))




