var slider_left = document.getElementById("slider-left");
var slider_right = document.getElementById("slider-right");
var thumb_left = document.querySelector(".slider > .thumb.left");
var thumb_right = document.querySelector(".slider > .thumb.right");
var range = document.querySelector(".slider > .range");
var thumb_info_left = document.getElementById("append-info-left");
var thumb_info_right = document.getElementById("append-info-right");
var left_val;
var right_val;
var price_array = [];
var show = function(element){ element.style.display = "block"; }
var hide = function(element){ element.style.display = "none"; }
function find_max_price(){
    var headings = document.getElementsByClassName("item-price");
    for(let i = 0; i<headings.length; i++){
        price_array.push(headings[i].innerHTML);
    }
    price_array = price_array.map(Number).sort(function(a, b){
        return a-b;
    });
    return;
}
find_max_price();
max_val = price_array.pop();
slider_left.setAttribute("max", max_val)
slider_right.setAttribute("max", max_val)

function filter_items(){
    items = document.getElementsByClassName("product-image-wrapper");
    for(let i = 0; i<items.length; i++){
        item_price = parseFloat(items[i].querySelector(".item-price").innerHTML);
        if(item_price < parseFloat(left_val) || item_price > parseFloat(right_val)) hide(items[i]);
        else show(items[i]);
    }
    return;
}

function setLeftValue() {
	const _this = slider_left;
	const	min = parseFloat(_this.min);
	const	max = parseFloat(_this.max);
	_this.value = Math.min(parseFloat(_this.value), parseFloat(slider_right.value) - 1);
	const percent = ((_this.value - min) / (max - min)) * 100;
	thumb_left.style.left = percent + "%";
	range.style.left = percent + "%";
    thumb_info_left.innerHTML = "£" + _this.value;
    left_val = _this.value;
    filter_items();
}
setLeftValue();

function setRightValue() {
	const _this = slider_right;
	const	min = parseFloat(_this.min);
	const	max = parseFloat(_this.max);
	_this.value = Math.max(parseFloat(_this.value), parseFloat(slider_left.value) + 1);
	const percent = ((_this.value - min) / (max - min)) * 100;
	thumb_right.style.right = (100 - percent) + "%";
	range.style.right = (100 - percent) + "%";
    thumb_info_right.innerHTML = "£" + _this.value;
    right_val = _this.value;
    filter_items();
}
setRightValue();

slider_left.addEventListener("input", setLeftValue);
slider_right.addEventListener("input", setRightValue);

slider_left.addEventListener("mouseover", function() {
	thumb_left.classList.add("hover");
});
slider_left.addEventListener("mouseout", function() {
	thumb_left.classList.remove("hover");
});
slider_left.addEventListener("mousedown", function() {
	thumb_left.classList.add("active");
});
slider_left.addEventListener("mouseup", function() {
	thumb_left.classList.remove("active");
});

slider_right.addEventListener("mouseover", function() {
	thumb_right.classList.add("hover");
});
slider_right.addEventListener("mouseout", function() {
	thumb_right.classList.remove("hover");
});
slider_right.addEventListener("mousedown", function() {
	thumb_right.classList.add("active");
});
slider_right.addEventListener("mouseup", function() {
	thumb_right.classList.remove("active");
});

