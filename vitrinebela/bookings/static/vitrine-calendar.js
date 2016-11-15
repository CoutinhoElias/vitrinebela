/**
 *	Neon Calendar Script
 *
 *	Developed by Arlind Nushi - www.laborator.co
 */

var neonCalendar = neonCalendar || {};

    function saveEventUpdate(event) {
        url = '/SIAV/calendario/crea_eventos/';

        // Create a copy of the event object
        //data = $.extend({}, event);
        // Replace string date with timestamp (ms since epoch)
        console.log(event);
        if (event.end == undefined) {
            event.end = ""
        };
        if (event.id == undefined) {
            event.id = ""
        };

        var ret_id = '';

        var jqxhr = jQuery.post(url, {
                id: event.id,
                title: event.title,
                start: event.start.valueOf(),
                avaluo_id: event.avaluo_id,
                allDay: event.allDay,
                end: event.end.valueOf()
            }, function(responseData) {
                // swal("Carga exitosa.","","success");
                // Executed on successful update to backend

                // Newly added event
                if (event.id != undefined) {
                    // Get event ID from insert response
                    obj = jQuery.parseJSON(responseData);
                    ret_id = obj.id;
                    event.id = ret_id;

                    // Render the event on the calendar
                    jQuery('#calendar').fullCalendar('renderEvent', event, true);
                }
            })
            .fail(function() {
                swal("Hubo un error procesando la solicitud, intente de nuevo.", "", "err");
            })

    }

    function deleteEvent($, evento_id) {
        url = '/SIAV/calendario/elimina_eventos/';
 
        // Create a copy of the event object
        //data = $.extend({}, event);
        // Replace string date with timestamp (ms since epoch)

        if (evento_id != undefined) {
            event.id = evento_id
        };

        var ret_id = '';

        var jqxhr = $.post(url, {
                id: event.id,
            }, function(responseData) {
                // swal("Carga exitosa.","","success");
                // Executed on successful update to backend

                // Newly added event
                if (event.id == undefined) {
                    // Get event ID from insert response
                    obj = jQuery.parseJSON(responseData);
                    ret_id = obj.id;
                    event.id = ret_id;

                    // Render the event on the calendar
                    $('#calendar').fullCalendar('removeEvents', evento_id);
                    $('#eventContent').dialog("close");
                }
            })
            .fail(function() {
                swal("Hubo un error procesando la solicitud, intente de nuevo.", "", "err");
            })

    }

    function updateEvent($, evento_id,visitador_id) {
        url = '/SIAV/calendario/actualiza_visitador/';
 
        // Create a copy of the event object
        //data = $.extend({}, event);
        // Replace string date with timestamp (ms since epoch)

        if (evento_id != undefined) {
            event.id = evento_id
        };

        var ret_id = '';

        var jqxhr = $.post(url, {
                id: event.id,
                visitador_id: visitador_id,
            }, function(responseData) {
                // swal("Carga exitosa.","","success");
                // Executed on successful update to backend

                // Newly added event
                if (event.id == undefined) {
                    // Get event ID from insert response
                    obj = jQuery.parseJSON(responseData);
                    ret_id = obj.id;
                    event.id = ret_id;

                    // Render the event on the calendar
                    $('#calendar').fullCalendar('removeEvents', evento_id);
                    $('#calendar').fullCalendar( 'refetchEvents' );
                    $('#eventContent').dialog("close");
                }
            })
            .fail(function() {
                swal("Hubo un error procesando la solicitud, intente de nuevo.", "", "err");
            })

    }

     jQuery('.draggable').draggable({
        revert: false, // immediately snap back to original position
        duration: '00:30',
        revertDuration: 0 //
    });
   

