$(document).ready(function(){
    get_products();
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

    function get_products(){
        $.ajax({
            beforeSend:function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
                }
            },
            type:'GET',
            url:'products/',
            success: function(data){   
             create_cards(data);
            }
        });
    }

    function create_cards(data){
        var card_array_unisex = [];
        var card_array_womens = [];
        var card_array_mens = [];
        var card = $('<div />', {'class':"card item-card flex-item"});
        for(key in data){
            if(data[key]['quantity'] == 0) continue;
            var product_detail = $('<a />', {'class':'product-detail','href':'product/'+data[key]['catalogue_code']+'/'})
            var img = $('<img />', {'class':'card-image-top', 'src':data[key]['shoe_image']}).appendTo(card);
            var card_body = $('<div />', {'class':'card-body'});
            var card_title = $('<h5 />', {'class':'card-title', html:data[key]['name']}).appendTo(card_body);
            var card_text = $('<p />', {'class':'card-text price-text', html:'£'+data[key]['price']}).appendTo(card_body);
            card.append(card_body);
            product_detail.append(card);
            if (data[key]['gender_category'] === 'U') {
                card_array_unisex.push(product_detail);
                card = $('<div />', {'class':"card item-card"});
            }
            else if (data[key]['gender_category'] === 'F') {
                card_array_womens.push(product_detail);
                card = $('<div />', {'class':"card item-card"});
            }
            else if (data[key]['gender_category'] === 'M'){ 
                card_array_mens.push(product_detail);
                card = $('<div />', {'class':"card item-card"});
            }
        }
        append_category(card_array_unisex, 'U');
        append_category(card_array_womens, 'F');
        append_category(card_array_mens, 'M');
    }

    function append_category(card_array, query){
        var length = 3; // 3 represents 4 (array index numbering)
        var data_slide_to = 0;
        var carousel = '';
        var indicator_append = ''
        var carousel_item = $('<div />', {'class':'carousel-item flex-container'});
        var carousel_indicator = '';
        if(query == 'U') {
            carousel = $("#unisex-inner");
            indicator_append = 'unisex-indicators';
        } 
        if(query == 'F') {
            carousel = $("#womens-inner");
            indicator_append = 'womens-indicators';
        }
        if(query == 'M'){
            carousel = $("#mens-inner");
            indicator_append = 'mens-indicators';
        } 
        for(let i=0; i<card_array.length; i++){
            if(i==0){
                carousel_indicator = $('<li />', {'data-target':"#"+indicator_append, 'data-slide-to':data_slide_to}).appendTo('#'+indicator_append);
            }
            if(i > length){
                data_slide_to++;
                length += length;
                carousel_item = $('<div />', {'class':'carousel-item flex-container'});
                carousel_indicator = $('<li />', {'data-target':"#"+indicator_append, 'data-slide-to':data_slide_to}).appendTo('#'+indicator_append);
            }
            $(carousel_item).append($(card_array[i]));
            $(carousel).append($(carousel_item));
            $(carousel).children(':first-child').addClass('active');
            $("#"+indicator_append).children(':first-child').addClass('active');
        }
    }
});