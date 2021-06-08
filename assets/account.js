let f1 = document.getElementById('name');
let f2 = document.getElementById('email');
let f3 = document.getElementById('password');
let f4 = document.getElementById('Height');

let n1 = document.getElementById('next1');
let n2 = document.getElementById('next2');
let n3 = document.getElementById('next3');

let b1 = document.getElementById('back1');
let b2 = document.getElementById('back2');
let b3 = document.getElementById('back3');

n1.addEventListener('click', function() {
    f1.classList.add('d-none');
    f2.classList.remove('d-none');

})
b1.addEventListener('click', function() {
    f2.classList.add('d-none');
    f1.classList.remove('d-none');
})
n2.addEventListener('click', function() {
    f2.classList.add('d-none');
    f3.classList.remove('d-none');
})
b2.addEventListener('click', function() {
    f3.classList.add('d-none');
    f2.classList.remove('d-none');
})
n3.addEventListener('click', function() {
    f4.classList.remove('d-none');
    f3.classList.add('d-none');
})
b3.addEventListener('click', function() {
    f4.classList.add('d-none');
    f3.classList.remove('d-none');
});

let a1 = document.getElementById('fname');
let a2 = document.getElementById('lname');
let a3 = document.getElementById('mail');
let a4 = document.getElementById('phone');
let a5 = document.getElementById('pass');
let a6 = document.getElementById('con');
let a7 = document.getElementById('he');
let a8 = document.getElementById('we');

let p1 = document.getElementById('p1');
let p2 = document.getElementById('p11');
let p3 = document.getElementById('p21');
let p4 = document.getElementById('p22');
let p5 = document.getElementById('p31');
let p6 = document.getElementById('p33');
let p7 = document.getElementById('p41');
let p8 = document.getElementById('p44');

let s = document.getElementById('submit');
let s1 = document.getElementById('pert');


a1.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p1.classList.remove('d-none');
    } else {
        p1.classList.add('d-none');
    }
});
a2.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p11.classList.remove('d-none');
    } else {
        p11.classList.add('d-none');
    }
});
a3.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p21.classList.remove('d-none');
    } else {
        p21.classList.add('d-none');
    }
});
a4.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p22.classList.remove('d-none');
    } else {
        p22.classList.add('d-none');
    }
});
a5.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p31.classList.remove('d-none');
    } else {
        p31.classList.add('d-none');
    }
});
a6.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p33.classList.remove('d-none');
    } else {
        p33.classList.add('d-none');
    }
});
a7.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p41.classList.remove('d-none');
    } else {
        p41.classList.add('d-none');
    }
});
a8.addEventListener('blur', function(event) {
    if (event.target.value === "") {
        p44.classList.remove('d-none');
    } else {
        p44.classList.add('d-none');
    }
});
s.addEventListener('click', function() {
    if (a1.value === '' || a2.value === '' || a3.value === '' || a4.value === '' || a5.value === '' || a6.value === '' || a7.value === '' || a8.value === '') {
        s1.classList.remove('d-none');
    } else {
        s1.classList.add('d-none');
    }
});