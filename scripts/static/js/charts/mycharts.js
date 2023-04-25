var commonUtil = {
  /**
   * 弹出消息框
   * @param msg 消息内容
   * @param type 消息框类型（参考bootstrap的alert）
   */
  alert: function(msg, type){
      if(typeof(type) =="undefined") { // 未传入type则默认为success类型的消息框
          type = "success";
      }
      // 创建bootstrap的alert元素
      var divElement = $("<div></div>").addClass('alert').addClass('alert-'+type).addClass('alert-dismissible').addClass('col-md-4').addClass('col-md-offset-4');
      divElement.css({ // 消息框的定位样式
          "position": "absolute",
          "top": "80px"
      });
      divElement.text(msg); // 设置消息框的内容
      // 消息框添加可以关闭按钮
      var closeBtn = $('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>');
      $(divElement).append(closeBtn);
      // 消息框放入到页面中
      $('body').append(divElement);
      return divElement;
  },
  
  /**
   * 短暂显示后上浮消失的消息框
   * @param msg 消息内容
   * @param type 消息框类型
   */
  message: function(msg, type) {
      var divElement = commonUtil.alert(msg, type); // 生成Alert消息框
      var isIn = false; // 鼠标是否在消息框中
      
      divElement.on({ // 在setTimeout执行之前先判定鼠标是否在消息框中
          mouseover : function(){isIn = true;},
          mouseout  : function(){isIn = false;}
      });

      // 短暂延时后上浮消失
      setTimeout(function() {
          var IntervalMS = 20; // 每次上浮的间隔毫秒
          var floatSpace = 60; // 上浮的空间(px)
          var nowTop = divElement.offset().top; // 获取元素当前的top值
          var stopTop = nowTop - floatSpace;    // 上浮停止时的top值
          divElement.fadeOut(IntervalMS * floatSpace); // 设置元素淡出
          
          var upFloat = setInterval(function(){ // 开始上浮
              if (nowTop >= stopTop) { // 判断当前消息框top是否还在可上升的范围内
                  divElement.css({"top": nowTop--}); // 消息框的top上升1px
              } else {
                  clearInterval(upFloat); // 关闭上浮
                  divElement.remove();    // 移除元素
              }
          }, IntervalMS);

          if (isIn) { // 如果鼠标在setTimeout之前已经放在的消息框中，则停止上浮
              clearInterval(upFloat);
              divElement.stop();
          }
          
          divElement.hover(function() { // 鼠标悬浮时停止上浮和淡出效果，过后恢复
              clearInterval(upFloat);
              divElement.stop();
          },function() {
              divElement.fadeOut(IntervalMS * (nowTop - stopTop)); // 这里设置元素淡出的时间应该为：间隔毫秒*剩余可以上浮空间
              upFloat = setInterval(function(){ // 继续上浮
                  if (nowTop >= stopTop) {
                      divElement.css({"top": nowTop--});
                  } else {
                      clearInterval(upFloat); // 关闭上浮
                      divElement.remove();    // 移除元素
                  }
              }, IntervalMS);
          });
      }, 1500);
  }
}





