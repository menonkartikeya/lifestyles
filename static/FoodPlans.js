// mySideBar
$('.sidebtn').on('click', function () {
	$('.sidebar').toggleClass("showSidebar");
	// $('.main').toggleClass("withOpacity");
});
$('.main').on('click', function () {
	$('.sidebar').removeClass("showSidebar");
	// $('.main').removeClass("withOpacity");
});





// $('.datepicker').datepicker();









// Open the full screen search box
function openSearch() {
  document.getElementById("myOverlay").style.display = "block";
}

// Close the full screen search box
function closeSearch() {
  document.getElementById("myOverlay").style.display = "none";
}

// Open the full screen search box
function openSearch3() {
  document.getElementById("myOverlay3").style.display = "block";
}

// Close the full screen search box
function closeSearch3() {
  document.getElementById("myOverlay3").style.display = "none";
}
function openSearch4() {
  document.getElementById("myOverlay4").style.display = "block";
}

// Close the full screen search box
function closeSearch4() {
  document.getElementById("myOverlay4").style.display = "none";
}
function openSearch5() {
  document.getElementById("myOverlay5").style.display = "block";
}

// Close the full screen search box
function closeSearch5() {
  document.getElementById("myOverlay5").style.display = "none";
}
function openSearch6() {
  document.getElementById("myOverlay6").style.display = "block";
}

// Close the full screen search box
function closeSearch6() {
  document.getElementById("myOverlay6").style.display = "none";
}

// Open the full screen search box
function openCal() {
  document.getElementById("myOverlay2").style.display = "block";
}

// Close the full screen search box
function closeCal() {
  document.getElementById("myOverlay2").style.display = "none";
}


function showCal(){
	$('#myCalendarWrapper').toggleClass("showOrNot");
}


const nextYear = new Date().getFullYear() + 1;
const myCalender = new CalendarPicker('#myCalendarWrapper', {
      min: new Date(),
      max: new Date(nextYear, 10)
});
