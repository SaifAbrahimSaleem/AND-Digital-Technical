$(document).ready(function(){
    function render_response(data){
        const container = $("#append-search-results").html("");
        for(key in data){
            const img = $("<img />", {"src": data[key]["shoe_image"], "id":"search-product-image"});
            const img_container = $("<div />", {"class":"col-lg-4 col-sm-4 col-4 product-img", "id":"image-container"}).append(img);
            const search_detail = $("<div />", {"class":"row search-detail"}).append(img_container);
            const product_name = $("<p />", {"class":"font-weight-bold", "id":"search-product-name", html:data[key]["name"]});
            const product_collection = $("<p />", {"class":"ml-2 mt-1 text-muted", "style":"font-size:12px;", "id":"search-product-name", html:data[key]["collection"]});
            const product_title = $("<div />", {"class":"py-2 d-flex flex-row"}).append([product_name, product_collection])
            const product_price = $("<p />", {"class":"text-black font-weight-bold d-inline", html:"£"+data[key]["price"]});
            const price_container = $("<div />", {"class":"py-2", html:"Price: "}).append(product_price);
            const product_array = [product_title, price_container];
            const search_product = $("<div />", {"class":"col-lg-8 col-sm-8 col-8 mx-auto my-auto search-product"}).append(product_array);
            search_detail.append(search_product);
            const link_to_product = $("<a />", {"id":"redirect-product","data-code":data[key]["catalogue_code"]}).append(search_detail);
            container.append(link_to_product);
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


    $("#search-products").on("keyup", function(){
        min_length = 3
        search_text = $(this).val();
        if(search_text.length >= min_length){
            $.ajax({
                beforeSend:function(xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                    }
                },
                type:"GET",
                url:"searchbar/",
                data:{
                    "search_text":search_text
                },
                success: function(data){
                    $("#searchbar").show();
                    render_response(data);
                }
            });
        } else {
            $("#searchbar").hide();
        }

    });

    $("#append-search-results").on("click", "#redirect-product", function(){
        window.location = '/product/'+$(this).attr("data-code");
    })
});