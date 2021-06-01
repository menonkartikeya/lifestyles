// mySideBar
$('.sidebtn').on('click', function () {
  $('.sidebar').toggleClass("showSidebar");
  // $('.main').toggleClass("withOpacity");
});
$('.main').on('click', function () {
  $('.sidebar').removeClass("showSidebar");
  // $('.main').removeClass("withOpacity");
});


let r1 = document.getElementById('met')
let r2 = document.getElementById('imp')
let d1 = document.getElementById('metdiv');
let d2 = document.getElementById('impdiv');
let y1 = document.getElementById('fabio')
d2.classList.add('d-none')
r1.addEventListener('click', function() {
    y1.textContent = 'BMI-Metric'
    d1.classList.remove('d-none')

    d2.classList.add('d-none')

})
r2.addEventListener('click', function() {
    y1.textContent = 'BMI-Imperial'
    d1.classList.add('d-none');
    d2.classList.remove('d-none')
})
