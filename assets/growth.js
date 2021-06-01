
// mySideBar
$('.sidebtn').on('click', function () {
  $('.sidebar').toggleClass("showSidebar");
  // $('.main').toggleClass("withOpacity");
});
$('.main').on('click', function () {
  $('.sidebar').removeClass("showSidebar");
  // $('.main').removeClass("withOpacity");
});

var labels = {{ bmidate|safe }};
var bmil = {{ bmilist |safe }};
data = {
    labels: labels,
    datasets: [{
        label: 'BMI Progress Graph',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: bmil,
    }]
};
let config = {
    type: 'line',
    data,
    options: {}
};
var myChart = new Chart(
    document.getElementById('myChart'),
    config
);





var labelss = {{ bmrdate|safe }};
var bmrl = {{ bmrlist |safe }};
data = {
    labels: labelss,
    datasets: [{
        label: 'My Second dataset',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: bmrl,
    }]
};
let config1 = {
    type: 'line',
    data,
    options: {}
};
var myChart = new Chart(
    document.getElementById('myChart1'),
    config1
);
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
