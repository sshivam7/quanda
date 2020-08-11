/*
  Author: Shivam Sood 
  Date: August 6th 2020
  Description: Typing animation to cycle through a set of words or phrases 
*/

// Get the span element form the DOM and create a list of words to cycle through
let wordSpan = document.querySelector(".word-span");
let phraseCounter = 0;
const rotateElements = ["Questions.", "Answers.", "Solutions."];

// cycle through words when window is loaded
window.onload = function () {
  cycleText(phraseCounter);
};

function cycleText(pCounter) {
  // Split the current word into an array of characters and set default values
  letterCount = 0;
  let charArr = rotateElements[pCounter].split("");
  wordSpan.classList.remove("highlight-text");

  // Add characters to the span element one at a time after a semi-random interval
  let typeInterval = setInterval(function () {
    wordSpan.textContent += charArr[letterCount++];

    // Clear interval if all characters in the array have been printed 
    if (letterCount >= charArr.length) {
      clearInterval(typeInterval);
      // Delete current text in span and call the cycleText function again if 
      // there are words remaining in the rotateElements list
      if (pCounter < rotateElements.length - 1) {
        // Add highlight class and wait 1 second before deleting the current word 
        wordSpan.classList.add("highlight-text");
        setTimeout(function () {
          wordSpan.textContent = "";
          cycleText(++phraseCounter);
        }, 1000);
      }
    }
  }, getRandTime());
}

// Get a random time value to vary typing speed
function getRandTime() {
  return 300 - Math.random() * 100;
}
