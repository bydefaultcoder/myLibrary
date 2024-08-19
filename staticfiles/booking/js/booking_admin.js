(function($) {
    $(document).ready(function() {
        let availabletimming = []
        let start_Dropdown = $('#id_start_time');
        let end_Dropdown = $('#id_end_time');
        // Listen for changes on the location dropdown
        $('#id_location').change(function() {
            console.log("hello for location")
            var locationId = $(this).val();  // Get selected location ID
            var seatDropdown = $('#id_seat');

            if (locationId) {
                // Clear the seat dropdown
                seatDropdown.empty();

                // Fetch seats associated with the selected location
                $.ajax({
                    url: '/admin/booking/get_seats_by_location/',  // URL to fetch seats
                    data: {
                        'location_id': locationId
                    },
                    success: function(data) {
                        console.log(data)
                        seatDropdown.append('<option value="">Select</option>');
                        $.each(data, function(key, value) {
                            seatDropdown.append('<option value="' + key + '">' + value + '</option>');
                        });
                    }
                });
            } else {
                seatDropdown.empty();
                seatDropdown.append('<option value="">---------</option>');
            }
        });
        console.log("javascript here")
        // -------------------for timming
// Event handler for seat selection
// Event handler for seat selection
        $('#id_seat').change(function() {
            // console.log("hello")
            console.log("hello")
            var SeatId = $(this).val();  // Get selected seat ID

            if (SeatId) {

                $.ajax({
                    url: '/admin/booking/get_timming_by_seat/',  // URL to fetch seats
                    data: {
                        'seat_id': SeatId
                    },
                    success: function(data) {
                        console.log(data)
                        availabletimming = data["data"]
                        updateStart(availabletimming)
                        // updateEnd(data)
                        end_Dropdown.empty();
                        end_Dropdown.append('<option value="">---------</option>');
                    }
                });
            } else {
                        availabletimming = {}
                        start_Dropdown.empty();
                        start_Dropdown.append('<option value="">---------</option>');

                        end_Dropdown.empty();
                        end_Dropdown.append('<option value="">---------</option>');
                    }
        });

        $('#id_start_time').change(function(){
            if(!$(this).val()){
                return
            }
            console.log("hello clicked on id_start_time ");
            let timeAfter = parseInt($(this).val().split(":")[0]);  // Get selected time
            console.log(timeAfter,"line 73")
            let hours = $('#id_hours').val();
            console.log(hours)
            if(hours==0){
                let new_timming_available = getAvailableTimmig(availabletimming,timeAfter)//work here..........
                if(!new_timming_available.length){
                    alert("no time available")
                }
                updateEnd(new_timming_available)
                console.log("value set")
            }else{
                const t = parseInt(timeAfter) + parseInt(hours)
                end_Dropdown.empty();
                end_Dropdown.append(`<option value="${correctIt(t%24)}:00:00" selected> ${timeDescription(t%24)} </option>`);
                console.log("disabled")
            }       
        })

        $('#id_hours').change(function(){
            let hour = $(this).val();
            
            if(hour==0) return;

            let timmings = [];
            availabletimming.forEach((e,_,array)=>{

                if(isValidTime(array,e,hour)){   
                        timmings.push(e)
                }
            })

            console.log(timmings)

            if(timmings.length<1){
                alert("Duration Not Possible")
                start_Dropdown.removeAttr("selected");
                end_Dropdown.removeAttr("selected");
                return;
            }
            
            start_Dropdown.empty();
            start_Dropdown.append('<option value="">Select</option>');
            
            // let get_selected_value = start_Dropdown.val()
            // for(let i=0;i<hour_to_select - hour;i++){
            timmings.forEach(startT => {

                let end = (parseInt(startT) + parseInt(hour))%24

                end_Dropdown.empty();
                end_Dropdown.append(`<option value="${correctIt(end)}:00:00" selected> ${timeDescription(end%24)} </option>`);
                start_Dropdown.append(`<option value="${correctIt(startT)}:00:00" selected>${timeDescription(startT % 24)}</option>`);  
            });
            
        })

        function getAvailableTimmig(timmings,selectedTime){
            console.log(timmings)
            let timminingLength = timmings.length
            let selected = selectedTime
            let privious = selectedTime
            
            let i = timmings.indexOf(selected)+1
            let availabletimming = []
            console.log("finding available timming....")
            while(true){
              let index = i % timminingLength;
              let next = timmings[index];
              if(privious+1==next || (privious==23 && next==0)  ){
                // console.log(next);
                availabletimming.push(next)
                privious = next;
                i++;
              }else{
                break;
              }
              
              if(next==selected ){
                break;
              }
            }
            return availabletimming;
      }

        function updateStart(data){
            start_Dropdown.empty();
            start_Dropdown.append('<option value="">Select</option>');
            $.each(data, function(inedx,value) {
                start_Dropdown.append(`<option value="${correctIt(value)}:00:00" >${timeDescription(value%24)}</option>`);
            });
        }
        function correctIt(value){
            let h = `${value}`
            if(value<10){
                h = `0${value}`
              }
            return h
        }

        function updateEnd(data){
            end_Dropdown.empty();
            end_Dropdown.append('<option value="">Select</option>');
            console.log(data)
            $.each(data, function(index,value) {
                console.log(index,value)
                let h = `${value}`
                if(value<10){
                  h = `0${value}`
                }
                end_Dropdown.append(`<option value="${h}:00:00"> ${timeDescription(value%24)}</option>`);
            });
        }

        function isValidTime(timmingsList=[],atTime,hour){
            let flag = true
            if(atTime+hour<24){
                for(let i = 1;i<=hour;i++){
                    if(!timmingsList.includes(atTime+i)){
                        flag = false
                        break
                    }
                }
            }else{
                for(let i = 1;i<=hour;i++){
                    if(!timmingsList.includes((atTime+i)%24)){
                        flag = false
                        break
                    }
                }
            }
            return flag
        }

        function timeDescription(hour) {
            // Check if the input is valid
            if (hour < 0 || hour > 23) {
                return "Invalid hour! Please enter a number between 0 and 23.";
            }
        
            // Determine if the time is AM or PM
            let period = hour < 12 ? 'AM' : 'PM';
            
            // Convert 24-hour time to 12-hour time
            let adjustedHour = hour % 12;
            adjustedHour = adjustedHour === 0 ? 12 : adjustedHour; // Convert hour 0 to 12
        
            // Determine the time of day (morning, evening, night)
            let timeOfDay;
            if (hour >= 5 && hour < 12) {
                timeOfDay = "morning";
            } else if (hour >= 12 && hour < 17) {
                timeOfDay = "afternoon";
            } else if (hour >= 17 && hour < 20) {
                timeOfDay = "evening";
            } else {
                timeOfDay = "night";
            }
        
            return `${adjustedHour} ${period} ${timeOfDay}`;
        }




        });    

})(django.jQuery);


