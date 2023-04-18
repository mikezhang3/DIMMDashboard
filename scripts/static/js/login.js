
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}



//加载动画gif
setTimeout(showMain,"500");
        function showMain()
        {
            document.getElementById("over").style.display = "none";
            document.getElementById("layout").style.display = "none";
        }


$(function(){

    $("#password-err").hide()

    $(".login_cs input").eq(0).focus(function () {
        $("#password-err").hide();
    });


    $(".login_cs").submit(function(e){
        //通过这个方法阴止浏览器对于表单的默认自动提交行为
        e.preventDefault();
        var user_name = $(".login_cs input").eq(0).val()
        var user_passwd = $(".login_cs input").eq(1).val()

        if (user_name == "NT name") {
            $("#password-err span").html(" Please input your NT name！").css({ 'color': 'red' });
            $("#password-err").css({ 'color': 'red' })
            $("#password-err").show();
            return;
        }
        if (user_passwd==="Password" ) {
            $("#password-err span").html(" Please input your password!").css({ 'color': 'red' });
            $("#password-err").css({ 'color': 'red' })
            $("#password-err").show();
            return;
        }
        


           // 将表单的数据存放到对象data中
        var data = {
            mobile: user_name,
            password: user_passwd
        };
        // 将data转为json字符串
        var jsonData = JSON.stringify(data);
        $(".layout").fadeIn(10);
        $.ajax({
            url:"/api/v0.1/sessions",
            type:"POST",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0") {

                    $(".layout").fadeOut(10);
                    // 登录成功，跳转到主页
                    location.href = "/";
                }
                else {
                    // 其他错误信息，在页面中展示
                    alert(resp.errmsg)
                    $("#password-err span").html(resp.errmsg);
                    $("#password-err").show();
                }
            }
        });



    
    })
    
})