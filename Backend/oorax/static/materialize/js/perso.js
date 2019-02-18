// pour les paramettres

 // pour popop
 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
  });

  // Or with jQuery

  $(document).ready(function(){
    $('.modal').modal();
  });



//pour select
  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, options);
  });

  $(document).ready(function(){
    $('select').formSelect();
  });



//drop down
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, options);
  });
  $(document).ready(function(){
    $('.collapsible').collapsible();
  });

//pour menu
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, options);
});

$(document).ready(function(){
  $('.sidenav').sidenav();
  $(".dropdown-trigger").dropdown();

});


//drop dow 3
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, options);
  });

  // Or with jQuery

  $('.dropdown-trigger').dropdown();




// auto complette

//recup id chapitre
/*
function changementType()
{


var type = document.getElementById("test1").value;

console.log(type);

if (type =)
{
document.getElementById("bien").style="display:block";

}
else if(type==0)
{
document.getElementById("good").style="display:block";

}
else
{

document.getElementById("bien").style="display:none";
}

}
*/
/* step by step debut */
