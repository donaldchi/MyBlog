(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-89568419-2', 'auto');
ga('send', 'pageview');

function textNumbersToImages(text) {
        var output = '';
        var images = ['0.png', '1.png', '2.png', '3.png', 
            '4.png', '5.png', '6.png', '7.png', '8.png', '9.png'];
        var nums = text.replace(/\D/g, ''); 
        for (var i=0; i < nums.length; i++) {
 output += '<img width="40" height="40" src="/static/images/number/'+images[nums.charAt(i)]+'">'
        }
        document.write(output);
};