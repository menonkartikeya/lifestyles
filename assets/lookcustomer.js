// mySideBar
$('.sidebtn').on('click', function () {
  $('.sidebar').toggleClass("showSidebar");
  // $('.main').toggleClass("withOpacity");
});
$('.main').on('click', function () {
  $('.sidebar').removeClass("showSidebar");
  // $('.main').removeClass("withOpacity");
});
