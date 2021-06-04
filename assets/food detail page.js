let data = {
    labels: [
        'Fat',
        'Protein',
        'Energy'
    ],
    datasets: [{
        label: 'My First Dataset',
        data: [20, 70, 100],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
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
    document.getElementById('myChart1'),
    config
);