var user = document.currentScript.getAttribute("user");
var basket = document.currentScript.getAttribute("basket");
var previously_clicked_btn =  null;
function button_clicked(button){
    parent = document.getElementById("append-sizes")
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
    parent.classList.remove("highlight");
    button.classList.remove(class1);
    button.classList.add(class2);
    return;
}

$(document).ready(function(){
    $("#shipping-form").hide();
    var basket_cookies = updateCookies("basket", basket);
    update_cookie_basket();
    function update_cookie_basket(){
        basket = JSON.parse(JSON.parse(getCookie("basket")));
        const container = $("#append-basket-detail").html("");
        $("#basket").html(basket["order"]["basket_items"] + " items in basket (£" + basket["order"]["basket_total"]+")");
        $("#total").html("£" + basket["order"]["basket_total"]);
        if(basket["items"].length == 0){
            empty_message = $("<div />", {"class":"text-center text-black font-weight-bold my-5", html:"Basket is empty. Add items to continue"});
            container.append(empty_message);
            $("button[id='checkout-btn']").prop("disabled", true);
            return;
        }
        else{
            $("button[id='checkout-btn']").prop("disabled", false);
        }
        items = basket["items"];
        for(key in items){
            const minus = $("<span />", {html:"&#8722;"});
            const plus = $("<span />", {html:"&#43;"});
            const img = $("<img />", {"src": "/media/"+items[key]["shoe"]["image"], "id":"basket-product-image"});
            const img_container = $("<div />", {"class":"col-lg-4 col-sm-4 col-4 product-img", "id":"image-container"}).append(img);
            const basket_detail = $("<div />", {"class":"row basket-detail"}).append(img_container);
            const product_quantity = $("<p />", {"class":"basket-product-quantity text-black align-self-center mr-5", html:"Quantity: "});
            const minus_quantity = $("<button />", {"class":"btn font-weight-bold", "id":"change-quantity", "data-action":"decrement"}).append(minus);
            const plus_quantity = $("<button />", {"class":"btn font-weight-bold", "id":"change-quantity", "data-action":"increment"}).append(plus);
            const quantity_input = $("<input />", {"class":"form-control mr-sm-2 shoe-quantity-basket", "type":"number", "value":items[key]["shoe"]["quantity"], "min":1, "max":items[key]["shoe"]["stock"]});
            const quantity_array = [product_quantity, minus_quantity, quantity_input, plus_quantity];
            const product_name = $("<p />", {"class":"font-weight-bold", "id":"basket-product-name", html:items[key]["shoe"]["name"], "data-code":items[key]["code"]});
            const product_size = $("<p />", {"class":"text-black font-weight-bold d-inline", "id":"basket-product-size", html:items[key]["shoe"]["size"]});
            const size_container = $("<div />", {"class":"py-2", html:"Size: "}).append(product_size);
            const quantity_container = $("<div />", {"class":"custom-input my-3"}).append(quantity_array);
            const product_price = $("<p />", {"class":"text-black font-weight-bold d-inline", html:"£"+items[key]["shoe"]["price"]});
            const price_container = $("<div />", {"class":"py-2", html:"Price: "}).append(product_price);
            const product_total = $("<p />", {"class":"float-left basket-product-price text-black font-weight-bold mx-0", html:"£"+items[key]["total"]});
            const remove_link = $("<u />", {"class":"float-right", "id":"remove-link", html:"Remove"});
            const product_array = [product_name, size_container, price_container, quantity_container, product_total, remove_link];
            const basket_product = $("<div />", {"class":"col-lg-8 col-sm-8 col-8 basket-product"}).append(product_array);
            basket_detail.append(basket_product);
            container.append(basket_detail);
        }
        return;
    }

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

    function updateCookies(name, updated_cookie=null){
        var cookie = JSON.parse(getCookie(name))
        if(cookie == undefined) {
            cookie = {}
        }
        if(updated_cookie !== null) cookie = updated_cookie;
        document.cookie = name+"=" + JSON.stringify(cookie) + ";domain=;path=/";
        return cookie;
    }

    function size_in_items(items, size){
        for(let i = 0; i<items.length; i++){
            if(parseFloat(items[i]["shoe"]["size"]) == parseFloat(size)) return true;
        }
        return false;
    }

    function code_in_items(items, code){
        for(let i = 0; i<items.length; i++){
            if(items[i]["code"] == code) return true;
        }
        return false;
    }

    function updateCookieItems(catalogue_code, quantity, size, action){
        basket_cookies = JSON.parse(JSON.parse(getCookie("basket")));
        if(action == "add"){
            // If there is no indication of an array named "items" in the basket cookie, create a new one
            if(basket_cookies["items"] == undefined) basket_cookies["items"]=[];
            // If there are no items currently in the items array, push a new item to the item array
            if (basket_cookies["items"].length == 0){
                basket_cookies["items"].push ({
                    "code": catalogue_code, 
                    "shoe":{ "size":size, "quantity":parseInt(quantity) }
                });
            } else {
                // If there is a matching item of the same code in the item array
                var is_code_in_items = code_in_items(basket_cookies["items"], catalogue_code);
                if(is_code_in_items == true){
                    // Check if the size is in the items array and increase the quantity by the selected amount if true 
                    var is_size_in_items = size_in_items(basket_cookies["items"], size);
                    if(is_size_in_items == true){
                        // Look for the entry containing the size found
                        for(let i = 0; i<items.length; i++){
                            if(parseFloat(items[i]["shoe"]["size"]) == parseFloat(size)) basket_cookies["items"][i]["shoe"]["quantity"] += parseInt(quantity);
                        }
                        
                    } else {
                        // otherwise push a new item to the items array and break out of the loop
                        basket_cookies["items"].push ({
                            "code": catalogue_code, 
                            "shoe":{"size":size, "quantity":parseInt(quantity) }
                        });
                    }
                } else {
                    // If there are no matching items in the items array, push a new item to the items array and break out of the loop
                    basket_cookies["items"].push ({
                        "code": catalogue_code, 
                        "shoe":{"size":size, "quantity":parseInt(quantity) }
                    });
                }
            }

        }
        if(action == "increment") {
            for(key in basket_cookies["items"]){
                // Search for matching item of the same catalogue_code and size within the basket
                if(basket_cookies["items"][key]["code"] == catalogue_code && basket_cookies["items"][key]["shoe"]["size"] == size){
                    // Incriment the count by 1
                    basket_cookies["items"][key]["shoe"]["quantity"] += 1;
                }
            }
        }
        if (action == "decrement") {
            // Logic for clicking on the minus button in the basket dropdown menu
            for(key in basket_cookies["items"]){
                // Search for matching item of the same catalogue_code and size within the basket
                if(basket_cookies["items"][key]["code"] == catalogue_code && basket_cookies["items"][key]["shoe"]["size"] == size){
                    // if the quantity of the item is 0 or reaching 0, the item is removed from the basket
                    if (basket_cookies["items"][key]["shoe"]["quantity"] == 0 || (basket_cookies["items"][key]["shoe"]["quantity"] - 1) == 0){
                        delete basket_cookies["items"][key];
                    } else {
                        // Otherwise the quantity is decremented by 1
                        basket_cookies["items"][key]["shoe"]["quantity"] -= 1;
                    }
                }
            }
        }
        if(action == "delete"){
            for(key in basket_cookies["items"]){
                // Search for matching item of the same catalogue_code and size within the basket
                if(basket_cookies["items"][key]["code"] == catalogue_code && basket_cookies["items"][key]["shoe"]["size"] == size){
                    // Delete item from item array in cookies
                    delete basket_cookies["items"][key];
                }
            }
        }
        if(action == "reset"){
            // Once an order is placed, the basket, as well as the cookies should be reset. Therefore all the items in the basket must be deleted
            for(key in basket_cookies["items"]){
                    delete basket_cookies["items"][key];
            }
        }
        // For any change made to the cookies, update the document cookies and then send an asynchronous request to the server:
        // This will format an appropriate response to be appended to the cookies, containing the correct shoe data
        basket = updateCookies("basket", basket_cookies);

        $.ajax({
            beforeSend:function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                }
            },
            type: "POST",
            data:
            {"basket": basket},
            url:"update-cookies/",
            success: function(data){
                updateCookies("basket", data);
                update_cookie_basket(data);
            }
        });
        return;
    };    

    $("#btn-apply-discount").on("click", function(){
        code = $("#promo-checkbox").val()
        $.ajax({
            beforeSend:function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                }
            },
            type:"GET",
            url:"/discount/",
            data:{
                "code":code
            },
            success:function(data){
                if(data["code"] == 0){
                    $("#apply-to-me").html(data["message"]).css("color", "red");
                } else {
                    var total = parseFloat($("#order_total").attr("data-total"));
                    total = total - parseFloat(total*parseFloat(data["discount"]));
                    $("#order_total").html("£"+total.toFixed(2));
                    $("#order_total").attr("data-total",total.toFixed(2));
                    $("#apply-to-me").html(data["message"]).css("color", "green");
                }
            }
        });
    });

    $("#add-to-basket").on("click", function(){
        var quantity = $("#shoe-quantity").val();
        var size = $(".clicked").attr("id");
        if (quantity == 0 || size == undefined){
            if (quantity == 0) $("#shoe-quantity").addClass("highlight");
            if (size == undefined) $("#product-sizes").addClass("highlight");
            return;
        }
        var catalogue_code = $(".content").attr("data-code");
        updateCookieItems(catalogue_code, quantity, size,"add");        
    });
    
    $("#append-basket-detail").on("click", "#remove-link", function(){
        const code = $(this).parent().find("#basket-product-name").attr("data-code");
        const size = $(this).parent().find("#basket-product-size").html();
        updateCookieItems(code, null, size, "delete");
    });

    $("#append-basket-detail").on("click", "#change-quantity", function(){
        const code = $(this).parent().parent().find("#basket-product-name").attr("data-code");
        const size = $(this).parent().parent().find("#basket-product-size").html();
        if($(this).attr("data-action") == "increment"){
            if(parseInt($(this).parent().find(".shoe-quantity-basket").val()) + 1 > parseInt($(this).parent().find(".shoe-quantity-basket").attr("max"))) return;
            $(this).parent().find(".shoe-quantity-basket").val(function(i, current_val){
                return parseInt(current_val)+1;
            });
            updateCookieItems(code, null, size, "increment");
        } else {
            $(this).parent().find(".shoe-quantity-basket").val(function(i, current_val){
                return parseInt(current_val)-1;
            });
            updateCookieItems(code, null, size, "decrement");            
        }
    });

    $(".product-image-wrapper").on("click", "#add-to-basket-search",function(){
        var code = $(this).parent().parent().parent().attr("data-code");
        var sizes = $(this).parent().parent().parent().attr("data-sizes").split(/[ ,\[\]]+/);
        sizes = sizes.splice(1, sizes.length);
        sizes.pop();
        $("#append-sizes").html("");
        $("#searchModal").attr("data-code", "");
        $("#searchModal").attr("data-code", code);
        $("#searchModal").modal("show");
        for(let i=0; i<sizes.length; i++){
            const button = $("<button />", {'class':'btn btn-outline-custom custom-text text-center', 'onclick':'button_clicked(this)' ,'id':sizes[i], html:sizes[i]});
            $("#append-sizes").append(button); 
        }
    });

    $("#open-shipping").on("click", function(){
        $("#shipping-form").toggle(
            function(){
                $(this).animate();
            });
    });

    $("#btn-checkout").on("click", function(){
        const name = $("#name-input").val();
        const email = $("#email-input").val();
        const address = $("#address-input").val();
        const city = $("#city-input").val();
        const postcode = $("#postal-input").val();
        const total = $("#order_total").attr("data-total");
        if(name == "" || email == "" || address == "" || city == "" || postcode == "") alert("Please Fill in all fields to process order!");
        else{
            $.ajax({
                beforeSend:function(xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                    }
                },
                type: "POST",
                data:
                {
                    "name":name,
                    "email":email,
                    "address":address,
                    "city":city,
                    "postcode":postcode,
                    "total":total
                },
                url:"process-order/",
                success: function(data){
                    updateCookieItems(null, null, null, "reset");
                }
            }).done(function(data){
                response = {
                    "email":data["email"],
                    "message":data["message"],
                    "items":data["items"],
                    "transaction_id":data["transaction_id"],
                    "total_price":data["total_price"],
                    "total_items":data["total_items"],
                    "shipping":data["shipping"]
                }
                var url = "/success/?"
                var count=0
                for(key in response){
                    const param = String(key);
                    const query = JSON.stringify(response[key]);
                    if(count == 0){
                        url = url.concat(param + "=" + query);
                    } else{
                        url = url.concat("&" + param + "=" + query);
                    }
                    count++;
                }
                window.location = url;
            });
        }
    });

    $(".productinfo").on("click", "#search-product-link", function(){
        window.location = '/product/'+$(this).eq(0).attr("data-code");
    });

    $(".modal").on("click", "#add-to-basket-modal", function(){
        var code = $(".modal").attr("data-code");
        var size = $(".clicked").attr("id");
        for(let i = 0; i< basket["items"].length; i++){
            if(basket["items"][i]["code"] == code) {
                if (basket["items"][i]["shoe"]["stock"] < basket["items"][i]["shoe"]["quantity"] + 1) {
                    $(".modal").modal("hide");
                    return;
                }
            }
        }
        updateCookieItems(code, 1, size, "add");
        $(".modal").modal("hide");
    });

    $("#shoe-quantity").on("click", function(){
        if($(this).hasClass("highlight")) $(this).removeClass("highlight");
        else return; 
    });

    $('.dropdown-menu').on('click', function (e) {
        e.stopPropagation();
     });
         
});