'use strict';
let scrollBtn = document.querySelector("#topBtn");

window.onscroll= function() {scrollTopFunction()}; 

function scrollTopFunction() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        scrollBtn.style.display = "block";
    }
    else {
        scrollBtn.style.display = "none";
    }
};

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
};