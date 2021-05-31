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
let q3 = document.getElementById('post');
let q4 = document.getElementById('pre');
let q5 = document.getElementById('Dinner');
let q6 = document.getElementById('breakfast');
q1.addEventListener('click', function(event) {
    q2.textContent = event.target.value
})
q3.addEventListener('click', function(event) {
    q2.textContent = event.target.value
})
q4.addEventListener('click', function(event) {
    q2.textContent = event.target.value
})
q5.addEventListener('click', function(event) {
    q2.textContent = event.target.value
})
q6.addEventListener('click', function(event) {
    q2.textContent = event.target.value
})