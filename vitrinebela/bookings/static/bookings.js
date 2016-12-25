    $(document).ready(function() {

		$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay,listDay,listWeek,listMonth'
			},
			defaultDate: new Date(),
			navLinks: true, // can click day/week names to navigate views
			selectable: true,
			selectHelper: true,
            locale: 'pt-br',

            handleWindowResize: true,
            weekends: true, // Hide weekends


            minTime: '07:30:00', // Start time for the calendar
            maxTime: '22:00:00', // End time for the calendar

            displayEventTime: true, // Display event time
            editable: true,
			eventLimit: true, // allow "more" link when too many events
			events: '/api/bookings/',

        // {#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*        #}
        // {# ENVIANDO DADOS PARA O MODAL BOOTSTRAP#}
            eventClick:  function(event, jsEvent, view) {
                // $("#modal-titleInput").val(event.title);
                // $("#modal-startInput").val(event.start.format());
                // $("#modal-endInput").val(event.end.format('DD-MM-YYYY HH:mm:ss'));
                // $("#modal-colorInput").val(event.color);
                // $("#modalTitle").html(event.title);
                // $('#fullCalModal').modal();
                // return false;
                window.location='/reserva/editar/'+ event.id;
            },
        // {#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*        #}

			select: function(start, end) {
                // var title = prompt('Nome do evento:');
                // var color = prompt('Agoraa cor do evento:');
				var eventData;
				if (title) {
					eventData = {
						title: title,
						start: start.format(),
						end: end.format(),
                        color: color
					};
					$('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true

                      $.ajax({
                        type: "POST",
                        url: '/api/bookings/create/',
                        data: {
                          //user: 2,
                          title: title,
                          start: start.format(),
                          end: end.format(),
                          all_day: true,
                          color: color
                        }
                      });
				}
				$('#calendar').fullCalendar('unselect');
			},



            eventDrop: function(event, delta) {
                $.ajax({
                        type: "PUT",
                        url: '/api/bookings/' + event.id +'/edit/',
                        data: {

                              //user: event.user,
                              title: event.title,
                              start: event.start.format(),
                              end: event.end.format(),
                              all_day: true,
                              color: event.color,
                              editable: event.editable
                        },
                    success: function(json) {
                        alert(event.title + " foi modificado para data " + event.start.format('L'));
                    }
                });
            },

            eventResize: function(event) {
                $.ajax({
                        type: "PUT",
                        url: '/api/bookings/' + event.id +'/edit/',
                        data: {

                              //user: event.user,
                              title: event.title,
                              start: event.start.format(),
                              end: event.end.format(),
                              all_day: true,
                              color: event.color,
                              editable: event.editable,
                        },
                    success: function(json) {
                        alert(event.title + " foi modificado para data " + event.start.format('L'));
                    }
                });

            },


		});


        var days = []

        $.get( "/api/bookings/feriado/", function( data ) {


            $.each(data, function(index, value){

                //alert(value.start.substr(0, 10))
                days.push(value.start.substr(0, 10))

            });


            $("td, th").each(function(){
                if(days.indexOf(this.dataset.date) >= 0){
                  $(this).css("background-color","red");
                }
            });

        });


});



//         {#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*        #}
// {#        CHAMADA DO MODAL PASSANDO OS VALORES DE EVENT#}
//         $('#exampleModal').on('show.bs.modal', function (event) {
//           var button = $(event.relatedTarget) // Button that triggered the modal
//           var recipient = button.data('whatever') // Extract info from data-* attributes
//           // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//           // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//           var modal = $(this)
//           modal.find('.modal-title').text('New message to ' + event.start)
//           modal.find('.modal-titleInput').text(event.title)
//           modal.find('.modal-startInput').text(event.start)
//           modal.find('.modal-endInput').text(event.end)
//           modal.find('.modal-colorInput').text(event.color)
//           modal.find('.modal-body input').val(event.start)
//         })
        // {#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*        #}

	// });