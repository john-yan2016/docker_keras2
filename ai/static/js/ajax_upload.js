$(function () {
        $("#submit").click(function(){	 
		$("#button_text").html("正在识别");
		$("#pre_result").show();
		$(".result").css("visibility","hidden");
		$(".progress").css("visibility","hidden");
  		$("#loading_img").show();
		x = $("#dataX").val();
        y = $("#dataY").val();
        w = $("#dataWidth").val();
        h = $("#dataHeight").val();
     
         var formData = new FormData($( "#uploadForm" )[0])
		       
         $.ajax({  
              url: '/upload' ,  
              type: 'POST',  
              data: formData, 
			  async: true,  
              cache: false, 
			  contentType: false,  
              processData: false,
              success: function (returndata) {
					//alert(returndata);
					$("#button_text").html("识别完成");
                 	$("#loading_img").hide();
					$(".result").css("visibility","visible");
					p1 = String(parseFloat(returndata.split('|')[1])*100)+"%";
					p2 = String(parseFloat(returndata.split('|')[3])*100)+"%";
					p3 = String(parseFloat(returndata.split('|')[5])*100)+"%";
					$(".progress").css("visibility","visible");
					$("#progress1").css("width",p1);
					$("#progress2").css("width",p2);
					$("#progress3").css("width",p3);
					
                    $("#predict1").text(returndata.split('|')[0]);
					$("#predict11").text(p1);
					$("#predict2").text(returndata.split('|')[2]);
					$("#predict22").text(p2);
					$("#predict3").text(returndata.split('|')[4]);
					$("#predict33").text(p3);
                    

              },  
              error: function (returndata) {  
                  alert("提交失败，请重试！");  
              }  
      }); 

     });
    });
