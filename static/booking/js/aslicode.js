(function($) {
    $(document).ready(function() {

        $("#id_seat").attr('disabled', 'disabled');
        $("#id_start_time").attr('disabled', 'disabled');
        $("#id_discount").attr('disabled', 'disabled');
        $("#id_total_amount_to_pay").attr('disabled', 'disabled');

        let MotnthlyPlanings =  []
        let availabletimming = []
        let start_Dropdown = $('#id_start_time');
        let end_Dropdown = $('#id_end_time');
        let forEndValueKeyTime = {}

        // $('#id_seat').select2();
        let seatDropdown = $('#id_seat');
        console.log("Every thing is loaded------------------------")

        let hoursDropdown = $('#id_plan');
        let slectedPrize = 0
        // let op = $('select2-id_location-container').val()
        // console.log(op)

        function selectPrize(prize){
            console.log("prize selected")
            slectedPrize = prize
        }
        let seat_data = {}
        function getSeats() {
            // to get location
            let locationId =  $("#id_location").val();
            console.log(locationId)
            if(!locationId){    
                alert("Please Select Library...")
                return
            }
            let joining_date = $('#id_joining_date').val()
            if(!joining_date){
                alert("Please Select Joining Date ...")
                return
            }
            let plan = $('#id_plan').val()
            if(!plan){
                alert("Please Select Plan ...")
                return
            }
            let duration = $('#id_duration').val()
            if(!duration){
                alert("Please Select Duration ...")
                return
            }
            let dataToSend = {
                'location_id':locationId,
                'joining_date': joining_date,
                'plan' : plan,
                'multiple' : duration,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            }
        
                // Clear the seat dropdown
            seatDropdown.empty();
            console.log(dataToSend,"hello for location")
            // Fetch seats associated with the selected location
            $.ajax({
                url: '/api/get_seats/',  // URL to fetch seats
                type: 'POST',  // Change the request method to POST
                data: dataToSend,
                success: function(data) {
                    console.log(data)
                    seat_data = data
                    seatDropdown.append('<option value="">Select</option>');
                    $("#id_total_amount_to_pay").val( parseInt(plan.split("_")[1])*parseInt(duration))
                    $.each(data, function(key,value) {
                        console.log(value,key)
                        seatDropdown.append('<option value="' + key + '">' + value[0] + '</option>');
                        // $("#id_seat").attr('disabled', 'disabled');
                        $("#id_seat").removeAttr('disabled');
                    });
                    calculateAmount()
                }
            });

        }
        $('#seat_finder').on('click',getSeats)

        
        console.log("javascript here")
        // $('#id_seat').on('change',
        onSelectChange(document.getElementById("select2-id_seat-container"),function() {
            // console.log("hello")
            console.log("hello")
            let seat_id =  $("#id_seat").val();
            if (seat_id) {
                        console.log(seat_data[seat_id][1])
                        hours =parseInt( $('#id_plan').val().split("_")[0])
                        availabletimming = getAvailableTimmig(seat_data[seat_id][1],hours)
                        updateStart(availabletimming)
                        end_Dropdown.empty();
                        end_Dropdown.append('<option value="">---------</option>');
                        $("#id_start_time").removeAttr('disabled');
                        $("#id_discount").removeAttr('disabled');
                        $("#id_total_amount_to_pay").removeAttr('disabled');
                    
                } else {
                        availabletimming = []
                        start_Dropdown.empty();
                        start_Dropdown.append('<option value="">---------</option>');

                        end_Dropdown.empty();
                        end_Dropdown.append('<option value="">---------</option>');
                    }
        })

        onSelectChange(document.getElementById("select2-id_start_time-container"),
            function(){
            console.log("hello clicked on id_start_time ");
            let timeAfter = parseInt($("#id_start_time").val());  // Get selected time
            let hours = parseInt($('#id_plan').val().split("_")[0]);
            console.log(hours)
            const t = parseInt(timeAfter) + parseInt(hours)
            if(timeAfter){
                end_Dropdown.empty();
                end_Dropdown.append(`<option value="${correctIt(t%24)}:00:00" selected> ${timeDescription(t%24)} </option>`);
            }
            console.log("disabled") 
        })

        $('#id_discount').val(0)
        $('#id_discount').on('keyup',function(){calculateAmount()});
        let totalAmountTOpay = 0
        function calculateAmount(){
            console.log("calculating total amount ......")

            let duration = $('#id_duration').val()
            if(!duration){
                alert("Please Select Duration ...")
                // just reload
            }
            slectedPrize = 0
            if($('#id_plan').val()){
                slectedPrize = parseFloat($('#id_plan').val().split("_")[1])
            }
            let discount = $('#id_discount').val()
            
            if(!discount){
                discount = 0
            }

            totalAmountTOpay = parseInt(duration) * slectedPrize *(100-parseInt(discount))/100
            console.log(totalAmountTOpay)
            $('#id_total_amount_to_pay').val(totalAmountTOpay)
        }


        function onSelectChange(targetNode,task){

            var observer = new MutationObserver(function(mutationsList, observer) {
                task()
            });
            var config = { childList: true, attributes: true, subtree: true }
    
            observer.observe(targetNode, config);
        }




        let total_amount_flag = true
        // $('#id_total_amount_to_pay').prop('disabled', total_amount_flag);
        $('#total_amount_type').on('click',function(){
            console.log("cliccked on totoamount type")
            total_amount_flag = !total_amount_flag
            $('#id_total_amount_to_pay').prop('disabled', total_amount_flag);
            if(total_amount_flag){
                $(this).text('Click to pay manual amount');
            }else{
                $(this).text('Click to pay custom amount');
            }
        })




        
        function getAvailableTimmig(timmings,selectedTime){
            console.log(timmings,selectedTime)
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
                forEndValueKeyTime[timeDescription(value%24)] = `${correctIt(value)}`
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
            $("#id_total_amount_to_pay").removeAttr('disabled');
            $("#id_end_time").removeAttr('disabled');
        });

        });    
        

})(django.jQuery);


