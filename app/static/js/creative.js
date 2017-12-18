(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 57)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 57
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Scroll reveal calls
  window.sr = ScrollReveal();
  sr.reveal('.sr-icons', {
    duration: 600,
    scale: 0.3,
    distance: '0px'
  }, 200);
  sr.reveal('.sr-button', {
    duration: 1000,
    delay: 200
  });
  sr.reveal('.sr-contact', {
    duration: 600,
    scale: 0.3,
    distance: '0px'
  }, 300);

  // Magnific popup calls
  $('.popup-gallery').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });



  // Crazy Investment
  let crazy = window.crazy ? window.crazy : {};
  crazy.selectedStrategies = [];

  // strategy selection and input amount check
  $(document).on("keyup", "#input_amount", function(){
    toogleHintAndSubmitBtn();
  });

  $(document).on("click", ".strategy-container", function(){
    // toggle icon visibility
    $(this).find("i.strategy-checked-icon").toggleClass("invisible");

    // update selected strategies
    let key = $(this).find("span.strategy-key").text();
    let keyIndex = crazy.selectedStrategies.indexOf(key);
    if(keyIndex < 0)
    {
      crazy.selectedStrategies.push(key); 
    }
    else
    {
      crazy.selectedStrategies.splice(keyIndex, 1);
    }

    toogleHintAndSubmitBtn();

    console.log(crazy.selectedStrategies);
  })

  // form submit control
  $(document).on("click", "#submit_strategy_selection", function(){

    let $form = $("#strategy_selection_form");
    $form.find("#selected_strategies_val").val(JSON.stringify(crazy.selectedStrategies));
    $form.submit();

  });

  function toogleHintAndSubmitBtn()
  {
    let $selection_hint = $("#selection_hint");
    let $submit_btn_container = $("#submit_btn_container");
    if(validStratrgiesInput())
    {
      $selection_hint.hide();
      $submit_btn_container.show(); 
    }
    else
    {
      $selection_hint.show();
      $submit_btn_container.hide();
    }
  }

  function validStratrgiesInput()
  {
    let inputAmount = $("#input_amount").val();
    if(!inputAmount || inputAmount.length < 1)
    {
      return false;
    }
    if(crazy.selectedStrategies.length > 2 
      || crazy.selectedStrategies.length <= 0 
      || parseFloat(inputAmount) < 5000)
    {
      return false;
    }

    return true;
  }


})(jQuery); // End of use strict
