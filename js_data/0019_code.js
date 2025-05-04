// Function to update the text content of the heading
function updatetext() {
    // Changing the text of the element with id "heading"
    document.getElementById("heading").innerHTML = "JavaScript is awesome!";
}

// New function that uses the Math library to generate a random number
function showRandomNumber() {
    // Generate a random number between 0 and 100
    let randomNumber = Math.floor(Math.random() * 101);

    // Display the random number in the heading
    document.getElementById("heading").innerHTML = "Random Number: " + randomNumber;
}
