var jquery_src = "http://iot.insigma.com.cn/static/survey/js/jquery.min.js";
var ext_css_src = "http://iot.insigma.com.cn/static/survey/css/vote.css";
var jsonp_url = "http://iot.insigma.com.cn/bbs/survey/" + __vote_id +"/vote_load/?callback=?";
var post_url="http://iot.insigma.com.cn/bbs/survey/" + __vote_id +"/vote_update/?";

var jquery_src = "http://127.0.0.1:8000/static/js/jquery.min.js";
var ext_css_src = "http://127.0.0.1:8000/static/css/vote.css";
var jsonp_url = "http://127.0.0.1:8000/survey/" + __vote_id +"/vote_load/?callback=?";
var post_url="http://127.0.0.1:8000/survey/" + __vote_id +"/vote_update/?";
(function() {
// Localize jQuery variable
var jQuery;
/******** Load jQuery if not present *********/
if (window.jQuery === undefined || window.jQuery.fn.jquery !== '1.4.2') {
    var script_tag = document.createElement('script');
    script_tag.setAttribute("type","text/javascript");
    script_tag.setAttribute("src",
        jquery_src);
    if (script_tag.readyState) {
      script_tag.onreadystatechange = function () { // For old versions of IE
          if (this.readyState == 'complete' || this.readyState == 'loaded') {
              scriptLoadHandler();
          }
      };
    } else {
      script_tag.onload = scriptLoadHandler;
    }
    // Try to find the head, otherwise default to the documentElement
    (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
} else {
    // The jQuery version on the window is the one we want to use
    jQuery = window.jQuery;
    main();
}

/******** Called once jQuery has loaded ******/
function scriptLoadHandler() {
    // Restore $ and window.jQuery to their previous values and store the
    // new jQuery in our local jQuery variable
    jQuery = window.jQuery.noConflict(true);
    // Call our main function
    main(); 
}
            
/********* vote function ***********/
            function bindVote($) {
                $("#id_vote").click(function(){
                    var e = document.getElementsByName("option");
                    var option_ids='';
                    for (var i=0;i<e.length;i++){
                        if(e[i].checked){
                            option_ids=option_ids+','+e[i].value;
                        }
                    }
                    //TODO Fail return
                    
                    if(option_ids){
                        $.getJSON(post_url+"options="+option_ids+"&callback=?", function() {
                            loadVoteHtml($);
                        });

                    }
                });
            }
            function bindshow($){
                $("#id_voter_show").click(function(){
                    $(".svote-voters").toggle();
                    if ($("#id_voter_show").text()=="显示投票人信息"){
                        $("#id_voter_show").text("隐藏投票人信息");
                    }else{
                        $("#id_voter_show").text("显示投票人信息");
                    }

                });
            }
            function loadVoteHtml($) {
                $.getJSON(jsonp_url, function(data) {
                    //TODO SERVER DATE-->
                    $('#widget-container').html(data.html);//date-->ifValid,voted,html
                    bindshow($);
                    if (data.is_vote) {//TODO 是否vote
                        $("ul.vote  input").attr("disabled","disabled");
                        $("#id_vote").attr("disabled","disabled");
                        if(data.voted){$("#id_vote").text("已投票");}
                    } else {
                        bindVote($);
                    }

                }, 'json');
            }

/******** Our main function ********/
function main() {
    jQuery(document).ready(function($) { 
        /******* Load CSS *******/
        var css_link = $("<link>", { 
            rel: "stylesheet", 
            type: "text/css", 
            href: ext_css_src 
//            href: "http://127.0.0.1:8000/media/djblets/css/vote.css"
        });
        css_link.appendTo('head');          
        /******* Load HTML *******/
        loadVoteHtml($);
        //$.getJSON(jsonp_url, function(data) {
        //  $('#widget-container').html("This data comes from another server: " + data.html);
        //});
    });
}

})(); // We call our anonymous function immediately
