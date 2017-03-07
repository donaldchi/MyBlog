$(function(){
        $("#button").click(function() {
          document.querySelector('.menu__list').classList.toggle('menu__list--animate');
        });
    });

$(function(){
  $("#button").mousemove(function() {
      this.style.background="#000000";
  });
});

$(function(){
  $("#button").mouseleave(function() {
      this.style.background="#2E3F47";
  });
});