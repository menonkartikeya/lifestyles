// mySideBar
$('.sidebtn').on('click',function(){
  $('.sidebar').toggleClass("showSidebar");
  // $('.main').toggleClass("withOpacity");
});
$('.main').on('click',function(){
  $('.sidebar').removeClass("showSidebar");
  // $('.main').removeClass("withOpacity");
});

// $("#debugDiv").hide();
// document.getElementById("debugDiv") {
//   $('#debugDiv').show();
//   // $('#debugDiv').html('<p>' + message + '</p>');
//   setTimeout(function() {$("#debugDiv").hide();}, 18000);
// };
// console.error = console.debug = console.info =  console.log;



var setText = $('.breadcrumb .active');
setText.text('My Profile');

var initText = $('.breadcrumb-item .active').text();

$('#myProfileTab').on('click', function () {
  setText.text($(this).text());
});
$('#perInfoTab').on('click', function () {
  setText.text($(this).text());
});
$('#passwordTab').on('click', function () {
  setText.text($(this).text());
});


function changetextbox()
{
    if (document.getElementById("diet").value === "no") {
        document.getElementById("inputReason1").disabled='true';
    } else {
        document.getElementById("inputReason1").disabled='';
    }

    if (document.getElementById("traine").value === "no") {
        document.getElementById("inputReason2").disabled='true';
    } else {
        document.getElementById("inputReason2").disabled='';
    }

    if (document.getElementById("nutri").value === "no") {
        document.getElementById("inputReason3").disabled='true';
    } else {
        document.getElementById("inputReason3").disabled='';
    }
}
