$('#slider1, #slider2, #slider3').owlCarousel({
    

    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})





$('.plus-cart').on('click', function() {

    var id = $(this).attr("pid").toString();
    // elm's parentnode is the quantity label and it's second children is quantity span in which real
// quantity is shown
    var elm = this.parentNode.children[2];
    console.log("clickable");
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success: function (data) {
            elm.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            console.log(data);
            // console.log("success")
            
        }
    })
  });
  $('.minus-cart').on('click', function() {

    var id = $(this).attr("pid").toString();
    var elm = this.parentNode.children[2];
    // console.log("clickable")
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success: function (data) {
            elm.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            // console.log(data)
            // console.log("success")
            
        }
    })
})

$('.remove-cart').on('click', function() {

    var id = $(this).attr("pid").toString();
    var elm = this
    console.log("clickable")
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success: function (data) {
            elm.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            elm.parentNode.parentNode.parentNode.parentNode.remove();
            // console.log(data)
            console.log("success")
            
        }
    })
})





// elm's parentnode is the quantity label and it's second children is quantity span in which real
// quantity is shown