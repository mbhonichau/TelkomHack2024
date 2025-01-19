// Run code and display output
document.getElementById("run").addEventListener("click", function() {
    let code = document.getElementById("codeInput").value;
    let outputDiv = document.getElementById("output");

    try {
        outputDiv.textContent = eval(code); // For running JavaScript code
    } catch (error) {
        outputDiv.textContent = 'Error: ' + error.message;
    }
});
