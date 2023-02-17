'use strict';
let scrollBtn = document.querySelector("#topBtn");

window.onscroll= function() {scrollTopFunction()}; 

function scrollTopFunction() {
    if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
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