'use strict';
let myInput = document.querySelector("#password");
let letter = document.querySelector("#psw-letter");
let capital = document.querySelector("#psw-capital");
let number = document.querySelector("#psw-number");
let length = document.querySelector("#psw-length");

myInput.onblur = function() {
  document.querySelector("#psw-message").style.display = "none";
};

myInput.onfocus = function() {
  document.querySelector("#psw-message").style.display = "block";
};

myInput.onkeyup = function() {

  let lowerCaseLetters = /[a-z]/g;
  if(myInput.value.match(lowerCaseLetters)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
};

  let upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  };

  let numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  };

  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }
};
