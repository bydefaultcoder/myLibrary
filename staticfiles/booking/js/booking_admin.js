(function($) {
    console.log("hello")
    function printAllIds() {
        const allElements = document.querySelectorAll('*'); // Selects all elements in the DOM
      
        allElements.forEach(element => {
          if (element.id) { // Check if the element has an id
            console.log(element.id);
          }
        });
      }
      
      printAllIds();

})(django.jQuery);


