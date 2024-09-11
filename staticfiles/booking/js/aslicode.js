(function($) {
    $(document).ready(function() {

        let MotnthlyPlanings =  []
        let availabletimming = []
        let start_Dropdown = $('#id_start_time');
        let end_Dropdown = $('#id_end_time');
        console.log($('#id_location').val())
        console.log($('#id_joining_date').val())

        // $('#id_seat').select2();
        
        console.log("Every thing is loaded++++++++++++++++++++++++++++++++")
        let seatDropdown = $('#id_seat');

        let hoursDropdown = $('#id_plan');
        let slectedPrize = 0

        // console.log(window.currentUserPK)
        // $.ajax({
        //     url: '/admin/booking/get_mothlyplans_by_user/',  // URL to fetch seats
        //     data: {
        //         'currentUserPK': window.currentUserPK
        //     },
        //     success: function(response) {
        //         // console.log(data)
        //         MotnthlyPlanings = response["data"]
        //         hoursDropdown.empty();
        //         // seatDropdown.append('<option value="">Select</option>');
        //         hoursDropdown.append('<option value="0">Select</option>');
        //         $.each(MotnthlyPlanings, function(key, value) {
        //             // console.log(key,value)
        //             let hours  = value.hours
        //             hoursDropdown.append(`<option value=${hours} onclick="selectPrize(${value.prize})" > ${value.hours} hours - monthly ${value.prize}(₹)</option>`);
        //         });
        //         // [{"timming_id": 4, "hours": 4, "prize": 300, "discription": "minimum", "status": "active", "created_by_id": 1}, {"timming_id": 5, "hours": 6, "prize": 500, "discription": "fix hours", "status": "active", "created_by_id": 1}]
        //     }
        // });

        function selectPrize(prize){
            console.log("prize selected")
            slectedPrize = prize
        }
        
        let seat_data
        $('#id_joining_date').keypress(function() {
            let joining_date = $(this).val();  // Get selected location ID
            let locationId =  $('#id_location').val();  // Get selected location ID
            console.log(joining_date,locationId)
            if (locationId) {
                // Clear the seat dropdown
                seatDropdown.empty();
                console.log("hello for location")
                // Fetch seats associated with the selected location
                $.ajax({
                    url: '/admin/api-booking/get_seats_by_location/',  // URL to fetch seats
                    data: {
                        'location_id': locationId,
                        'joining_date':joining_date
                    },
                    success: function(data) {
                        seat_data = data
                        console.log(data)
                        seatDropdown.append('<option value="">Select</option>');
                        $.each(data, function(value, key) {
                            seatDropdown.append('<option value="' + value + '">' + value + '</option>');
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
        // $('#id_seat').on('select2:select',function() {
        $('#id_seat').on('change',function() {
            // console.log("hello")
            console.log("hello")
            var SeatId = $(this).val();  // Get selected seat ID
            // console.log(SeatId,"3333333333333333333")
            if (SeatId) {

                $.ajax({
                    url: '/admin/api-booking/get_timming_by_seat/',  // URL to fetch seats
                    data: {
                        'seat_id': SeatId,
                        'joining_date':$('#id_joining_date').val()
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
                        availabletimming = []
                        start_Dropdown.empty();
                        start_Dropdown.append('<option value="">---------</option>');

                        end_Dropdown.empty();
                        end_Dropdown.append('<option value="">---------</option>');
                    }
        });

        $('#id_start_time').on('change',function(){
        // $('#id_start_time').on('select2:select',function(){
            if(!$(this).val()){
                return
            }
            console.log("hello clicked on id_start_time ");
            let timeAfter = parseInt($(this).val().split(":")[0]);  // Get selected time
            console.log(timeAfter,"line 73")
            let hours = parseInt($('#id_plan').val().split("_")[0]);
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

        // $('#id_plan').on('select2:select',function(){
        $('#id_plan').on('change',function(){
            let hour = parseInt($(this).val().split("_")[0]);
            if(hour==0) return;
            let timmings = [];
            availabletimming.forEach( function(e,_,array){

                if(isValidTime(array,e,hour)){   
                        timmings.push(e)
                }
            })
            console.log(timmings)
            if(timmings.length<1){
                alert("Duration Not Possible")
                start_Dropdown.removeAttr("selected");
                end_Dropdown.removeAttr("selected");
                calculateAmount()
                return;
            }
            start_Dropdown.empty();
            start_Dropdown.append('<option value="">Select</option>');
            // let get_selected_value = start_Dropdown.val()
            // for(let i=0;i<hour_to_select - hour;i++){
            console.log("calculating....")
            calculateAmount()
            timmings.forEach(startT => {
                let end = (parseInt(startT) + parseInt(hour))%24
                end_Dropdown.empty();
                end_Dropdown.append(`<option value="${correctIt(end)}:00:00" selected> ${timeDescription(end%24)} </option>`);
                start_Dropdown.append(`<option value="${correctIt(startT)}:00:00" selected>${timeDescription(startT % 24)}</option>`);  
            });

        })
        // console.log($('#id_discount').val())
        $('#id_discount').val(0)
        $('#id_remain_no_of_months').on('keyup', function() {calculateAmount()});
        $('#id_discount').on('keyup',function(){calculateAmount()});
        let totalAmountTOpay = 0
        function calculateAmount(){
            console.log("calculating")
            let months = $('#id_remain_no_of_months')
            let discount = $('#id_discount').val()
            let no_of_months = months.val()
            slectedPrize = 0
            if($('#id_plan').val()){
                slectedPrize = parseFloat($('#id_plan').val().split("_")[1])
            }

            if(!discount){
                discount = 0
            }
            // id_remain_no_of_months
            console.log(slectedPrize,no_of_months,discount)
            // if(slectedPrize>0 && no_of_months){
            if(!selectPrize){
                selectPrize = 0
            }
            if(!no_of_months){
                no_of_months = 0
            }
            if(!discount){
                discount = 0
            }
            totalAmountTOpay = no_of_months*slectedPrize *(100-discount)/100
            console.log(totalAmountTOpay)
            // $('#id_total_amount').prop('disabled', false);
            $('#id_total_amount').val(totalAmountTOpay)
                // $('#id_total_amount').prop('disabled', true);
            // }
        }
        let total_amount_flag = true
        $('#id_total_amount').prop('disabled', total_amount_flag);
        $('#total_amount_type').on('click',function(){
            console.log("cliccked on totoamount type")
            total_amount_flag = !total_amount_flag
            $('#id_total_amount').prop('disabled', total_amount_flag);
            if(total_amount_flag){
                $(this).text('Click to pay manual amount');
            }else{
                $(this).text('Click to pay custom amount');
            }
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


        $('#booking_form').submit(function(){
            $("#id_total_amount").removeAttr('disabled');
        });

        });    

})(django.jQuery);