$(function(){


    $("#layout").hide();

    $('#datetimepicker6').datetimepicker();
    $('#datetimepicker7').datetimepicker();
    $("#datetimepicker6").on("dp.change",function (e) {
    $('#datetimepicker7').data("DateTimePicker").minDate(e.date);
    });
     $("#datetimepicker7").on("dp.change",function (e) {
     $('#datetimepicker6').data("DateTimePicker").maxDate(e.date);
    });





    var ro = new ResizeObserver( entries => {
        for (let entry of entries) {
          const cr = entry.contentRect;
        // console.log('Element:', entry.target);
        //   console.log(`Element size: ${cr.width}px x ${cr.height}px`);
        //   console.log(`Element padding: ${cr.top}px ; ${cr.left}px`);

        var myChart = echarts.init(entry.target);
        myChart.resize();


        }
      });
    


    
    
        ro.observe(main);
        ro.observe(normalchart);
        ro.observe(chartdiv2);
        





      // default value ..
        var item_select = $("#chart_itemselect").find('option:selected').text();
        
        $.get("/api/v0.1/bigdata/Get_cpkchart",{test_item:item_select},function(resp){
          if (resp.errno == "0" ){
            cpkchart(resp.data.pn_list,resp.data.sum_data,resp.data.date_list,item_select) 
          }

        })


        $("#chart_itemselect").change(function(){

          var item_select = $("#chart_itemselect").find('option:selected').text();
          $.get("/api/v0.1/bigdata/Get_cpkchart",{test_item:item_select},function(resp){
            if (resp.errno == "0" ){
              cpkchart(resp.data.pn_list,resp.data.sum_data,resp.data.date_list,item_select) 
            }
  
          })


        })








        default_chart()






        
        
        $.get("/api/v0.1/bigdata/Get_barchart",function(resp){

            if (resp.errno == "0"){
                fabochartcall(resp.data.chart_items)
                console.log(resp.data.today_qty)
                $("#chart_qty").html(resp.data.today_qty)
            }
        })


        //Get group 
        $.get("/api/v0.1/bigdata/Get_group_names",function(resp) {
            if (resp.errno == "0"){
             $("#myAlert").hide();
            //Echartsdisplay()
            for (var i=0;i<resp.data.group_items.length;i++) {
                   document.getElementById("itemselectgp").options.add(new Option(resp.data.group_items[i][1],resp.data.group_items[i][0]));
            }
            }else {

              commonUtil.message("Get Workcell item Failed from SQL server !","danger")

    
            }
    
        },"json");





        // refresh datatime 


        var startDate = new Date();
        var endDate = new Date();
        endDate.setSeconds(startDate.getSeconds() + 280);


        CountDown.openTimeCountByStartAndEndDate({
            Ele: document.getElementById('refresh_datatime'),
            StartDate: startDate,
            EndDate: endDate,
            Sign: 'flypie',
            Divider: ':',
            EndFunc: function () {
                console.log('end');
            },
            additionToggle: {
                seconds: 1,
                callback: function () {
                    
                  
                    location.href = "/"

                }
            }
        });


        var e_button = document.getElementById('stop_btn');
        e_button.addEventListener('click', function () {

          $("#stop_btn em").addClass("red");
          $("#resume_btn em").removeClass("red");


            CountDown.stopBySign('flypie');
        });

        var e_button2 = document.getElementById('resume_btn');
        e_button2.addEventListener('click', function () {

            $("#resume_btn em").addClass("red");
            $("#stop_btn em").removeClass("red");

            CountDown.resumeBySign('flypie');
        });



        $("#itemselectgp").change(function(){
            $("#itemselectwc").empty();
            $("#itemselecttester").empty();
            $("#itemselectpn").find("option:selected").text("");
            $("#itemselectpn").empty();
            $("#itemselect").find("option:selected").text("");
            $("#itemselect").empty();

            var group_name = $("#itemselectgp").find('option:selected').text();

            if (group_name.length >2){

            var parames = {
                'group_name': group_name
             }

            $.get("/api/v0.1/bigdata/Get_workcell",parames,function(resp){

                $("#itemselectwc").append("<option value= 0 ></option>");
                if (resp.errno == 0){
                    for (var i=0;i<resp.data.wc_items.length;i++) {
                    $("#itemselectwc").append("<option value = '"+resp.data.wc_items[i][1] +"'>" + resp.data.wc_items[i][0] +"</option>")

                    }


                    // add change event -- wc

                    $("#itemselectpn").find("option:selected").text("");
                    $("#itemselectpn").empty();

                    $("#itemselectwc").change(function(){

                        var wc_id = $("#itemselectwc").find('option:selected').val();

                        $.get("/api/v0.1/bigdata/Get_bigdata_pn_items",{'wc_id':wc_id},function(resp){

                            
                            if (resp.errno == '0'){
                            
                            $("#itemselectpn").append("<option value= 0 ></option>");
                            for (var i=0;i<resp.data.pn_items.length;i++) {
                                $("#itemselectpn").append("<option value = '"+ i +"'>" + resp.data.pn_items[i] +"</option>")
            
                                }

                            }


                        // add change event -- tester
                        

                        $("#itemselectpn").change(function(){

                            $("#itemselecttester").empty();
                            
                            $("#itemselect").empty();
                            

                       
                        
                        
                        
                        $.get("/api/v0.1/bigdata/Query_testers",{'wc_id': $("#itemselectwc").find('option:selected').val(),'pn':$("#itemselectpn").find('option:selected').text()},function(resp){


                            if (resp.errno == '0'){
                            $("#itemselecttester").append("<option value = 0 selected >ALL</option>")

                            for (var i=0;i<resp.data.tester_items.length;i++) {
                                $("#itemselecttester").append("<option value = '"+ i+1 +"'>" + resp.data.tester_items[i] +"</option>")
            
                                } 


                            // add change event -- 

                            $.get("/api/v0.1/bigdata/get_test_items",{"group_name":$("#itemselectgp").find('option:selected').text(),"wc_name":$("#itemselectwc").find('option:selected').text(),"pn":$("#itemselectpn").find('option:selected').text()},function(resp){


                                $("#itemselect").append("<option value= 0 ></option>");
    
                                for (var i = 0;i<resp.data.test_items.length;i++){
    
                                    $("#itemselect").append("<option value = '"+ i+1 +"'>" + resp.data.test_items[i] +"</option>")
    
                                }    
    
                            })


                            }

                        })
                    })

                        })
                    })

                } 

            })


            }

        })


})





