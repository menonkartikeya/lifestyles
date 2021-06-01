
// mySideBar
$('.sidebtn').on('click', function () {
  $('.sidebar').toggleClass("showSidebar");
  // $('.main').toggleClass("withOpacity");
});
$('.main').on('click', function () {
  $('.sidebar').removeClass("showSidebar");
  // $('.main').removeClass("withOpacity");
});


//let van1 = document.getElementById('bmi');
//let van2 = document.getElementById('bmr');
//let van3 = document.getElementById('bmidiv');
//let van4 = document.getElementById('bmrdiv');
//van4.classList.add('d-none')
//van1.addEventListener('click', function() {
//   van4.classList.add('d-none')
//  van3.classList.remove('d-none')

//});
//van2.addEventListener('click', function() {
//   van3.classList.add('d-none')
// van4.classList.remove('d-none')
//})
