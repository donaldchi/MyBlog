$(function() {
  var API_KEY = '656543be107a732c0a43bf388631d886'
  var city = 'Tokyo';
  var url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&units=metric&APPID=' + API_KEY;
  $.ajax({
    url: url,
    dataType: "json",
    type: 'GET',
  })
  .done(function(data) {
    var insertHTML = "";
    var cityName =data.city.name;
    
    //format mont/day/weekday 
    var d = new Date();
    var year = d.getFullYear();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var weekday = d.getDay();
    var weekdays = ["日", "月", "火", "水", "木", "金", "土"];

    $('#city-name').html("Weather: "+cityName);
    for (var i = 0; i <= 8; i = i + 2) {
      insertHTML += buildHTML(data, i);
    }
    insertHTML = '<ul class="myweather">' + insertHTML + "</ul>"
    $('#weather').html(insertHTML);
  })
  .fail(function(data) {
    console.log("失敗しました");
  });
});

function buildHTML(data, i) {
  var Week = new Array("（日）","（月）","（火）","（水）","（木）","（金）","（土）");
  var date = new Date (data.list[i].dt_txt);
  date.setHours(date.getHours() + 9);
  var month = date.getMonth()+1;
  var day = month + "/" + date.getDate() +"<br>"+date.getHours() + "時";
  console.log(data);
  var icon = data.list[i].weather[0].icon;
  var weatherID = data.list[i].weather[0].id;
  
  var windSpeed = data.list[i].wind.speed;
  var windDegree = data.list[i].wind.deg;
  console.log("wind: " + windSpeed + ", " + windDegree);

  var html = 
  '<li class="myweather__item">'+
    '<div class="weather-date">' + day + '</div>' +
    '<img src="http://openweathermap.org/img/w/'+icon+'.png">'+
    '<div class="weather-main">'+translateWeather(weatherID)+'</div>'+
    '<div class="weather-temp">'+Math.round(data.list[i].main.temp)+'度</div>'+
    '<div class="weather-wind">風('+windDirect(windDegree)+')<br>' + windSpeed + 'm</div>' +
  '</li>';
  return html
}

function translateWeather(id) {
  var weatherDescriptions = {
    200 : '小雨と雷雨',201 : '雨と雷雨',202 : '大雨と雷雨',
    210 : '光雷雨',211 : '雷雨',212 : '重い雷雨',
    221 : 'ぼろぼろの雷雨',230 : '小雨と雷雨',231 : '霧雨と雷雨',
    232 : '重い霧雨と雷雨',300 : '光強度霧雨',301 : '霧雨',
    302 : '重い強度霧雨',310 : '光強度霧雨の雨',311 : '霧雨の雨',
    312 : '重い強度霧雨の雨',313 : 'にわかの雨と霧雨',314 : '重いにわかの雨と霧雨',
    321 : 'にわか霧雨',500 : '小雨',501 : '適度な雨',502 : '重い強度の雨',
    503 : '非常に激しい雨',504 : '極端な雨',511 : '雨氷',520 : '光強度のにわかの雨',
    521 : 'にわかの雨',522 : '重い強度にわかの雨',531 : '不規則なにわかの雨',
    600 : '小雪',601 : '雪',602 : '大雪','611' : 'みぞれ',612 : 'にわかみぞれ',
    615 : '光雨と雪',616 : '雨や雪',620 : '光のにわか雪',621 : 'にわか雪',
    622 : '重いにわか雪',701 : 'ミスト',711 : '煙',721 : 'ヘイズ',
    731 : '砂、ほこり旋回する',741 : '霧',751 : '砂',761 : 'ほこり',
    762 : '火山灰',771 : 'スコール',781 : '竜巻',800 : '晴天',
    801 : '薄い雲',802 : '雲',803 : '曇りがち',804 : '厚い雲',
  }
  return weatherDescriptions[id];
}

function windDirect(degree) {
  if (degree<22.5) {
    degree += 360
  }

  if(degree > 337.5 & degree < 382.5) {
    return "北";
  } else if(degree >= 22.5 & degree < 67.5){
    return "東北";
  } else if(degree >= 67.5 & degree < 112.5){
    return "東";
  } else if(degree >= 112.5 & degree < 157.5){
    return "東南";
  } else if(degree >= 157.5 & degree < 202.5){
    return "南";
  } else if(degree >= 202.5 & degree < 247.5){
    return "西南";
  } else if(degree >= 247.5 & degree < 292.5){
    return "西";
  } else if(degree >= 292.5 & degree < 337.5){
    return "西北";
  } else {
    return "";
  }
}



