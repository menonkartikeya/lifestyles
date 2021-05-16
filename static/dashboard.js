const labels = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
];
data = {
    labels: labels,
    datasets: [{
        label: 'My First dataset',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 20, 5, 2, 20, 30, 45],
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