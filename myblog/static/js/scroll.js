//■page topボタン
$(function(){
var topBtn=$('#pageTop');
topBtn.hide();
 
//◇ボタンの表示設定
$(window).scroll(function(){
  if($(this).scrollTop()>80){
    //---- 画面を80pxスクロールしたら、ボタンを表示する
    topBtn.fadeIn();
  }else{
    //---- 画面が80pxより上なら、ボタンを表示しない
    topBtn.fadeOut();
  } 
});
 
// ◇ボタンをクリックしたら、スクロールして上に戻る
topBtn.click(function(){
  $('body,html').animate({
  scrollTop: 0},800);
  return false;
});

});

$(function(){
    var aboutBtn=$('#aboutmeBtn');
    var projectBtn=$('#projectBtn');
    var educationBtn=$('#educationBtn');
    var blogBtn=$('#blogBtn');
    var githubBtn=$('#githubBtn');
    var musicBtn=$('#musicBtn');
    var serviceBtn=$('#serviceBtn');

    aboutBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#aboutme").offset().top
        }, 800);
        return false;
    });

    projectBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#project").offset().top
        }, 800);
        return false;
    });

    educationBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#education").offset().top
        }, 800);
        return false;
    });
    blogBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#blog").offset().top
        }, 800);
        return false;
    });
    githubBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#github").offset().top
        }, 800);
        return false;
    });
    serviceBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#service").offset().top
        }, 800);
        return false;
    });
    musicBtn.click(function(){
        $('html, body').animate({
          scrollTop: $("#music").offset().top
        }, 800);
        return false;
    });
});