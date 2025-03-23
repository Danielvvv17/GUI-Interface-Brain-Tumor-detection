document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const imageContainer = document.getElementById('imageContainer');
    const uploadPrompt = document.getElementById('uploadPrompt');
    const previewImage = document.getElementById('previewImage');
    const markerCanvas = document.getElementById('markerCanvas');
    const processBtn = document.getElementById('processBtn');
    const markerBtn = document.getElementById('markerBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const processingTime = document.getElementById('processingTime');
    const resultContainer = document.getElementById('resultContainer');
    const resultText = document.getElementById('resultText');
    const feedbackSelect = document.getElementById('feedbackSelect');
    const submitFeedbackBtn = document.getElementById('submitFeedbackBtn');

    let isProcessing = false;
    let isMarkerActive = false;
    let markerPoints = [];
    let currentImage = null;

    // Handle file upload
    imageContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        imageContainer.classList.add('border-blue-500');
    });

    imageContainer.addEventListener('dragleave', () => {
        imageContainer.classList.remove('border-blue-500');
    });

    imageContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        imageContainer.classList.remove('border-blue-500');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageUpload(file);
        }
    });

    imageContainer.querySelector('button').addEventListener('click', () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                handleImageUpload(file);
            }
        };
        input.click();
    });

    function handleImageUpload(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            currentImage = new Image();
            currentImage.onload = () => {
                uploadPrompt.classList.add('hidden');
                previewImage.classList.remove('hidden');
                previewImage.src = e.target.result;
                
                // Enable buttons
                processBtn.disabled = false;
                markerBtn.disabled = false;
                deleteBtn.disabled = false;
                
                // Setup marker canvas
                markerCanvas.width = currentImage.width;
                markerCanvas.height = currentImage.height;
                markerCanvas.style.position = 'absolute';
                markerCanvas.style.top = previewImage.offsetTop + 'px';
                markerCanvas.style.left = previewImage.offsetLeft + 'px';
            };
            currentImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    // Process Image
    processBtn.addEventListener('click', () => {
        if (!currentImage || isProcessing) return;

        isProcessing = true;
        progressContainer.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        cancelBtn.disabled = false;
        processBtn.disabled = true;
        markerBtn.disabled = true;
        deleteBtn.disabled = true;

        let progress = 0;
        const processingInterval = setInterval(() => {
            progress += 1;
            progressBar.style.width = (progress * 20) + '%';
            processingTime.textContent = `Processing time: ${progress}s`;

            if (progress >= 5) {
                clearInterval(processingInterval);
                completeProcessing();
            }
        }, 1000);
    });

    function completeProcessing() {
        isProcessing = false;
        progressContainer.classList.add('hidden');
        resultContainer.classList.remove('hidden');
        cancelBtn.disabled = true;
        processBtn.disabled = false;
        markerBtn.disabled = false;
        deleteBtn.disabled = false;

        // Simulate random result (Tumor/No Tumor)
        const result = Math.random() > 0.5 ? 'Tumor' : 'No Tumor';
        resultText.textContent = result;
        resultText.className = result === 'Tumor' ? 'text-red-600 text-xl font-bold' : 'text-green-600 text-xl font-bold';
    }

    // Marker Tool
    markerBtn.addEventListener('click', () => {
        isMarkerActive = !isMarkerActive;
        markerBtn.classList.toggle('marker-active');
        markerCanvas.classList.toggle('hidden');
        
        if (isMarkerActive) {
            markerPoints = [];
            const ctx = markerCanvas.getContext('2d');
            ctx.clearRect(0, 0, markerCanvas.width, markerCanvas.height);
        }
    });

    markerCanvas.addEventListener('click', (e) => {
        if (!isMarkerActive) return;

        const rect = markerCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        markerPoints.push({ x, y });

        const ctx = markerCanvas.getContext('2d');
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fillStyle = 'red';
        ctx.fill();

        if (markerPoints.length > 1) {
            ctx.beginPath();
            ctx.moveTo(markerPoints[markerPoints.length - 2].x, markerPoints[markerPoints.length - 2].y);
            ctx.lineTo(x, y);
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
    });

    // Delete Image
    deleteBtn.addEventListener('click', () => {
        currentImage = null;
        uploadPrompt.classList.remove('hidden');
        previewImage.classList.add('hidden');
        markerCanvas.classList.add('hidden');
        previewImage.src = '';
        resultContainer.classList.add('hidden');
        progressContainer.classList.add('hidden');
        
        // Reset buttons
        processBtn.disabled = true;
        markerBtn.disabled = true;
        deleteBtn.disabled = true;
        cancelBtn.disabled = true;
        markerBtn.classList.remove('marker-active');
        
        // Clear marker
        isMarkerActive = false;
        markerPoints = [];
        const ctx = markerCanvas.getContext('2d');
        ctx.clearRect(0, 0, markerCanvas.width, markerCanvas.height);
    });

    // Cancel Processing
    cancelBtn.addEventListener('click', () => {
        if (!isProcessing) return;
        
        isProcessing = false;
        progressContainer.classList.add('hidden');
        cancelBtn.disabled = true;
        processBtn.disabled = false;
        markerBtn.disabled = false;
        deleteBtn.disabled = false;
        processingTime.textContent = 'Processing time: 0s';
        progressBar.style.width = '0%';
    });

    // Submit Feedback
    submitFeedbackBtn.addEventListener('click', () => {
        const feedback = feedbackSelect.value;
        if (!feedback) return;

        const currentResult = resultText.textContent;
        if (currentResult !== feedback) {
            // Simulate feedback storage
            console.log(`Feedback submitted: Original prediction: ${currentResult}, Corrected to: ${feedback}`);
            alert('Thank you for your feedback! The system will learn from this.');
        }
        feedbackSelect.value = '';
    });
});