document.addEventListener("DOMContentLoaded", function() {
    // Get the button element
    const runButton = document.getElementsByClassName("run-button")[0];
    const stopButton = document.getElementsByClassName("stop-button")[0];


    // Add click event listener to the button
    runButton.addEventListener("click", function() {
        // Send a request to your Flask server when the button is clicked
        fetch("/button_click",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)})
            .then(response => response.json())
            .then(data => {
                // Handle the response from the server
                console.log(data);
            })
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
    });
    stopButton.addEventListener("click", function() {
        // Send a request to your Flask server when the button is clicked
        fetch("/button_end",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)})
            .then(response => response.json())
            .then(data => {
                // Handle the response from the server
                console.log(data);
            })
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
    });
});