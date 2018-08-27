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

 $(document).ready(function() {
        BindControls();
    });

    function BindControls() {
        var Countries = [
            'Cour',
            'Annonce',
            'Evènement',
            'Pharmacie',
            ];

        $('#tvsearch').autocomplete({
            source: Countries,
            minLength: 0,
            scroll: true
        }).focus(function() {
            $(this).autocomplete("search", "");
        });
    }


