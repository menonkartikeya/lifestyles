// mySideBar
$('.sidebtn').on('click', function () {
	$('.sidebar').toggleClass("showSidebar");
	// $('.main').toggleClass("withOpacity");
});
$('.main').on('click', function () {
	$('.sidebar').removeClass("showSidebar");
	// $('.main').removeClass("withOpacity");
});
$("#debugDiv").hide();
// console.log = function(message) {
//   $('#debugDiv').show();
//   $('#debugDiv').html('<p>' + message + '</p>');
//   setTimeout(function() {$("#debugDiv").hide();}, 6000);
// };
// console.error = console.debug = console.info =  console.log;
//


let q1 = document.getElementById('snack');
let q2 = document.getElementById('head')
let q3 = document.getElementById('postmeal');
let q4 = document.getElementById('premeal');
let q5 = document.getElementById('Dinner');
let q6 = document.getElementById('breakfast');
q1.addEventListener('click', function(event) {
    q2.textContent = event.target.value
    document.getElementById('snacks').style.display = "block";
    document.getElementById('lunch').style.display = "none";
    document.getElementById('pre').style.display = "none";
    document.getElementById('post').style.display = "none";
    document.getElementById('dinner').style.display = "none";
})
q3.addEventListener('click', function(event) {
    q2.textContent = event.target.value
    document.getElementById('snacks').style.display = "none";
    document.getElementById('lunch').style.display = "none";
    document.getElementById('pre').style.display = "none";
    document.getElementById('post').style.display = "block";
    document.getElementById('dinner').style.display = "none";
})
q4.addEventListener('click', function(event) {
    q2.textContent = event.target.value
    document.getElementById('snacks').style.display = "none";
    document.getElementById('lunch').style.display = "none";
    document.getElementById('pre').style.display = "block";
    document.getElementById('post').style.display = "none";
    document.getElementById('dinner').style.display = "none";
})
q5.addEventListener('click', function(event) {
    q2.textContent = event.target.value
    document.getElementById('snacks').style.display = "none";
    document.getElementById('lunch').style.display = "none";
    document.getElementById('pre').style.display = "none";
    document.getElementById('post').style.display = "none";
    document.getElementById('dinner').style.display = "block";
})
q6.addEventListener('click', function(event) {
    q2.textContent = event.target.value
    document.getElementById('snacks').style.display = "none";
    document.getElementById('lunch').style.display = "block";
    document.getElementById('pre').style.display = "none";
    document.getElementById('post').style.display = "none";
    document.getElementById('dinner').style.display = "none";
})