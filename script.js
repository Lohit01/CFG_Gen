document.getElementById('cfgForm').onsubmit = function() {
    const image = document.getElementById('cfgImage');
    image.style.display = 'none'; // Hide image initially
    image.src = ''; // Reset src
};

fetch('/path_to_your_generated_image') // Make sure to replace with the actual image path if needed
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const image = document.getElementById('cfgImage');
        image.src = url;
        image.style.display = 'block'; // Show image
    });
