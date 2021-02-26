$(document).ready(function() {
    $('.charcount1').keyup(function() {
        var characterCount1 = $(this).val().length,
          current = $('.current1'),
          maximum = $('.maximum1'),
          theCount = $('.the-count1');

      current.text(characterCount1);
        if (characterCount1 >= 245) {
        maximum.css('color', '#8f0001');
        current.css('color', '#8f0001');
        theCount.css('font-weight','bold');
      } else {
        current.css('color','#666');
        maximum.css('color','#666');
        theCount.css('font-weight','normal');
      }
    });

    $('.charcount2').keyup(function() {
        var characterCount2 = $(this).val().length,
          current = $('.current2'),
          maximum = $('.maximum2'),
          theCount = $('.the-count2');

      current.text(characterCount2);
        if (characterCount2 >= 3975) {
        maximum.css('color', '#8f0001');
        current.css('color', '#8f0001');
        theCount.css('font-weight','bold');
      } else {
        current.css('color', '#666');
        maximum.css('color','#666');
        theCount.css('font-weight','normal');
      }
    //    $('.current2').text($(this).val().length);
    });
});