function chart_update() {
    //加载动画gif


var group_name = $("#itemselectgp").find('option:selected').text();
var item_value_wc = $("#itemselectwc").find('option:selected').text();
var wc_id = $("#itemselectwc").find('option:selected').val();
var item_value_pn = $("#itemselectpn").find('option:selected').text();
var start_time = $("#inputstarttime").val();
var end_time = $("#inputendtime").val();
var tester = $("#itemselecttester").find('option:selected').text();
var item_value = $("#itemselect").find('option:selected').text(); 

params ={
    group_name:group_name,
    workcell:item_value_wc,
    wc_id:wc_id,
    part_num:item_value_pn,
    tester:tester,
    defalut:"NO",
    starttime:start_time,
    endtime:end_time,
    testitem:item_value
}
$.ajax({
    url: "/api/v0.1/bigdata/Get_test_data",
    type: "GET",
    data: params,
    success: function (resp) {
        if ("4103" == resp.errno || "4002" == resp.errno ) {

            commonUtil.message(resp.errmsg,"danger")
            $("#main").hide();
        }

        if ("0" == resp.errno) {
              $("#myAlert").hide();
              $("#main").fadeIn();
              var testdata = resp.data.test_data
              var testlimit= resp.data.test_limit
              var timelist = resp.data.time_list
              var test_item_name = resp.data.test_item_name
              var test_out_limit_list = resp.data.out_limit_list
              Echartsdisplay(testdata,testlimit,timelist,test_item_name,test_out_limit_list)
        }

    }
});

}


function default_chart(){

    let params ={
        group_name:"IMED",
        workcell:"Medtronic",
        wc_id:"83",
        part_num:"MD7006076-008-A-R",
        tester:"ALL",
        defalut:"YES",
        starttime:"03-07-2023 00:12:00",
        endtime:"03-11-2023 00:12:00",
        testitem:"p1_dist"
    }
    $.ajax({
        url: "/api/v0.1/bigdata/Get_test_data",
        type: "GET",
        data: params,
        success: function (resp) {
            if ("4103" == resp.errno || "4002" == resp.errno ) {
               
                $("#main").hide();
            }

            if ("0" == resp.errno) {
                $("#myAlert").hide();
                $("#main").fadeIn();
                var testdata = resp.data.test_data
                var testlimit= resp.data.test_limit
                var timelist = resp.data.time_list
                var test_item_name = resp.data.test_item_name
                var test_out_limit_list = resp.data.out_limit_list
                var test_value_list = resp.data.test_value_list
                var cpk_value = resp.data.cpk
                Echartsdisplay(testdata,testlimit,timelist,test_item_name,test_out_limit_list)
                normalcharts(test_value_list,testlimit,cpk_value)
            }

        }
    });
}

