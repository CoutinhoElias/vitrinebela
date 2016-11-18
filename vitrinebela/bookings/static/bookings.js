/**
 * Created by eliaspai on 18/11/16.
 */
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


			select: function(start, end) {

				var title = prompt('Título do evento:');
				var eventData;
				if (title) {
					eventData = {

						title: title,
						date_start: start.format(),
                        date_end: end.format(),
                        all_day: true,
                        color: '#ff00ff'
					};
					// $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
                      $.ajax({
                        type: "POST",
                        url: '/api/bookings/create/',
                        data: {
                          user: '1',
                          title: title,
                          start: start.format(),
                          end: end.format(),
                          all_day: true,
                          color: '#ff00ff'
                        }
                      });
				}
                console.log(eventData);
				$('#calendar').fullCalendar('unselect');
			},

            eventDrop: function(event, delta, revertFunc) {

                alert(event.title + " was dropped on " + event.start.format() + " e o id=" + event.id);

                if (!confirm("Are you sure about this change?")) {
                    revertFunc();
                        eventData = {
                            id: event.id,
                            title: title,
                            date_start: start.format(),
                            date_end: end.format(),
                            all_day: true,
                            color: '#ff00ff'
					};
					// $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
                      $.ajax({
                        type: "POST",
                        url: '/api/bookings/update/',
                        data: {
                          id: event.id,
                          user: '1',
                          title: title,
                          start: start.format(),
                          end: end.format(),
                          all_day: true,
                          color: '#ff00ff'
                        }


                      });

                }

            },






            height: 650,

			editable: true,
			eventLimit: true, // allow "more" link when too many events
			events: '/api/bookings/'
		});


	});


