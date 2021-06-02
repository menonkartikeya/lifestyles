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





let data = {
    labels: [
        'Burned',
				'To Burn',
    ],

    datasets: [{
        label: 'My First Dataset',
        data: [300, 800],
        backgroundColor: [
            '#66AC36' ,
						'#EEF2EB',
        ],
        hoverOffset: 4
    }]
};
const config = {
    type: 'doughnut',
    data: data,
    options: {
        responsive: false
    }
};
var myChart = new Chart(
    document.getElementById('myChart123'),
    config
);

$('.progress-bar').each(function() {
    var bar = $(this);
    var value = $(this).find('.count');

    bar.prop('Counter', 0).animate({
            Counter: parseFloat(bar.attr('aria-valuenow'))
        },
        {
            duration: 3000,
            easing: 'swing',
            step: function(now) {
                var number = parseFloat(Math.round(now * 100) / 100).toFixed(2);
                bar.css({ 'width': number + '%' });
                value.text(number + '%');
            }
        });
});




// Open the full screen search box
function openSearch() {
  document.getElementById("myOverlay").style.display = "block";
}

// Close the full screen search box
function closeSearch() {
  document.getElementById("myOverlay").style.display = "none";
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
