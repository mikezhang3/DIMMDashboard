function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

function logoutfunc() {
    $.ajax({
        url: "/api/v0.1/session",
        type: "delete",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if ("0" == resp.errno) {
                location.href = "/index.html";
            }
        }
    });
}






$(function(){

    $(".rt_header").load("right_header.html", function () {
       
        $(".footerload").load("footer.html",function(){})
        $(".sidebarLoad").load("sidebar.html",function(){

            var toggle = true;				
            $(".sidebar-icon").click(function() {     
                
              if (toggle)
              {
                $(".page-container").addClass("sidebar-collapsed").removeClass("sidebar-collapsed-back");
                $("#menu span").css({"position":"absolute"});
              }
              else
              {
                $(".page-container").removeClass("sidebar-collapsed").addClass("sidebar-collapsed-back");
                setTimeout(function() {
                  $("#menu span").css({"position":"relative"});
                }, 400);
              }
                            
                            toggle = !toggle;
                        });


            $.get("/api/v0.1/session",function (resp) {
                if (resp.errno == "0"){
                    $(".name-caret").html(resp.data.name)
                    $(".role_title").html(resp.data.emp_title + " in Company")

                    
                  
                }else {
                  
                    location.href = "/login.html";
                }
                },"json") ;//后面这个json 指定后端返回数据类型，可传可不传







        })


    })




})