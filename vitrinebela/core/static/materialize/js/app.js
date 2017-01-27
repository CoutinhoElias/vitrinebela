var dadosBusca = {
  			'Ué': null,
  			'Uélson': null,
  			'Uélsinnnnnnnnnnnnn': null,
  			'Uée': null
  		};

  		function callParallax(){
  			$('.parallax').parallax();

  			$('.dropdown-button').dropdown({
			      	belowOrigin: true, // Displays dropdown below the button
				    alignment: 'right' // Displays dropdown with edge aligned to the left of button
    		});
  		}

  		window.onload = callParallax();

  		$(document).ready(function(){
  			$('input#search').autocomplete({
    			data: dadosBusca
  			});
  			$('.modal-msg-trigger').leanModal();
  		});

  		$('#btn-sidebar').click(function(e){
  			e.preventDefault();
  			$('#wrapper').toggleClass('toggled');
  			$("#btn-sidebar").toggleClass("toggled");
  		});

  		$('.master-menu').click(function(e){
  			$(this).next('ul').slideToggle('slow');
  			$('.child-menu').not($(this).next()).slideUp();
  		});
