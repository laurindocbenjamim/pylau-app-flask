
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var navScroller = document.querySelector(".nav-scroller");

  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    navScroller.classList.add("fixed-nav");
    navScroller.classList.add("black-bg");
  } else {
    navScroller.classList.remove("fixed-nav");
    navScroller.classList.remove("black-bg");

  }
}