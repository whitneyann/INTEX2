$(function(context) {
    return function()
    {
        container = $("#ajax_container");
        container.load("/catalog/index.products/" + context.catid + "/");

        pnum = 1

        $("#previous").click(function(){
            previous = Number($("#Page").text())-1;
            if (previous > 0){
                container.load("/catalog/index.products/" + context.catid + "/" + previous);
                $("#Page").text(previous);
            }

        })


        $("#next").click(function(){
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
//


    }
 }(DMP_CONTEXT.get()))
// $(function(context){
//     return function(){
//         $('#ajax_container').load('/catalog/index.products/' + context.catid1 + '/')
//         var total_pages = context.myPages1
//         // pnum = (context.pnum1)
//         pnum = 1
//         console.log("hello")
//         // console.log('pnum before',context.pnum1)
//
//         $('#previous').click(function(){
//             console.log('previous works')
//             if (pnum >= 1){
//                 pnum--
//                 $('#ajax_container').load('/catalog/index.products/' + context.catid1 + '/' + pnum)
//                 $('#page_number').text(pnum)
//             }
//               // console.log('pnum previous',context.pnum1)
//         })
//         $('#next').click(function(){
//             console.log('next works', pnum)
//
//             if (pnum < total_pages ) {
//                 pnum += 1
//                 $('#ajax_container').load('/catalog/index.products/' + context.catid1 + '/' + pnum);
//                 $('#page_number').text(pnum)
//             }
//             // console.log('pnum next',context.pnum1)
//         })
//         console.log('pnum context',context.pnum1)
//         console.log('pnum-1',pnum)
//     }
// }(DMP_CONTEXT.get()))
