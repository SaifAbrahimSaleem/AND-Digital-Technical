$(document).ready(function () {
    function DisplayNotification(data){
        var alert_class = ["alert"]
        if(data.code == 1){
          alert_class.push("alert alert-success animate__animated animate__bounceIn alert-dismissible fade show");
          var msg_icon = $("<i />", { "class": "fa fa-check-circle" });
          var msg = $("<div />", { "class": alert_class.join(" ") });
          var msgTitle = $("<h4 />", { html: "Success!" }).appendTo(msg);
        } else{
          alert_class.push("alert-danger animate__animated animate__bounceIn alert-dismissible fade show justifu-content-center");
          var msg_icon = $("<i />", { "class": "fa ffa fa-exclamation-circle" });
          var msg = $("<div />", { "class": alert_class.join(" ") });
          var msgTitle = $("<h4 />", { html: "Error!"}).appendTo(msg);
        }
        msgTitle.prepend(msg_icon);
        var msg_text = $("<strong />", { "class":"text-center alert-text", html: data.message }).appendTo(msg);
        var msgClose = $("<span />", { "class": "close", "data-dismiss": "alert", html: "<i class='fa fa-times-circle'></i>" }).appendTo(msg);
        $('#notification').prepend(msg);
        setTimeout(function(){
          setTimeout(function(){
            msg.remove();
          },1000);
        }, 5000);
      }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == name + "=") {
                    cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrfmiddlewaretoken =  getCookie("csrftoken")

    $("#submit-contact").on("click", function () {
        var contact_name = $("#id_contact_name").val();
        var contact_email = $("#id_contact_email").val();
        var contact_number = $("#id_contact_number").val();
        var contact_content = $("#id_contact_content").val();
        $.ajax({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken",csrfmiddlewaretoken);
            }
        },
        type: "POST",
        url: "/contact/",
        data: {
            contact_name: contact_name,
            contact_email: contact_email,
            contact_number: contact_number,
            contact_content: contact_content,
        },
        success: function (data) {
            console.log(data)
            DisplayNotification(data);
        },
        });
    });


});
