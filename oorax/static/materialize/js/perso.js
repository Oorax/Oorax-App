 // pour popop
 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
  });
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
});

// auto complette

$(function () {
    var availableTags = [
        "MongoDB",
        "ExpressJS",
        "Angular",
        "NodeJS",
        "JavaScript",
        "jQuery",
        "jQuery UI",
        "PHP",
        "Zend Framework",
        "JSON",
        "MySQL",
        "PostgreSQL",
        "SQL Server",
        "Oracle",
        "Informix",
        "Java",
        "Visual basic",
        "Yii",
        "Technology",
        "WilzonMB.com"
    ];
    $("#q").autocomplete({
        source: availableTags,
        minLength: 0
    }).focus(function(){
       $(this).autocomplete('search', $(this).val())
     });
});
/*document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems, options);
  });

  $(document).ready(function(){
    $('input#search').autocomplete({
      data: {
        "Annonce": null,
        "Actualité":null,
        "Cours": null,
        "Evenement":null,
        "Location":null,
        "Restaurant":null,
        "Renseignement":null,
        "Rencontre":null,
        "Pharmatie":null,
        "Google": 'https://placehold.it/250x250'
      },
    });
  });
*/
