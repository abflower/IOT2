$(document).ready(function(){
  
  var mc = {
    '950-980'     : 'dark_red',
    '981-995'     : 'red',
    '996-1025'    : 'orange',
    '1026-1050'   : 'green',
    '1051-1070'   : 'light_green'
  };
  
function between(x, min, max) {
  return x >= min && x <= max;
}
  var dc;
  var first; 
  var second;
  var th;
  
  $('div').each(function(index){
    
    th = $(this);
    
    dc = parseInt($(this).attr('data-color'),10);
    
    
      $.each(mc, function(name, value){
        
        
        first = parseInt(name.split('-')[0],10);
        second = parseInt(name.split('-')[1],10);
        
        console.log(between(dc, first, second));
        
        if( between(dc, first, second) ){
          th.addClass(value);
        }

    
    
      });
    
  });
});