function Echartsdisplay(Test_data,Test_limit_list,Time_list,Test_item_name,Test_out_limit_list) {
    var dom = document.getElementById("main");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;
    option = {
        color: [ '#19ccdb'],
       
        title: {
            textStyle: {
            color:'#19ccdb'
            },
            subtextStyle: {
              fontSize: 10
            },
            text: 'DIMM Total Tested Qty:['+ Test_out_limit_list[0] +'] L-out Qty: ['+ Test_out_limit_list[1] +'] H-out Qty: [' + Test_out_limit_list[2] + ']',
            subtext: 'From: ([' + Test_item_name + '] [LSL:' + Test_limit_list[0] + '--USL:'+ Test_limit_list[1] + '])'
        },
        grid: {
            left: '2%',
            right: '2%',
            bottom: '3%',
            containLabel: true
        },
       
        tooltip: {
            // trigger: 'axis',
            showDelay: 0,
            formatter: function (params) {
                if (params.value.length > 1) {
                    return params.seriesName + '-> Test Date :' + params.value[0] + '<br/>'
                    + 'Test Value: ' + params.value[1] + ' SN:' + params.value[2];
                }
                else {
                    return params.name + ' : '
                    + params.value + ' ';
                }
            },
            axisPointer: {
                show: true,
                type: 'cross',
                lineStyle: {
                    type: 'dashed',
                    width: 1
                }
            }
        },
        toolbox: {
            feature: {
                dataZoom: {},
                saveAsImage: {},
                brush: {
                    type: ['rect', 'polygon', 'clear']
                }
            }
        },
        brush: {
        },
        legend: {
            data: ['DIMM'],
            left: 'center'
        },
        xAxis: [
            {
                type: 'time',
                scale: true,
                axisLabel: {
                    formatter: function (value) {//在这里写你需要的时间格式
                      var t_date = new Date(value);
                      return [t_date.getFullYear(), t_date.getMonth() + 1, t_date.getDate()].join('-') + " "
                      + [t_date.getHours(), t_date.getMinutes()].join(':');
                }
                },
                splitNumber : 7,
                splitLine: {
                    show: false
                },
                min:Time_list[0],
                max:Time_list[1],
            }

        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                axisLabel: {
                    formatter: '{value}'
                },
                splitNumber : 7,
                splitLine: {
                    show: false
                },
                min:function (value) {
                if (value.min < Test_limit_list[0] )
                {
                    if  (value.min < 1 ){
                        if (value.min<0.1){
                        return 0
                        }
                    else{ return value.min - 0.01 }
                    }
                else{ return value.min - 0.02 }
                }
                else{
                    if (Test_limit_list[0]<1){
                        if (Test_limit_list[0]<0.1){
                        return 0
                        }else{
                        return Test_limit_list[0] - 0.01}
                        }
                    else{
                     return Test_limit_list[0] - 0.02 }
                    }
                },

                max: function (value) {
                if (value.max > Test_limit_list[1])
                { return value.max

                }
                else{
                    return Test_limit_list[1] + 0.01
                    }

                    }
            }
        ],
        series: [
            {
                name: 'DIMM',
                type: 'scatter',
                data: Test_data,
                inRange: {
                    colorLightness: Test_limit_list
                  },
                  outOfRange: {
                    color: ['rgba(255,255,255,0.4)']
                  },
                  controller: {
                    inRange: {
                      color: ['#c23531']
                    },
                    outOfRange: {
                      color: ['#999']
                    }
                },
                markArea: {
                    silent: true,
                    itemStyle: {
                        color: 'transparent',
                        borderWidth: 1,
                        borderType: 'dashed'
                    },
                    data: [[{
                        name: 'Test distribution interval' ,
                        xAxis: 'min',
                        yAxis: 'min'
                    }, {
                        xAxis: 'max',
                        yAxis: 'max'
                    }]]
                },
                markPoint: {
                    data: [
                        {type: 'max', name: 'Max value',
                        symbol: "pin",
                        symbolSize: 60,
                        animation: true,
                        label: {
                          show: true,
                          color: '#230'
                    },
                    
                        itemStyle: { color: '#FF1493'}
                      },
                    
                    
                      {type: 'min', name: 'Min value',
                      symbol: "pin",
                        symbolSize: 60,
                        animation: true,
                        label: {
                          show: true,
                          color: '#230'
                    },
                    
                        itemStyle: { color: '#7B68EE' }
                    
                    
                    },



                    ],


                },

                markLine: {
                    label:{
                    show:true
                    },
                    symbol:"none",
                    lineStyle: {
                        color: '#3398db',
                        type: 'solid'
                    },
                    data: [
                        {type: 'average', name: '平均值'},
                        {yAxis:Test_limit_list[0],name:'LSL'},
                        {yAxis:Test_limit_list[1],name:'USL'},
                    ]
                }



            }
        ]
    };
    ;
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
        }