;(function($, window, undefined)
{
	"use strict";

	$(document).ready(function()
	{
		neonCalendar.$container = $(".calendar-env");

		$.extend(neonCalendar, {
			isPresent: neonCalendar.$container.length > 0
		});

		// Mail Container Height fit with the document
		if(neonCalendar.isPresent)
		{
			neonCalendar.$sidebar = neonCalendar.$container.find('.calendar-sidebar');
			neonCalendar.$body = neonCalendar.$container.find('.calendar-body');


			// Checkboxes
			var $cb = neonCalendar.$body.find('table thead input[type="checkbox"], table tfoot input[type="checkbox"]');

			$cb.on('click', function()
			{
				$cb.attr('checked', this.checked).trigger('change');

				calendar_toggle_checkbox_status(this.checked);
			});

			// Highlight
			neonCalendar.$body.find('table tbody input[type="checkbox"]').on('change', function()
			{
				$(this).closest('tr')[this.checked ? 'addClass' : 'removeClass']('highlight');
			});


			// Setup Calendar
			if($.isFunction($.fn.fullCalendar))
			{
				var calendar = $('#calendar');

				calendar.fullCalendar({
        timezone: 'America/Monterrey',
        lang: 'es',
        minTime: "07:00:00",
        maxTime: "19:00:00",
        defaultTimedEventDuration: '00:30:00',
        forceEventDuration: true,
        allDaySlot: false,
        defaultView: 'agendaWeek',
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: {
            url: '/SIAV/calendario/carga_eventos/',
            type: 'POST',
            allDay: false,
            error: function() {
                swal('Hubo un error al cargar los eventos, contacte al administrador.', "", "error");
            }
        },
        googleCalendarApiKey: 'AIzaSyAk5zR9LcqsE5UuW9bTYdyqZGzocW-NhPg',
        aspectRatio: 2,
        /*
        events: {
            googleCalendarId: '8887t7tu2lnp4onj4g1lr74vj4@group.calendar.google.com',
            className: 'gcal-event' // an option!
        },*/
        eventStartEditable: true,
        eventDurationEditable: false,
        droppable: true,

        eventClick: function(calEvent, jsEvent, view) {

           // swal(calEvent.title.replace('-', '\n') + '\n' + calEvent.start.toLocaleString(), "", "");


            // change the border color just for fun
            //$(this).css('border-color', 'red');

        },
        drop: function(date, allDay) { // this function is called when something is dropped

            // retrieve the dropped element's stored Event Object
            var originalEventObject = jQuery(this).data('eventObject');

            // we need to copy it, so that multiple events don't have a reference to the same object
            var copiedEventObject = jQuery.extend({}, originalEventObject);

            // assign it the date that was reported
            var tempDate = new Date(date);
            copiedEventObject.start = date;
            copiedEventObject.end = new Date(tempDate.setMinutes(tempDate.getMinutes() + 30));
            //copiedEventObject.allDay = allDay;
            copiedEventObject.allDay = false; //< -- only change
            // render the event on the calendar
            // the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
            //$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
            saveEventUpdate(copiedEventObject);
            // is the "remove after drop" checkbox checked?
            // if ($('#drop-remove').is(':checked')) {
            // if so, remove the element from the "Draggable Events" list
            jQuery(this).remove();
            // }

        },
        eventDrop: function(event, dayDelta, minuteDelta, allDay, revertFunc) {
            console.log(event);
            saveEventUpdate(event);
        },
      eventRender: function (event, element) {
        element.attr('href', 'javascript:void(0);');
        element.click(function() {
            $("#startTime").html(moment(event.start).format('MMM Do h:mm A'));
            $("#endTime").html(moment(event.end).format('MMM Do h:mm A'));
            $("#eventInfo").html(event.description);
            $("#eventId").html(event.id);
            $("#id_Visitadores").val(event.visitador);
            $("#eventLink").attr('href', event.url);
            $("#eventContent").dialog({ modal: true, title: event.title, width:450,
                 buttons :  { 
                     "eventLink" : {
                         text: "Eliminar",
                         href: event.url,
                         id: "eventLink",
                         click: function(){

                          var singleValues = $( "#eventId" ).html();
                          // alert( singleValues );
                          deleteEvent(singleValues);

                         }   
                      }}});
        });

    }
				});

				$("#draggable_events li a").draggable({
					zIndex: 999,
					revert: true,
					revertDuration: 0
				}).on('click', function()
				{
					return false;
				});
			}
			else
			{
				alert("Please include full-calendar script!");
			}


			$("body").on('submit', '#add_event_form', function(ev)
			{
				ev.preventDefault();

				var text = $("#add_event_form input");

				if(text.val().length == 0)
					return false;

				var classes = ['', 'color-green', 'color-blue', 'color-orange', 'color-primary', ''],
					_class = classes[ Math.floor(classes.length * Math.random()) ],
					$event = $('<li><a href="#"></a></li>');

				$event.find('a').text(text.val()).addClass(_class).attr('data-event-class', _class);

				$event.appendTo($("#draggable_events"));

				$("#draggable_events li a").draggable({
					zIndex: 999,
					revert: true,
					revertDuration: 0
				}).on('click', function()
				{
					return false;
				});

				fit_calendar_container_height();

				$event.hide().slideDown('fast');
				text.val('');

				return false;
			});
		}
	});

})(jQuery, window);


function fit_calendar_container_height()
{
	if(neonCalendar.isPresent)
	{
		if(neonCalendar.$sidebar.height() < neonCalendar.$body.height())
		{
			neonCalendar.$sidebar.height( neonCalendar.$body.height() );
		}
		else
		{
			var old_height = neonCalendar.$sidebar.height();

			neonCalendar.$sidebar.height('');

			if(neonCalendar.$sidebar.height() < neonCalendar.$body.height())
			{
				neonCalendar.$sidebar.height(old_height);
			}
		}
	}
}

function reset_calendar_container_height()
{
	if(neonCalendar.isPresent)
	{
		neonCalendar.$sidebar.height('auto');
	}
}

function calendar_toggle_checkbox_status(checked)
{
	neonCalendar.$body.find('table tbody input[type="checkbox"]' + (checked ? '' : ':checked')).attr('checked',  ! checked).click();
}