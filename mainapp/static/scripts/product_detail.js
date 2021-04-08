var previously_clicked_btn =  null;
function button_clicked(button){
    parent = document.getElementById("product-sizes")
    parent.classList.remove("highlight");
    const contains_class = button.classList.contains("clicked")
    if(previously_clicked_btn == null){
        previously_clicked_btn = button;
    } else {
        toggle_button( previously_clicked_btn, "clicked", "btn-outline-custom", parent);
    }
    if(contains_class == true) {
        toggle_button(button, "clicked", "btn-outline-custom", parent);
        
        return;
    } 
    toggle_button(button, "btn-outline-custom", "clicked", parent);
    
    previously_clicked_btn = button;

    return;
}

function toggle_button(button, class1, class2, parent){
    input = document.getElementById("shoe-quantity");
    if (class1 == "clicked") input.value = 0;
    else {
        input.value = 1;
        input.classList.remove("highlight");
        parent.classList.remove("highlight");
    }
    button.classList.remove(class1);
    button.classList.add(class2);
    return;
}

$(document).ready(function(){
    get_product_detail();
    var rating = 0;
    var product_quantity = 0;
    var code = $("#detail").attr("code");
    var previously_clicked_tab = $(".tab-link").eq(0).addClass("active-tab"); 
    $(".info-sections").children().hide();
    $("#"+previously_clicked_tab.attr("data-target")).show(); 

    function getCookie(name) {
        // Split cookie string and get all individual name=value pairs in an array
        var cookieArr = document.cookie.split(";");
        // Loop through the array elements
        for(var i = 0; i < cookieArr.length; i++) {
            var cookiePair = cookieArr[i].split("=");
            /* Removing whitespace at the beginning of the cookie name
            and compare it with the given string */
            if(name == cookiePair[0].trim()) {
                // Decode the cookie value and return
                return decodeURIComponent(cookiePair[1]);
            }
        }
        // Return null if not found
        return null;
    }

    var csrfmiddlewaretoken = getCookie("csrftoken");

    function get_product_detail(){
        $.ajax({
            beforeSend:function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                }
            },
            type:'GET',
            url:'detail/',
            success:function(data){
                var product_quantity;
                for(key in data){
                    switch (key){
                        case "name":
                            $("#product-name").html(data[key]);
                            break;
                        case "collection":
                            $("#product-collection").html(data[key]);
                            break;
                        case "price":
                            $("#product-price").html("£"+data[key]);
                            break;
                        case "shoe_image":
                            $("#product-image").attr("src", data[key]);
                            break;
                        case "sizes":
                            for(let i=0; i<data[key].length; i++){
                                const button = $("<button />", {'class':'btn btn-outline-custom custom-text text-center', 'onclick':'button_clicked(this)' ,'id':data[key][i], html:data[key][i]});
                                $("#product-sizes").append(button); 
                            }
                            break;
                        case "quantity":
                            product_quantity = data[key];
                            $("#shoe-quantity").attr("max", product_quantity)
                            break;
                        case "description":
                            $("#product-description").html(data[key]);
                            break;
                        case "materials":
                            $("#product-materials").html(data[key]);
                            break;
                        case "colour":
                            $("#product-colour").html(data[key]);
                            break;
                    }
                }
                if(product_quantity <= 0){
                    out_of_stock = $("<p />", {"class":"out-of-stock text-center", html:"We're sorry but this item is currently OUT OF STOCK"});
                    $("#quantity-title").hide();
                    $("#size-title").hide();
                    $("#add-to-basket").hide();
                    $(".custom-input").hide();
                    $("#product-sizes").html("").append(out_of_stock);
                }   
            }
        });
    }

    $("#rating-form").on("submit", function(event){
        event.preventDefault();
        var checked_val;
        var review_text = $("#review-text").val();
        var code = $(this).attr("data-code");
        for(let i=1; i<=5; i++){
            if($('#star'+i).is(':checked')){
                checked_val = $("#star"+i).attr("value")
            }
        }
        $.ajax({
            beforeSend:function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                }
            },
            type:"POST",
            url:"/review/",
            data:{
                "code":code,
                "rating":checked_val,
                "review":review_text
            },
            success:function(data){
                if(data["code"]==1){
                    location.reload();
                }
            }
        });
        
    });

    $(".tab-link").on("click", function(){
        previously_clicked_tab.removeClass("active-tab");
        $(this).addClass("active-tab");
        $(".info-sections").children().hide();
        $("#"+$(this).attr("data-target")).show();
        previously_clicked_tab = $(this);
    });
});

