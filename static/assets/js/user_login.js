$(".email-signup").hide();
console.log("Hola");
$("#signup-box-link").click(function(){
  $(".email-login").fadeOut(150);
  $(".email-signup").delay(150).fadeIn(150);
  $("#login-box-link").removeClass("active");
  $("#signup-box-link").addClass("active");
});
$("#login-box-link").click(function(){
  $(".email-login").delay(150).fadeIn(150);;
  $(".email-signup").fadeOut(150);
  $("#login-box-link").addClass("active");
  $("#signup-box-link").removeClass("active");
});
