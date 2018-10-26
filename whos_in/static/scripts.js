const socket = io('http://'+window.location.hostname+':5000'); // Host needs to be changed at some point
const logged_in_user = {name: ""};

socket.on('connect', function(){
    console.log("connect");
});
socket.on('disconnect', function(){
    console.log("dicsonnect");
});

socket.on('update', function(data){
    console.log("update");

    if(logged_in_user.name == "")
        return;

    $.each(data, function(index, user) {
        var name_ = user.name;
        if($('#'+name_).length == 0) {
            var myNewElement_  = $("<div></div>", {html: user.name, id: name_});
            myNewElement_.addClass("alert");
            myNewElement_.addClass("d-flex");
            myNewElement_.addClass("justify-content-between");

            if(user.is_in) {
                myNewElement_.addClass("alert-success");
            }
            else {
                myNewElement_.addClass("alert-danger");
            }

            if(name_ == logged_in_user.name) {

                var toggleButton_ = $("<button type=\"button\">Toggle</button>");
                toggleButton_.addClass("btn");
                toggleButton_.addClass("btn-sm");

                if(user.is_in) {
                    toggleButton_.addClass("btn-danger");
                }
                else {
                    toggleButton_.addClass("btn-success");
                }

                toggleButton_.on('click', function() {
                    socket.emit("inout", `{"name": "${logged_in_user.name}", "is_in": ${!user.is_in}}`)
                    user.is_in = !user.is_in;

                    if(user.is_in) {
                        toggleButton_.addClass("btn-danger");
                        toggleButton_.removeClass("btn-success");
                    }
                    else {
                        toggleButton_.addClass("btn-success");
                        toggleButton_.removeClass("btn-danger");
                    }
                });
                myNewElement_.append(toggleButton_);

            }

            $('body').append(myNewElement_);
        }
        else {
            if(user.is_in) {
                $('#'+name_).addClass("alert-success");
                $('#'+name_).removeClass("alert-danger");
            }
            else {
                $('#'+name_).addClass("alert-danger");
                $('#'+name_).removeClass("alert-success");
            }
        }
    });
});

$("#login_button").on("click", function() {
    console.log("logging in");
    socket.emit("login", "{\"name\": \""+ $("#name_input").val() +"\"}");

    logged_in_user.name = $("#name_input").val();

    $("#login_form").remove();
});