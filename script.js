function generateCertificate() {
    const nameInput = document.getElementById('nameInput').value;
    const canvas = document.getElementById('certificateCanvas');
    const context = canvas.getContext('2d');
    const downloadLink = document.getElementById('downloadLink');

    if (nameInput.trim() !== "") {
        canvas.width = 800;
        canvas.height = 600;
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Draw certificate background
        context.fillStyle = '#fff';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.strokeRect(0, 0, canvas.width, canvas.height);

        // Draw abstract shapes on the sides
        context.fillStyle = '#1e3a5f';
        context.beginPath();
        context.moveTo(0, 0);
        context.lineTo(100, 0);
        context.lineTo(0, 100);
        context.closePath();
        context.fill();

        context.fillStyle = '#4CAF50';
        context.beginPath();
        context.moveTo(800, 0);
        context.lineTo(700, 0);
        context.lineTo(800, 100);
        context.closePath();
        context.fill();

        context.fillStyle = '#1e3a5f';
        context.beginPath();
        context.moveTo(0, 600);
        context.lineTo(100, 600);
        context.lineTo(0, 500);
        context.closePath();
        context.fill();

        context.fillStyle = '#4CAF50';
        context.beginPath();
        context.moveTo(800, 600);
        context.lineTo(700, 600);
        context.lineTo(800, 500);
        context.closePath();
        context.fill();

        // Draw certificate text
        context.font = '30px Arial';
        context.textAlign = 'center';
        context.fillStyle = '#000';
        context.fillText('Certificate of Completion', canvas.width / 2, 100);
        context.font = '20px Arial';
        context.fillText('This is to certify that', canvas.width / 2, 200);
        context.font = '40px Arial';
        context.fillText(nameInput, canvas.width / 2, 300);
        context.font = '20px Arial';
        context.fillText('has successfully completed the course.', canvas.width / 2, 400);

        // Show the canvas and download link
        canvas.style.display = 'block';
        downloadLink.style.display = 'block';
        downloadLink.href = canvas.toDataURL('image/png');
        downloadLink.download = 'certificate.png';
        downloadLink.textContent = 'Download Certificate';
    } else {
        alert("Please enter your name.");
    }
}
