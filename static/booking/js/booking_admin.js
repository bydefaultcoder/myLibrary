flag = true

setTimeout(() => {
    // console.log("hello")
    const script = document.createElement('script');
    script.src = '/static/booking/js/aslicode.js'; // Replace with the actual path to your script
    document.head.appendChild(script);
  }, 2000); // Load the script after a 2-second delay