function fabochartcall(vallist) {

        // console.log(vallist)
		data = vallist

		$("#chart2").faBoChart({
		  time: 2500,
		  animate: true,
		  data: data,
		  straight: true,
		  labelTextColor : "#002561",
		});
	}



function normalcharts(test_value_list,testlimit,cpk_value){


  var dom = document.getElementById("normalchart");
  var myChart = echarts.init(dom, null, {
    renderer: "canvas",
    useDirtyRect: false
  });
  var app = {};
  
  //正态分布计算
  function func(x, u, a) {
    return (
      (1 / Math.sqrt(2 * Math.PI)) *
      a *
      Math.exp((-1 * ((x - u) * (x - u))) / (2 * a * a))
    );
  }
  
  var data = test_value_list
  
  // [
  //   0.542883,0.541334,0.541087,0.542801,0.540751,0.541046,0.541309,0.541326,0.542259,0.542081,0.540658,0.541932,0.540264,0.541136,0.541834,0.541806,0.54191,0.541162,0.541588","0.54171","0.541944","0.54249","0.541608","0.542637","0.542628",
  //   "0.541736","0.542044","0.541634","0.541134","0.541331","0.542692","0.542678","0.541077","0.542479","0.541207","0.541357","0.542993","0.540908","0.54237","0.542457","0.541858","0.540906","0.54146","0.54254","0.541301","0.541388","0.541912","0.540631","0.540638","0.542972",
  //   "0.543154","0.541233","0.54123","0.540909","0.540939","0.542727","0.541439","0.541614","0.541203","0.541626","0.541992","0.541581","0.541359","0.54154","0.54091","0.54167","0.540783","0.540965","0.541084","0.540914","0.540771","0.542147","0.542002","0.542324","0.541054",
  //   "0.542164","0.541391","0.54105","0.542225","0.541618","0.541854","0.541794","0.542989","0.542233","0.542063","0.541452","0.541856","0.541981","0.541694","0.541974","0.542118"
  // ];
  var xMin = testlimit[0]; //LowLimit
  var xMax = testlimit[1]; //UpLimit
  var mean = math.mean(data); //平均值  计算方法来自math.js
  var stdev = math.std(data); //方差
  var threeSigUp = mean + 3 * stdev;
  var threeSigLow = mean - 3 * stdev;
  //数据升序排序
  const dataSec = data.sort((a, b) => {
    return a - b;
  });
  //计算频数
  


  // console.log('datasec is:',dataSec)
  var resNum = {};
  for (var m = 0; m < dataSec.length; m++) {
    var key = parseFloat(dataSec[m]);
    if (parseFloat(key) === 0) continue;
  
    // console.log('resnum is:',resNum[key])
    if (resNum[key]) resNum[key] = key;
    else resNum[key] =key ;
  }

  var xArr = []; //横坐标值
  var fArr = []; //频数
  var yArr = []; //正态值
  
  for (var k in resNum) {
    xArr.push(parseFloat(k));
  }
  xArr = xArr.sort((a, b) => {
    return a - b;
  });
  //console.log(xArr);
  
  //计算x值对应的频数
  for (var i = 0; i < xArr.length; i++) {
    var xNy = [xArr[i], resNum[xArr[i]]];
    fArr.push(xNy);
  }
  
  //计算x值对应的正态分布值
  var distance = xMax - xMin; //为了更好看，设置正态曲线起止位置
  for (var j = xMin + distance / 40; j < xMax - distance / 40; j += 0.0005) {
  
      // console.log('j is:',j)
  
      // console.log('mean is:',mean)
    
      // console.log('stdev is:',stdev)
  
    var xy = [j, func(j, mean, stdev)];
    yArr.push(xy);
  }
  
  // console.log('yArr is:',yArr)
  var option;
  option = {
    //backgroundColor: "#12141e",


        graphic: [{
          type: 'text',
          left: '40%',
          top: '30px',
          draggable: true,
          style: {
              text: 'CPK:'+ cpk_value,
              fill: 'blue',
              fontSize: 16
          }
      }],

    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow"
      }
    },
    legend: {
      orient: "vertical",
      x: "right",
      y: "top",
      top: "20px",
      data: ["Frequency", "Normal distribution"],
      textStyle: {
        color: "rgba(255,255,255,1)",
        fontSize: "12"
      }
    },
    grid: {
      left: "2%",
      top: "18px",
      right: "2%",
      bottom: "2%",
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },

    xAxis: [
      {
        type: "value",
        min: xMin,
        max: xMax,
        axisLabel: {
          textStyle: {
            color: "rgba(255,255,255,1)",
            fontSize: 10
          }
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: "rgba(255,255,255,1)"
          }
        },
        splitLine: {
          show: false
        }
      }
    ],
    yAxis: [
      {
        type: "value", //数值轴
        name: "Normal Curve",
        position: "right",
        axisTick: { show: true },
        axisLine: {
          show: false,
          lineStyle: {
            color: "rgba(255,255,255,1)"
          }
        },
        axisLabel: {
          show: true,
          textStyle: {
            color: "rgba(255,255,255,1)",
            fontSize: 10
          }
        },
        splitLine: {
          show: false
        }
      },
      {
        type: "value",
        name: "Frequency",
        type: "value",
        min: 0,
        max: xMax + 0.2,
        position: "left",
        axisLabel: {
          //formatter: '{value} %'
          show: true,
          textStyle: {
            color: "rgba(255,255,255,1)",
            fontSize: "12"
          }
        },
        axisTick: {
          show: true
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: "rgba(0,0,0,.1)",
            width: 1,
            type: "solid"
          }
        },
        splitLine: {
          lineStyle: {
            color: "rgba(255,255,255,.3)"
          }
        }
      }
    ],
    series: [
      {
        name: "Normal distribution",
        type: "line",
        smooth: true,
        yAxisIndex: 0,
        symbol: "circle",
        symbolSize: 5,
        showSymbol: false,
        lineStyle: {
          
          normal: {
            color: "#ceb664",
            width: 6
          }
        },
  
        itemStyle: {
          normal: {
            color: "#ceb664",
            borderColor: "rgba(221, 220, 107, .1)",
            borderWidth: 5
          }
        },
        data: yArr,
        markLine: {
          symbol: ["none"],
          lineStyle: {
            type: "dotted",
            color: "pink",
            width: 5
          },
          itemStyle: {
            normal: {
              show: true,
              color: "black"
            }
          },
          label: {
            show: true,
            position: "end"
          },
          data: [
            {
              name: "3σ",
              xAxis: threeSigLow.toFixed(6),
              label: {
                show: true,
                formatter: "3σ"
              }
            },
            {
              name: "3σ",
              xAxis: threeSigUp.toFixed(6),
              label: {
                show: true,
                formatter: "3σ"
              }
            }
          ]
        }
      },
      {
        name: "Frequency",
        type: "bar",
        yAxisIndex: 1,
        xAxisIndex: 0,
        barWidth: 8,
        barGap: 1,
        symbol: "solid",
        symbolSize: 5,
        showSymbol: true,
        itemStyle: {
          normal: {
            color: "#0184d5",
            opacity: 1,
            barBorderRadius: 3
          }
        },
        data: fArr,
        markLine: {
          symbol: ["none"],
          lineStyle: {
            type: "dotted",
            color: "red"
          },
          itemStyle: {
            normal: {
              show: true,
              color: "black"
            }
          },
          label: {
            show: true,
            position: "middle"
          },
          data: [
            {
              name: "LowLimit",
              xAxis: xMin.toFixed(6),
              label: {
                show: true,
                formatter: "Low"
              }
            },
            {
              name: "High",
              xAxis: xMax.toFixed(6),
              label: {
                show: true,
                formatter: "High"
              }
            }
          ]
        }
      }
    ]
  };
  
  if (option && typeof option === "object") {
    myChart.setOption(option);
  }
  
  window.addEventListener("resize", myChart.resize);





}



