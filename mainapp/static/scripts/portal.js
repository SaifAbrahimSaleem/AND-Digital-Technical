$(document).ready(function(){

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

    $("#login-form").on('submit', function(event){
      event.preventDefault();
      var data = $(this).serialize();
      data['email'] = $("#login_email").val();
      data['password']= $("#id_password").val();
      $.ajax({
        beforeSend: function(xhr, settings) {
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
              xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
          }
        },
        type:"POST",
        url:"/login/",
        data:data,
        success: function(data){
          if(parseInt(data["redirect"])==0){
              DisplayNotification(data);
          } else{
              window.location = "/";
          }
        }
      });
    });
  
    $("#signup-form").on('submit', function(event){
      event.preventDefault();
      var data = {};
      data['email'] = $("#register_email").val();
      data['username'] = $("#register_username").val();
      data['first_name'] = $("#register_first").val();
      data['last_name'] = $("#register_last").val();
      data['password1'] = $("#register_password").val();
      data['password2'] = $("#register_confirm_password").val();
      $.ajax({
        beforeSend: function(xhr, settings) {
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
        }
        },
        type:"POST",
        url:"/signup/",
        data:data,
        success: function(data){
          if(parseInt(data["redirect"])==0){
              DisplayNotification(data);
          } else{
              window.location = "/portal/";
              DisplayNotification(data);
          }
        }
      });
    });
  });

  function DisplayNotification(data){
    var alert_class = ["alert", "appendable", "notif-alert", "alert", "animate__animated", "animate__bounceIn", "alert-dismissible", "fade", "show"];
    var msg_icon =  ["fa"];
    var msgTitle;
    var msgSubTitle;
    var msg;
    var msg_text;
    var break_after;
    var break_before;
    if(data.hasOwnProperty('code')){
      if(data.code == 0){
        alert_class.push("alert-danger");
        msg_icon.push("fa-times");
        msgTitle = "Warning!"
        msg_icon = $("<i />", { "class": msg_icon.join(" ") });
        msg = $("<div />", { "class": alert_class.join(" ") });
        msgTitle = $("<h4 />", { html: msgTitle }).appendTo(msg);
      } else {
        alert_class.push("alert-success");
        msg_icon.push("fa-check-circle");
        msgTitle = "Success!"
        msg_icon = $("<i />", { "class": msg_icon.join(" ") });
        msg = $("<div />", { "class": alert_class.join(" ") });
        msgTitle = $("<h4 />", { html: msgTitle }).appendTo(msg);
      }
      msgTitle.prepend(msg_icon);
    }
    if(data.hasOwnProperty('form_errors')){
      $.each(data.form_errors,function(key,value){
        switch (key){
            case "__all__":
                msgSubTitle = $("<p />").appendTo(msgTitle);
                msg_text = $("<strong />",  { "class": "d-flex justify-content-center", html: value}).appendTo(msgSubTitle);
                break;
            case "email":
                msg_text = $("<strong />", { html: "- Email: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);
                break;
            case "first_name":
                msg_text = $("<strong />", { html: "- First Name: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);
                break;
            case "last_name":
                msg_text = $("<strong />", { html: "- Last Name: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);
                break;
            case "password1":
                msg_text = $("<strong />", { html: "- Initial Password: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);
                break;
            case "password2":
                msg_text = $("<strong />", { html: "- Password Confirmation: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);
                break;
            case "username":
                msg_text = $("<strong />", { html: "- Username: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);
                break;
            case "password":
                msg_text = $("<strong />", { html: "- Password: " + value}).appendTo(msg);
                break_after = $("<br />").appendTo(msg);

        }
      });
    }
    if(data.hasOwnProperty('response')){
      var break_before = $("<br />").appendTo(msg);
      var msg_text = $("<strong />", { html: data.response}).appendTo(msg);
      var break_after = $("<br />").appendTo(msg);
    }
    var msgClose = $("<span />", { "class": "close", "data-dismiss": "alert", html: "<i class='fa fa-times-circle'></i>" }).appendTo(msg);
    $('.login-notification').prepend(msg);
    setTimeout(function(){
      setTimeout(function(){
        msg.remove();
      },1000);
    }, 5000);
  }