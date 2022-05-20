document.addEventListener('DOMContentLoaded', function () {

$(document).ready(function() {
        navigator.geolocation.getCurrentPosition(coordinates); 
      
        function coordinates(pos) {
          var la = pos.coords.latitude;
          var lon = pos.coords.longitude;
          weather(la, lon);
        }
      
        function weather(la, lon) {
          var URL = `https://fcc-weather-api.glitch.me/api/current?lat=${la}&lon=${lon}`;
          $.getJSON(URL, function(data) {
            exhibit(data);
          });
        }
      
        function exhibit(data) {
          if (data.weather[0].main == "Sunny" || data.weather[0].main == "sunny") {
            $(".weathercon").html(
              "<i class='fas fa-sun' style='color: #d36326;'></i>"
            );
          } else {
            $(".weathercon").html(
              "<i class='fas fa-cloud' style='color: #44c3de;'></i>"
            );
           }
          }
      
      
        
      });

      $(document).ready(function() {
        
        element = document.getElementsByClassName("text-muted")
        for (let i = 0; i < element.length; i++) {
            text = document.getElementsByClassName("text-muted")[i].innerText
            var date = new Date(text)
            document.getElementsByClassName("text-muted")[i].innerText = date.toDateString()
        }
    });
    
    
    window.addEventListener('scroll', function(e) {
                  $.ajax({
                    success: function (data) {
                        if (data["success"]) {
                            articles = data["data"]
                            article_container= ''
                            for (let i = 0; i < articles.length; i++) {
                              article_container+= ' \
                                        <div class="col-md-8">\
                                            <div class="card-body">\
                                                <h5 class="card-title"><a href="'+ articles[i]["url"] +'" target="_blanck">'+ articles[i]["title"] +'</a></h5>\
                                                <p class="card-text">'+ articles[i]["description"] +'</p>\
                                                <p class="card-text"><small class="text-muted">'+ articles[i]["publishedat"] +'</small></p>\
                                            </div>\
                                        </div>\
                                                \
                                        <div class="col-md-4 img-box">\
                                            <img src="'+ articles[i]["image"] +'" class="card-img" alt="..." height="100%">\
                                        </div>\
                                        '
                            }
                            $("#article").append(article_container);
                            p += 1
                            ws = true;
                            }
                        else {
                          ws = true;
                        }
                    }
                });
            })
    
    window.onscroll = function() {stickyfunction()};

    var navbar = document.getElementById("navbar");

    var sticky = navbar.offsetTop;

    function stickyfunction() {
      if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
      } else {
        navbar.classList.remove("sticky");
      }
    }
  })