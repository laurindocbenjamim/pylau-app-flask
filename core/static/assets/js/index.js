
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var navScroller = document.querySelector(".nav-scroller");
  var navItem = document.querySelectorAll(".nav-item");

  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    navScroller.classList.add("fixed-nav");
    navScroller.classList.add("black-bg");
    navItem.classList.add("white-text");
  } else {
    navScroller.classList.remove("fixed-nav");
    navScroller.classList.remove("black-bg");
    navItem.classList.remove("white-text");
  }
}