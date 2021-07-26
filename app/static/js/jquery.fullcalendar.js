
!function($) {
    "use strict";

    var CalendarApp = function() {
        this.$body = $("body")
        this.$modal = $('#event-modal'),
        this.$event = ('#external-events div.external-event'),
        this.$calendar = $('#calendar'),
        this.$saveCategoryBtn = $('.save-category'),
        this.$categoryForm = $('#add-category form'),
        this.$extEvents = $('#external-events'),
        this.$calendarObj = null
    };


    /* on drop */
    CalendarApp.prototype.onDrop = function (eventObj, date) { 
        var $this = this;
            // retrieve the dropped element's stored Event Object
            var originalEventObject = eventObj.data('eventObject');
            var $categoryClass = eventObj.attr('data-class');
            // we need to copy it, so that multiple events don't have a reference to the same object
            var copiedEventObject = $.extend({}, originalEventObject);
            // assign it the date that was reported
            copiedEventObject.start = date;
            if ($categoryClass)
                copiedEventObject['className'] = [$categoryClass];
            // render the event on the calendar
            $this.$calendar.fullCalendar('renderEvent', copiedEventObject, true);
            // is the "remove after drop" checkbox checked?
            if ($('#drop-remove').is(':checked')) {
                // if so, remove the element from the "Draggable Events" list
                eventObj.remove();
            }
    },
    /* on click on event */
    CalendarApp.prototype.onEventClick =  function (calEvent, jsEvent, view) {

        var detail_log;
        $.ajax({
            type : 'GET',
            url : `/get_detail_log?date=${calEvent.date}`,
            async: false, // thực thi đồng bộ, chờ dữ liệu từ flask rồi mới thực hiện tiếp
        })
        .done(function(data) {
            // data = JSON.parse(data);
            console.log(data);
            detail_log = data;
        });


//console.log(detail_log)
        var $this = this;
            var form = $("<form></form>");
            form.append(`<h3>Chi tiết công: ${detail_log.date}</h3>`);
            // form.append("<div class='input-group m-b-20'><input class='form-control' type=text value='" + calEvent.title + "' /><span class='input-group-append'><button type='submit' class='btn btn-primary'>Lưu</button></span></div>");
            // form.append("<div class='input-group m-b-20'><input class='form-control' type=text value='" + calEvent.title + "' /><span class='input-group-append'></span></div>");
            // form.append(`<p>Thời điểm đến công ty: ${detail_log.time_in}</p>`);
            // form.append(`<p>Thời điểm rời công ty : ${detail_log.time_out}</p>`);
            // form.append(`<p>Correct time in : ${detail_log.correct_time_in}</p>`);
            // form.append(`<p>Correct time out : ${detail_log.correct_time_out}</p>`);


            var table = `<table id="customers">
                          <tr>
                            <td>Thời gian đi làm</td>
                            <td>${detail_log.time_in}</td>
                          </tr>
                          <tr>
                            <td>Thời gian về</td>
                            <td>${detail_log.time_out}</td>
                          </tr>
                          <tr>
                            <td>Thời gian công ty vào làm</td>
                            <td>${detail_log.correct_time_in}</td>
                          </tr>
                          <tr>
                            <td>Thời gian công ty tan ca</td>
                            <td>${detail_log.correct_time_out}</td>
                          </tr>
                    </table>`;
            form.append(table);


            $this.$modal.modal({
                backdrop: 'static'
            });
            $this.$modal.find('.delete-event').show().end().find('.save-event').hide().end().find('.modal-body').empty().prepend(form).end().find('.delete-event').unbind('click').click(function () {
                $this.$calendarObj.fullCalendar('removeEvents', function (ev) {
                    return (ev._id == calEvent._id);
                });
                $this.$modal.modal('hide');
            });
            $this.$modal.find('form').on('submit', function () {
                calEvent.title = form.find("input[type=text]").val();
                $this.$calendarObj.fullCalendar('updateEvent', calEvent);
                $this.$modal.modal('hide');
                return false;
            });
    },
    /* on select */
    CalendarApp.prototype.onSelect = function (start, end, allDay) {
        // var $this = this;
        //     $this.$modal.modal({
        //         backdrop: 'static'
        //     });
        //     var form = $("<form></form>");
        //     form.append("<div class='row'></div>");
        //     form.find(".row")
        //         .append("<div class='col-md-6'><div class='form-group'><label>Chấm công</label><input class='form-control' type='text' name='title'/></div></div>")
        //         .append("<div class='col-md-6'><div class='form-group'><label>Loại công</label><select class='select form-control' name='category'></select></div></div>")
        //         .find("select[name='category']")
        //         .append("<option value='bg-danger'>Đúng giờ</option>")
        //         .append("<option value='bg-success'>Muộn giờ</option>")
        //         .append("<option value='bg-warning'>Nghỉ</option></div></div>");
        //     $this.$modal.find('.delete-event').hide().end().find('.save-event').show().end().find('.modal-body').empty().prepend(form).end().find('.save-event').unbind('click').click(function () {
        //         form.submit();
        //     });
        //     $this.$modal.find('form').on('submit', function () {
        //         var title = form.find("input[name='title']").val();
        //         var beginning = form.find("input[name='beginning']").val();
        //         var ending = form.find("input[name='ending']").val();
        //         var categoryClass = form.find("select[name='category'] option:checked").val();
        //         if (title !== null && title.length != 0) {
        //             $this.$calendarObj.fullCalendar('renderEvent', {
        //                 title: title,
        //                 start:start,
        //                 end: end,
        //                 allDay: false,
        //                 className: categoryClass
        //             }, true);  
        //             $this.$modal.modal('hide');
        //         }
        //         else{
        //             alert('You have to give a title to your event');
        //         }
        //         return false;
                
        //     });
        //     $this.$calendarObj.fullCalendar('unselect');
    },
    CalendarApp.prototype.enableDrag = function() {
        //init events
        $(this.$event).each(function () {
            // create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
            // it doesn't need to have a start or end
            var eventObject = {
                title: $.trim($(this).text()) // use the element's text as the event title
            };
            // store the Event Object in the DOM element so we can get to it later
            $(this).data('eventObject', eventObject);
            // make the event draggable using jQuery UI
            $(this).draggable({
                zIndex: 999,
                revert: true,      // will cause the event to go back to its
                revertDuration: 0  //  original position after the drag
            });
        });
    }


    var logs;

    // $.get( "/home", function( data ) {
    //     data = JSON.parse(data);
    //     console.log(data);
    //     logs = data;
    // });

    $.ajax({
            type : 'GET',
            url : '/home',
            async: false, // thực thi đồng bộ, chờ dữ liệu từ flask rồi mới thực hiện tiếp
        })
        .done(function(data) {
            data = JSON.parse(data);
            logs = data;
            // console.log(data);
            // console.log(typeof logs);
        });



    /* Initializing */
    CalendarApp.prototype.init = function() {
        this.enableDrag();
        /*  Initialize the calendar  */
        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
        var form = '';
        var today = new Date($.now());


        var arrAllDayToCurrent = [];
        var dayHasLog = [];
        var dayNotHasLog = [];

        var first_day = new Date(new Date().getFullYear(), 0, 1);
        var today = new Date();
        today.setDate(today.getDate()+1);
        var next_day = new Date(first_day);

        while(today.toDateString() !== next_day.toDateString()){
          var dd = String(next_day.getDate()).padStart(2, '0');
          var mm = String(next_day.getMonth() + 1).padStart(2, '0');
          var yyyy = next_day.getFullYear();

          var res = yyyy+"-"+mm+"-"+dd;
          arrAllDayToCurrent.push(res);
          next_day.setDate(next_day.getDate()+1);
        }
        


        var events = [];
        for(var log of logs){
            var obj_in = {};
            var obj_out = {};

            if(log.tag_in == 1){
                obj_in.title = "Đúng giờ";
                obj_in.className = "bg-success";
            }
            else if(log.tag_in == 2){
                obj_in.title = "Muộn giờ";
                obj_in.className = "bg-warning";
            }
            else{
                obj_in.title = "Không log"
                obj_in.className = "bg-danger";   
            }

            if(log.tag_out == 1){
                obj_out.title = "Đúng giờ";
                obj_out.className = "bg-success";
            }
            else if(log.tag_out == 2){
                obj_out.title = "Về sớm";
                obj_out.className = "bg-warning";
            }
            else{
                obj_out.title = "Không log";
                obj_out.className = "bg-danger";
            }

            obj_in.start = log.date;
            obj_out.start = log.date;
            obj_in.date = log.date;
            obj_out.date = log.date;

            dayHasLog.push(log.date);
            events.push(obj_in);
            events.push(obj_out);
        }

        console.log(events);


        dayNotHasLog = arrAllDayToCurrent.filter( function( item ) {
          return !dayHasLog.includes( item );
        } );


        for(var d of dayNotHasLog){
            var obj_in = {};
            var obj_out = {};


            obj_in.title = "Không log"
            obj_in.className = "bg-danger";   

            obj_out.title = "Không log";
            obj_out.className = "bg-danger";

            obj_in.start = d;
            obj_out.start = d;
            obj_in.date = d;
            obj_out.date = d;

            events.push(obj_in);
            events.push(obj_out);
        }




        // var defaultEvents =  [{
        //         title: '1111111',
        //         start: "2021-5-1",
        //         className: 'bg-danger'
        //     },
        //     {
        //         title: 'Hòa',
        //         start: today,
        //         // end: new Date($.now() + 338000000),
        //         className: 'bg-success'
        //     },
        //     {
        //         title: '222222',
        //         start: new Date($.now() + 168000000),
        //         className: 'bg-info'
        //     },
        //     {
        //         title: '333333',
        //         start: new Date($.now() + 338000000),
        //         className: 'bg-warning'
        //     },
        //     {
        //         title: '4444444',
        //         start: new Date($.now() + 238000000),
        //         className: 'bg-primary'
        //     }
        //     ];

        var $this = this;
        $this.$calendarObj = $this.$calendar.fullCalendar({
            slotDuration: '00:15:00', /* If we want to split day time each 15minutes */
            minTime: '08:00:00',
            maxTime: '19:00:00',  
            defaultView: 'month',  
            handleWindowResize: true,   
            height: $(window).height() - 200,   
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            events: events,
            editable: true,
            droppable: true, // this allows things to be dropped onto the calendar !!!
            eventLimit: false, // allow "more" link when too many events
            selectable: true,
            drop: function(date) { $this.onDrop($(this), date); },
            select: function (start, end, allDay) { $this.onSelect(start, end, allDay); },
            eventClick: function(calEvent, jsEvent, view) { $this.onEventClick(calEvent, jsEvent, view); }

        });

        //on new event
        this.$saveCategoryBtn.on('click', function(){
            var categoryName = $this.$categoryForm.find("input[name='category-name']").val();
            var categoryColor = $this.$categoryForm.find("select[name='category-color']").val();
            if (categoryName !== null && categoryName.length != 0) {
                $this.$extEvents.append('<div class="external-event bg-' + categoryColor + '" data-class="bg-' + categoryColor + '" style="position: relative;"><i class="mdi mdi-checkbox-blank-circle m-r-10 vertical-middle"></i>' + categoryName + '</div>')
                $this.enableDrag();
            }

        });
    },

   //init CalendarApp
    $.CalendarApp = new CalendarApp, $.CalendarApp.Constructor = CalendarApp
    
}(window.jQuery),

//initializing CalendarApp
function($) {
    "use strict";
    $.CalendarApp.init()
}(window.jQuery);