function cpkchart(pn_list,sum_data,date_list,item_select){

  // chartdiv2

  var chartDom = document.getElementById('chartdiv2');
  var myChart = echarts.init(chartDom);
  var option;
  
  option = {
    title: {
      text: 'DIMM '+ item_select
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c}'
    },
    legend: {
      data: pn_list
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: date_list,
      

    },
    yAxis: {
      
      min:0,
      max:6,
      type: 'value'
    },
    series: [
      {
        name: sum_data[0][0],
        type: 'line',
        // stack: 'Total', //delete it ,align the vlaue with scale
        data: sum_data[0][1]
      },
      {
        name: sum_data[1][0],
        type: 'line',
       
        data: sum_data[1][1],
        z: 2 // 设置 z-index 为 2
      },
      {
        name: sum_data[2][0],
        type: 'line',
        data: sum_data[2][1],
        z: 1 // 设置 z-index 为 2
      }
    ]
  };
  
  option && myChart.setOption(option);


}




function exportreport() {
  $("#layout").fadeIn(); 
  var wc_g = $("#itemselectgp").find('option:selected').text();
  var wc_name = $("#itemselectwc").find('option:selected').text();
  var pn = $("#itemselectpn").find('option:selected').text();
  var tester = $("#itemselecttester").find('option:selected').text();
  var start_time = $("#inputstarttime").val()
  var end_time = $("#inputendtime").val()

  // console.log(value_check([wc_g,wc_name,pn,tester,start_time,end_time]))
  if (!value_check([wc_g,wc_name,pn,tester,start_time,end_time])){
    commonUtil.message("Pramas error ,please select all of the pramas !","danger")
    return false

  }
  $("#download_button").hide();
  params ={
      group_name:wc_g,
      workcell:wc_name,
      part_num:pn,
      tester:tester,
      starttime:start_time,
      endtime:end_time,
      download:'NO',
  }

//    location.href = "/api/v0.1/AMS_Charts/Download_excel?" + "workcell=" + item_value_wc + "&part_num=" + item_value_pn + "&starttime=" + start_time + "&endtime=" + end_time ;
  $("#layout").fadeIn(500); 
  $.ajax({
      url: "/api/v0.1/dimm/Download_excel",
      async: true,
      type: "GET",
      data: params,
      success: function (resp) {

          if (resp.errno == "0") {
              $("#download_button").show();
              commonUtil.message("Get excel ,will download it !","success")
              $("#layout").fadeOut(5); 
              location.href = "/api/v0.1/dimm/Download_excel?group_name="+ wc_g +"&workcell=" + wc_name + "&part_num=" + pn + "&tester="+tester+"&starttime=" + start_time + "&endtime=" + end_time +"&download=YES";
             
          }
          if ("4103" == resp.errno || "4002" == resp.errno ) {
              $("#download_button").show();
              commonUtil.message(resp.errmsg,"danger")
              $("#layout").fadeOut(5); 
              return false
          }
      }
  });
}


function value_check(values){
  values.forEach(element => {
    console.log(element)
    if (typeof(element) == "undefined") return false
    if (element.length <2) return false
  
  });

  return true

}