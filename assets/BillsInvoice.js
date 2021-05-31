// mySideBar
$('.sidebtn').on('click',function(){
  $('.sidebar').toggleClass("showSidebar");
  // $('.main').toggleClass("withOpacity");
});
$('.main').on('click',function(){
  $('.sidebar').removeClass("showSidebar");
  // $('.main').removeClass("withOpacity");
});

var setText = $('.breadcrumb .active');
setText.text('Subscriptions');

var initText = $('.breadcrumb-item .active').text();

$('#SubscriptionsTab').on('click', function () {
  setText.text($(this).text());
});
$('#GroceryTab').on('click', function () {
  setText.text($(this).text());
});
$('#ProductsTab').on('click', function () {
  setText.text($(this).text());
});
