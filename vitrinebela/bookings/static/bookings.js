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
				var title = prompt('Event Title:');
				var eventData;
				if (title) {
					eventData = {
						title: title,
						start: start.format('YYYY-MM-DD HH:mm:ss'),
						end: end.format('YYYY-MM-DD HH:mm:ss'),
                        color: '#ff00ff'
					};
					$('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true

                      $.ajax({
                        type: "POST",
                        url: '/api/bookings/create/',
                        data: {
                          user: '1',
                          title: title,
                          start: start.format('YYYY-MM-DD HH:mm:ss'),
                          end: end.format('YYYY-MM-DD HH:mm:ss'),
                          all_day: true,
                          color: '#ff00ff'
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

                              user: '1',
                              title: event.title,
                              start: event.start.format(),
                              end: event.end.format(),
                              all_day: true,
                              color: '#ff00ff'
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

                              user: '1',
                              title: event.title,
                              start: event.start.format(),
                              end: event.end.format(),
                              all_day: true,
                              color: '#ff00ff'
                        },
                    success: function(json) {
                        alert(event.title + " foi modificado para data " + event.start.format('L'));
                    }
                });

            },



			editable: true,
			eventLimit: true, // allow "more" link when too many events
			events: '/api/bookings/'
		});

	});