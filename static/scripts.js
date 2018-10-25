const socket = io('http://localhost:5000');
const logged_in_user = {name: ""};

socket.on('connect', function(){
    console.log("connect");
});
socket.on('disconnect', function(){
    console.log("dicsonnect");
});

socket.on('update', function(data){
    console.log("update");
    console.log(data);

    if(logged_in_user.name == "")
        return;

    $.each(JSON.parse(data), function(index, user) {
        var name_ = user.name;
        if($('#'+name_).length == 0) {
            var myNewElement_  = $("<div></div>", {html: user.name, id: name_});

            if(user.is_in) {
                myNewElement_.addClass("in");
            }

            if(name_ == logged_in_user.name) {

                var toggleButton_ = $("<button>Toggle</button>");
                toggleButton_.on('click', function() {
                    socket.emit("inout", `{"name": "${logged_in_user.name}", "is_in": ${!user.is_in}}`)
                    user.is_in = !user.is_in;
                });
                myNewElement_.append(toggleButton_);

            }

            $('body').append(myNewElement_);
        }
        else {
            if(user.is_in) {
                $('#'+name_).addClass("in");
            }
            else {
                $('#'+name_).removeClass("in");
            }
        }
    });
});

$("#login_button").on("click", function() {
    console.log("here");
    socket.emit("login", "{\"name\": \""+ $("#name_input").val() +"\"}");

    logged_in_user.name = $("#name_input").val();

    $("#login_form").remove();
});