// Enhanced UI interactions and functionality
function fillPrompt(text) {
    document.getElementById('prompt').value = text;
    // Add subtle animation feedback
    const input = document.getElementById('prompt');
    input.style.transform = 'scale(1.02)';
    setTimeout(() => input.style.transform = 'scale(1)', 200);
}

function generateAnother() {
    document.getElementById('result').style.display = 'none';
    document.getElementById('prompt').value = '';
    document.getElementById('prompt').focus();
}

function downloadVideo() {
    const video = document.getElementById('generatedVideo');
    const videoSrc = video.src;
    
    // Create download with timestamp
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const link = document.createElement('a');
    link.href = videoSrc;
    link.download = `ai-video-${timestamp}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Show success feedback
    showNotification('Video downloaded successfully! 📥');
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

function startProgressAnimation() {
    const progress = document.querySelector('.progress');
    let width = 0;
    const interval = setInterval(() => {
        width += Math.random() * 15;
        if (width >= 90) {
            width = 90;
            clearInterval(interval);
        }
        progress.style.width = width + '%';
    }, 800);
    return interval;
}

// Enhanced form submission with better UX
document.getElementById('videoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const prompt = document.getElementById('prompt').value.trim();
    const generateBtn = document.getElementById('generateBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('loadingSpinner');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');
    
    // Input validation
    if (prompt.length < 3) {
        showNotification('Please enter a more descriptive prompt (at least 3 characters)');
        return;
    }
    
    // Reset UI state
    loading.style.display = 'block';
    result.style.display = 'none';
    error.style.display = 'none';
    
    // Button loading state
    generateBtn.disabled = true;
    btnText.textContent = 'Generating...';
    spinner.style.display = 'inline-block';
    
    // Start progress animation
    const progressInterval = startProgressAnimation();
    
    try {
        const formData = new FormData();
        formData.append('prompt', prompt);
        
        const response = await fetch('/generate-video', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || `HTTP ${response.status}`);
        }
        
        if (data.status === 'success') {
            // Complete progress bar
            document.querySelector('.progress').style.width = '100%';
            
            setTimeout(() => {
                const video = document.getElementById('generatedVideo');
                video.src = data.video_data;
                
                // Enhanced prompt display
                document.getElementById('enhancedPrompt').innerHTML = `
                    <div class="prompt-comparison">
                        <div class="prompt-section">
                            <strong>📝 Your Prompt:</strong>
                            <p>${data.original_prompt}</p>
                        </div>
                        <div class="prompt-section">
                            <strong>🚀 AI Enhanced:</strong>
                            <p>${data.enhanced_prompt}</p>
                        </div>
                        <div class="model-info">
                            <small>Generated using: ${data.model_used}</small>
                        </div>
                    </div>
                `;
                
                // Setup download button
                const downloadBtn = document.getElementById('downloadBtn');
                downloadBtn.onclick = downloadVideo;
                
                loading.style.display = 'none';
                result.style.display = 'block';
                
                showNotification('Video generated successfully! 🎉');
            }, 500);
            
        } else {
            throw new Error(data.detail || 'Unknown error occurred');
        }
        
    } catch (err) {
        console.error('Generation error:', err);
        
        loading.style.display = 'none';
        error.style.display = 'block';
        error.innerHTML = `
            <h4>⚠️ Generation Failed</h4>
            <p>${err.message}</p>
            <small>Please try again with a different prompt or check your connection.</small>
        `;
        
        showNotification('Generation failed. Please try again.');
        
    } finally {
        // Reset button state
        clearInterval(progressInterval);
        generateBtn.disabled = false;
        btnText.textContent = 'Generate Video';
        spinner.style.display = 'none';
        
        // Reset progress bar
        setTimeout(() => {
            document.querySelector('.progress').style.width = '0%';
        }, 1000);
    }
});

// Enhanced input experience
document.getElementById('prompt').addEventListener('input', function(e) {
    const charCount = e.target.value.length;
    const maxLength = 200;
    
    // Update character counter (if you want to add one)
    if (charCount > maxLength * 0.8) {
        e.target.style.borderColor = '#ff9800';
    } else {
        e.target.style.borderColor = '#ddd';
    }
});

// Auto-focus on prompt input when page loads
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('prompt').focus();
});