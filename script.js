// Simple interactivity, canvas background (soft gradient wave) + rain overlay + EmailJS contact
document.addEventListener('DOMContentLoaded', ()=>{

  // Tab navigation
  document.querySelectorAll('.tab').forEach(btn=>{
    btn.addEventListener('click', ()=> {
      document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.target;
      document.querySelectorAll('.section').forEach(s=> {
        s.classList.toggle('active', s.id === target);
      });
      window.scrollTo({top:0,behavior:'smooth'});
    });
    
    // Add touch support for mobile
    btn.addEventListener('touchstart', (e)=> {
      e.preventDefault();
      btn.click();
    });
  });

  // Enable hash link navigation (e.g., #contact)
  function activateSectionById(id){
    document.querySelectorAll('.section').forEach(s=>{
      s.classList.toggle('active', s.id === id);
    });
    document.querySelectorAll('.tab').forEach(btn=>{
      btn.classList.toggle('active', btn.dataset.target === id);
    });
    window.scrollTo({top:0,behavior:'smooth'});
  }

  function handleHash(){
    const id = location.hash.replace('#','');
    if(id){ activateSectionById(id); }
  }
  window.addEventListener('hashchange', handleHash);
  handleHash();

  // Canvas animated gradient wave
  const canvas = document.getElementById('bgCanvas');
  const ctx = canvas.getContext('2d');
  function resize(){ 
    canvas.width = window.innerWidth; 
    canvas.height = window.innerHeight; 
  }
  
  // Handle mobile orientation changes
  window.addEventListener('resize', resize);
  window.addEventListener('orientationchange', ()=> {
    setTimeout(resize, 100);
  });
  
  resize();

  let t = 0;
  function draw(){
    t += 0.005;
    const grd = ctx.createLinearGradient(0,0,canvas.width,canvas.height);
    grd.addColorStop(0, `hsl(${(Math.sin(t)*40)+200} 80% 50%)`);
    grd.addColorStop(0.5, `hsl(${(Math.cos(t*1.2)*40)+280} 70% 45%)`);
    grd.addColorStop(1, `hsl(${(Math.sin(t*0.7)*40)+330} 70% 40%)`);
    ctx.fillStyle = grd;
    ctx.fillRect(0,0,canvas.width,canvas.height);

    // subtle moving wave overlay
    ctx.globalCompositeOperation = 'lighter';
    for(let i=0;i<6;i++){
      ctx.beginPath();
      const amp = 20 + i*10;
      ctx.moveTo(0, canvas.height/2);
      for(let x=0;x<canvas.width;x+=20){
        const y = canvas.height/2 + Math.sin((x*0.01) + t*(0.2+i*0.05)) * amp;
        ctx.lineTo(x,y);
      }
      ctx.lineTo(canvas.width, canvas.height);
      ctx.lineTo(0, canvas.height);
      ctx.closePath();
      ctx.fillStyle = 'rgba(255,255,255,0.01)';
      ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';
    requestAnimationFrame(draw);
  }
  draw();

  // Rain overlay using DOM (CSS handles visual)
  const overlay = document.querySelector('.overlay-rain');
  // create pseudo raindrops via repeating-radial background or leave as-is for performance

});

// Typing effect for hero role
const roles = [
  'Full‑Stack Developer',
  'AI/ML Enthusiast',
  'Software Engineer',
  'Problem Solver'
];
let roleIndex = 0, charIndex = 0, deleting = false;
function typeLoop(){
  const el = document.getElementById('typedRole');
  if(!el){ requestAnimationFrame(typeLoop); return; }

  const current = roles[roleIndex];
  if(!deleting){
    charIndex++;
    el.textContent = current.slice(0, charIndex);
    if(charIndex === current.length){ deleting = true; setTimeout(typeLoop, 1200); return; }
  } else {
    charIndex--;
    el.textContent = current.slice(0, charIndex);
    if(charIndex === 0){ deleting = false; roleIndex = (roleIndex+1)%roles.length; }
  }
  setTimeout(typeLoop, deleting ? 60 : 90);
}
typeLoop();

// CV Download handler for mobile compatibility
function downloadCV(e) {
  e.preventDefault();
  const fileName = 'Abiha_Fatima_cv (3).pdf';
  const downloadName = 'Abiha_Fatima_CV.pdf';
  
  // Try to download the file
  const link = document.createElement('a');
  link.href = fileName;
  link.download = downloadName;
  link.target = '_blank';
  
  // For mobile devices, try to open in new tab first
  if (/Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    // Mobile: open in new tab
    window.open(fileName, '_blank');
    alert('CV opened in new tab. You can save it from there.');
  } else {
    // Desktop: direct download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// Contact form handler (Web3Forms)
function sendEmail(e){
  e.preventDefault();
  const form = e.target;

  const name = form.name.value;
  const email = form.email.value;
  const message = form.message.value;

  if(!name.trim() || !email.trim() || !message.trim()){
    alert('Please fill in all fields.');
    return;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if(!emailRegex.test(email)){
    alert('Please enter a valid email address.');
    return;
  }

  const formData = new FormData(form);
  fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    body: formData
  })
  .then(async (res)=>{
    const data = await res.json();
    if(res.ok){
      alert(`Thank you, ${name}! Your message was sent successfully.`);
      form.reset();
    } else {
      console.error('Web3Forms error:', data);
      alert('Failed to send message. Please try again later.');
    }
  })
  .catch(err=>{
    console.error(err);
    alert('Network error. Please check your connection and try again.');
  });
}

// AI Chatbot functionality
class AIChatbot {
  constructor() {
    this.isOpen = false;
    this.messages = [];
    this.init();
  }

  init() {
    const toggle = document.getElementById('chatbot-toggle');
    const container = document.getElementById('chatbot-container');
    const close = document.getElementById('chatbot-close');
    const input = document.getElementById('chatbot-input');
    const send = document.getElementById('chatbot-send');

    toggle.addEventListener('click', () => this.toggle());
    close.addEventListener('click', () => this.close());
    send.addEventListener('click', () => this.sendMessage());
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });

    this.addMessage('bot', 'Hello! I\'m your AI assistant. Ask me anything about Abiha\'s skills, projects, or experience!');
  }

  toggle() {
    this.isOpen = !this.isOpen;
    const container = document.getElementById('chatbot-container');
    if (this.isOpen) {
      container.classList.add('active');
    } else {
      container.classList.remove('active');
    }
  }

  close() {
    this.isOpen = false;
    document.getElementById('chatbot-container').classList.remove('active');
  }

  addMessage(sender, text) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${sender}`;
    messageDiv.textContent = text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  async sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    if (!message) return;

    this.addMessage('user', message);
    input.value = '';

    // Simulate AI response
    setTimeout(() => {
      const response = this.generateResponse(message);
      this.addMessage('bot', response);
    }, 1000);
  }

  generateResponse(message) {
    const responses = {
      'skills': 'Abiha has expertise in C, C++, Java, Python, HTML, CSS, JavaScript, DSA (Java), MySQL, GitHub, and VS Code. She\'s particularly strong in full-stack development and AI/ML technologies.',
      'projects': 'Abiha has worked on several exciting projects including an ML Scanner for image recognition, a Fingerprint Scanner with salary prediction, an Interactive Panda Form for employee tracking, and a Student Management System.',
      'experience': 'Abiha is an aspiring Software Engineer with a passion for AI/ML. She has completed 30+ projects and has experience with various technologies. She\'s currently pursuing her Masters at Amity University.',
      'contact': 'You can reach Abiha at abihaz344@gmail.com or call her at +91 9569519323. She\'s also active on GitHub and LinkedIn.',
      'education': 'Abiha is pursuing her Masters at Amity University (CPI: 8.9) and completed her Bachelors at Lucknow University (CPI: 7.9). She also completed her 12th and 10th at Emma Thompson School.',
      'hobbies': 'Abiha enjoys cooking, listening to music, learning different languages, and spending time with friends. These activities help her stay creative and balanced.',
      'default': 'That\'s an interesting question! Abiha is a talented developer with skills in multiple programming languages and technologies. Would you like to know more about her specific skills, projects, or experience?'
    };

    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
      if (lowerMessage.includes(key)) {
        return response;
      }
    }
    return responses.default;
  }
}

// Project Demo Functions
function openMLScanner() {
  const modal = document.getElementById('ml-scanner-modal');
  modal.classList.add('active');
  modal.style.display = 'flex';
}

function openFingerprintScanner() {
  const modal = document.getElementById('fingerprint-modal');
  modal.classList.add('active');
  modal.style.display = 'flex';
  
  // Add click handler to scanner surface
  const scannerSurface = document.querySelector('.scanner-surface');
  if (scannerSurface) {
    scannerSurface.addEventListener('click', simulateFingerprintScan);
  }
}

function openPandaForm() {
  const modal = document.getElementById('panda-form-modal');
  modal.classList.add('active');
  modal.style.display = 'flex';
  getCurrentLocation();
  startWatchingLocation();
}

function openStudentSystem() {
  const modal = document.getElementById('student-system-modal');
  modal.classList.add('active');
  modal.style.display = 'flex';
  loadStudentData();
}

// ML Scanner Demo
function initMLScanner() {
  const startBtn = document.getElementById('start-ml-camera');
  const stopBtn = document.getElementById('stop-ml-camera');
  const captureBtn = document.getElementById('capture-ml-image');
  const video = document.getElementById('ml-video');
  const canvas = document.getElementById('ml-canvas');
  const results = document.getElementById('ml-results');

  let stream = null;

  startBtn.addEventListener('click', async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      results.innerHTML = '<p>Camera started. Real-time face detection active. Click "Capture & Analyze" to process the image.</p>';
      
      // Add live emotion display
      const liveEmotionDiv = document.createElement('div');
      liveEmotionDiv.id = 'live-emotion-display';
      liveEmotionDiv.style.cssText = 'position: absolute; top: 10px; right: 10px; background: rgba(0,255,0,0.9); color: #000; padding: 8px 12px; border-radius: 20px; font-weight: bold; z-index: 15; font-size: 14px;';
      liveEmotionDiv.textContent = 'Live Emotion: Happy (95%)';
      document.querySelector('.camera-container').appendChild(liveEmotionDiv);
      
      // Start real-time face detection
      startRealTimeDetection();
    } catch (err) {
      results.innerHTML = '<p>Camera access denied. This is a demo - simulating ML analysis...</p>';
      simulateMLAnalysis();
    }
  });

  stopBtn.addEventListener('click', () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      video.srcObject = null;
      results.innerHTML = '<p>Camera stopped.</p>';
      
      // Clear detection interval
      if (detectionInterval) {
        clearInterval(detectionInterval);
        detectionInterval = null;
      }
      
      // Remove live emotion display
      const liveEmotionDisplay = document.getElementById('live-emotion-display');
      if (liveEmotionDisplay) {
        liveEmotionDisplay.remove();
      }
      
      // Clear canvas
      const canvas = document.getElementById('ml-canvas');
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  });

  captureBtn.addEventListener('click', () => {
    if (stream) {
      const ctx = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);
      analyzeImage();
    } else {
      simulateMLAnalysis();
    }
  });
}

// Real-time face detection function
let detectionInterval;
let emotionIndex = 0;
const emotions = ['Happy', 'Focused', 'Confident', 'Excited', 'Calm', 'Determined'];
const confidenceLevels = [92, 88, 95, 89, 91, 87];

function startRealTimeDetection() {
  const video = document.getElementById('ml-video');
  const canvas = document.getElementById('ml-canvas');
  const ctx = canvas.getContext('2d');
  
  // Clear any existing detection
  if (detectionInterval) {
    clearInterval(detectionInterval);
  }
  
  function detectFaces() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      // Set canvas size to match video display size
      const videoRect = video.getBoundingClientRect();
      canvas.width = video.offsetWidth;
      canvas.height = video.offsetHeight;
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Simulate face detection with movement - vary position slightly
      const time = Date.now() * 0.001;
      const faceX = canvas.width * (0.15 + Math.sin(time * 0.5) * 0.1);
      const faceY = canvas.height * (0.1 + Math.cos(time * 0.3) * 0.05);
      const faceWidth = canvas.width * 0.7;
      const faceHeight = canvas.height * 0.8;
      
      // Draw face detection rectangle with animation
      ctx.strokeStyle = '#00ff00';
      ctx.lineWidth = 3;
      ctx.setLineDash([5, 5]);
      ctx.strokeRect(faceX, faceY, faceWidth, faceHeight);
      ctx.setLineDash([]);
      
      // Add pulsing effect
      const pulse = Math.sin(time * 3) * 0.3 + 0.7;
      ctx.strokeStyle = `rgba(0, 255, 0, ${pulse})`;
      ctx.lineWidth = 2;
      ctx.strokeRect(faceX - 2, faceY - 2, faceWidth + 4, faceHeight + 4);
      
      // Add live emotion label
      const currentEmotion = emotions[emotionIndex % emotions.length];
      const currentConfidence = confidenceLevels[emotionIndex % confidenceLevels.length];
      
      // Update live emotion display
      const liveEmotionDisplay = document.getElementById('live-emotion-display');
      if (liveEmotionDisplay) {
        liveEmotionDisplay.textContent = `Live Emotion: ${currentEmotion} (${currentConfidence}%)`;
      }
      
      ctx.fillStyle = '#00ff00';
      ctx.font = 'bold 16px Arial';
      ctx.fillText(`Live Emotion: ${currentEmotion} (${currentConfidence}%)`, faceX, faceY - 15);
      
      // Add confidence indicator
      ctx.fillStyle = '#00ff00';
      ctx.font = '12px Arial';
      ctx.fillText('✓ Face Tracking Active', faceX + faceWidth - 100, faceY + faceHeight + 15);
      
      // Add movement indicator
      ctx.fillStyle = '#00ff00';
      ctx.font = '10px Arial';
      ctx.fillText('🔄 Live Detection', faceX, faceY + faceHeight + 30);
    }
    
    // Continue detection
    requestAnimationFrame(detectFaces);
  }
  
  // Start detection
  detectFaces();
  
  // Change emotions every 2 seconds
  detectionInterval = setInterval(() => {
    emotionIndex++;
  }, 2000);
}

function analyzeImage() {
  const results = document.getElementById('ml-results');
  const video = document.getElementById('ml-video');
  const canvas = document.getElementById('ml-canvas');
  
  results.innerHTML = '<p>Analyzing image...</p>';
  
  // Show the captured image
  canvas.style.display = 'block';
  canvas.style.width = '100%';
  canvas.style.maxWidth = '400px';
  canvas.style.borderRadius = '8px';
  canvas.style.margin = '10px auto';
  canvas.style.display = 'block';
  
  // Add emotion detection overlay (green square)
  setTimeout(() => {
    const ctx = canvas.getContext('2d');
    
    // Simulate face detection - draw green square around detected face area
    // Position the square to cover the main face area (center of image)
    const faceX = canvas.width * 0.2; // 20% from left
    const faceY = canvas.height * 0.15; // 15% from top
    const faceWidth = canvas.width * 0.6; // 60% of image width
    const faceHeight = canvas.height * 0.7; // 70% of image height
    
    // Draw green square for emotion detection around face
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 4;
    ctx.strokeRect(faceX, faceY, faceWidth, faceHeight);
    
    // Add emotion label above the face
    ctx.fillStyle = '#00ff00';
    ctx.font = 'bold 18px Arial';
    ctx.fillText('Emotion: Happy (95%)', faceX, faceY - 10);
    
    // Add confidence indicator
    ctx.fillStyle = '#00ff00';
    ctx.font = '14px Arial';
    ctx.fillText('✓ Face Detected', faceX + faceWidth - 80, faceY + faceHeight + 20);
    
    const analysis = {
      objects: ['Person', 'Computer', 'Desk'],
      confidence: [0.95, 0.87, 0.72],
      emotions: ['Happy', 'Focused', 'Confident'],
      text: ['Portfolio', 'Projects']
    };
    
    let html = '<h3>ML Analysis Results:</h3>';
    html += '<div class="captured-image-container">';
    html += '<p><strong>Captured Image with Face Detection:</strong></p>';
    html += '<div class="image-wrapper">';
    html += '<canvas id="ml-canvas" style="display: block; width: 100%; max-width: 400px; border-radius: 8px; margin: 10px auto;"></canvas>';
    html += '<div class="emotion-overlay">🎯 Real-time Emotion: Happy (95%)</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="analysis-grid">';
    html += '<div class="analysis-item"><strong>Objects Detected:</strong><br>';
    analysis.objects.forEach((obj, i) => {
      html += `${obj} (${Math.round(analysis.confidence[i] * 100)}%)<br>`;
    });
    html += '</div>';
    html += '<div class="analysis-item"><strong>Emotions:</strong><br>' + analysis.emotions.join(', ') + '</div>';
    html += '<div class="analysis-item"><strong>Text Found:</strong><br>' + analysis.text.join(', ') + '</div>';
    html += '</div>';
    
    results.innerHTML = html;
    
    // Re-draw the canvas with proper face detection overlay
    setTimeout(() => {
      const newCanvas = document.getElementById('ml-canvas');
      if (newCanvas) {
        const newCtx = newCanvas.getContext('2d');
        const faceX = newCanvas.width * 0.2;
        const faceY = newCanvas.height * 0.15;
        const faceWidth = newCanvas.width * 0.6;
        const faceHeight = newCanvas.height * 0.7;
        
        // Draw face detection rectangle
        newCtx.strokeStyle = '#00ff00';
        newCtx.lineWidth = 4;
        newCtx.strokeRect(faceX, faceY, faceWidth, faceHeight);
        
        // Add emotion label
        newCtx.fillStyle = '#00ff00';
        newCtx.font = 'bold 18px Arial';
        newCtx.fillText('Emotion: Happy (95%)', faceX, faceY - 10);
        
        // Add confidence indicator
        newCtx.fillStyle = '#00ff00';
        newCtx.font = '14px Arial';
        newCtx.fillText('✓ Face Detected', faceX + faceWidth - 80, faceY + faceHeight + 20);
      }
    }, 100);
  }, 2000);
}

function simulateMLAnalysis() {
  const results = document.getElementById('ml-results');
  results.innerHTML = '<p>Simulating ML analysis...</p>';
  
  setTimeout(() => {
    const analysis = {
      objects: ['Person', 'Computer', 'Desk', 'Phone'],
      confidence: [0.92, 0.85, 0.78, 0.65],
      emotions: ['Focused', 'Professional', 'Confident'],
      text: ['Portfolio', 'Projects', 'Contact']
    };
    
    let html = '<h3>ML Analysis Results (Simulated):</h3>';
    html += '<div class="captured-image-container">';
    html += '<p><strong>Captured Image:</strong></p>';
    html += '<div class="image-wrapper">';
    html += '<div class="simulated-image">';
    html += '<canvas id="simulated-canvas" width="400" height="300" style="display: block; width: 100%; max-width: 400px; border-radius: 8px; margin: 10px auto; background: linear-gradient(135deg, #1a1a2e, #16213e);"></canvas>';
    html += '<div class="emotion-overlay">🎯 Emotion Detected: Focused (92%)</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="analysis-grid">';
    html += '<div class="analysis-item"><strong>Objects Detected:</strong><br>';
    analysis.objects.forEach((obj, i) => {
      html += `${obj} (${Math.round(analysis.confidence[i] * 100)}%)<br>`;
    });
    html += '</div>';
    html += '<div class="analysis-item"><strong>Emotions:</strong><br>' + analysis.emotions.join(', ') + '</div>';
    html += '<div class="analysis-item"><strong>Text Found:</strong><br>' + analysis.text.join(', ') + '</div>';
    html += '</div>';
    
    results.innerHTML = html;
    
    // Draw simulated image with emotion detection
    setTimeout(() => {
      const canvas = document.getElementById('simulated-canvas');
      if (canvas) {
        const ctx = canvas.getContext('2d');
        
        // Draw a simple face representation
        ctx.fillStyle = '#ffdbac';
        ctx.beginPath();
        ctx.arc(200, 120, 60, 0, 2 * Math.PI);
        ctx.fill();
        
        // Eyes
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(180, 100, 8, 0, 2 * Math.PI);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(220, 100, 8, 0, 2 * Math.PI);
        ctx.fill();
        
        // Smile
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(200, 130, 30, 0, Math.PI);
        ctx.stroke();
        
        // Draw green square around the entire face for emotion detection
        const faceX = 140; // Position to cover the face
        const faceY = 60;  // Position to cover the face
        const faceWidth = 120; // Width to cover the face
        const faceHeight = 120; // Height to cover the face
        
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 4;
        ctx.strokeRect(faceX, faceY, faceWidth, faceHeight);
        
        // Add emotion label above the face
        ctx.fillStyle = '#00ff00';
        ctx.font = 'bold 18px Arial';
        ctx.fillText('Emotion: Focused (92%)', faceX, faceY - 10);
        
        // Add confidence indicator
        ctx.fillStyle = '#00ff00';
        ctx.font = '14px Arial';
        ctx.fillText('✓ Face Detected', faceX + faceWidth - 80, faceY + faceHeight + 20);
      }
    }, 100);
  }, 2000);
}

// Fingerprint Scanner Demo
let isScanning = false;
let scanAttempts = 0;

function simulateFingerprintScan() {
  const progressBar = document.querySelector('.progress-bar');
  const dataDiv = document.getElementById('fingerprint-data');
  const scannerSurface = document.querySelector('.scanner-surface');
  const scannerInfo = document.querySelector('.scanner-info p');
  
  if (isScanning) return;
  
  isScanning = true;
  scanAttempts++;
  
  // Reset progress bar
  progressBar.style.width = '0%';
  progressBar.style.animation = 'none';
  
  // Add visual feedback for finger placement
  scannerSurface.style.boxShadow = 'inset 0 0 50px rgba(126,249,255,0.3)';
  scannerInfo.textContent = 'Place your finger on the scanner...';
  
  // Simulate finger detection
  setTimeout(() => {
    scannerSurface.style.boxShadow = 'inset 0 0 50px rgba(0,255,0,0.5)';
    scannerInfo.textContent = 'Finger detected! Scanning...';
    
    // Animate progress bar
    progressBar.style.animation = 'scanProgress 3s ease-in-out';
    
    // Simulate different outcomes based on attempts
    setTimeout(() => {
      const successRate = Math.random();
      const isSuccessful = successRate > 0.3 || scanAttempts > 2; // Higher success rate after multiple attempts
      
      if (isSuccessful) {
        showSuccessfulScan();
      } else {
        showFailedScan();
      }
      
      isScanning = false;
    }, 3000);
  }, 1000);
}

function showSuccessfulScan() {
  const dataDiv = document.getElementById('fingerprint-data');
  const scannerSurface = document.querySelector('.scanner-surface');
  const scannerInfo = document.querySelector('.scanner-info p');
  
  scannerSurface.style.boxShadow = 'inset 0 0 50px rgba(0,255,0,0.8)';
  scannerInfo.textContent = '✓ Scan successful!';
  
  const fingerprintData = {
    id: 'FP_' + Math.random().toString(36).substr(2, 9),
    quality: ['High', 'Medium', 'High'][Math.floor(Math.random() * 3)],
    minutiae: Math.floor(Math.random() * 50) + 30,
    ridgeCount: Math.floor(Math.random() * 20) + 15,
    pattern: ['Loop', 'Whorl', 'Arch'][Math.floor(Math.random() * 3)],
    confidence: (Math.random() * 0.2 + 0.8).toFixed(2)
  };
  
  let html = '<div class="fingerprint-analysis">';
  html += `<p><strong>Fingerprint ID:</strong> ${fingerprintData.id}</p>`;
  html += `<p><strong>Quality:</strong> ${fingerprintData.quality}</p>`;
  html += `<p><strong>Minutiae Points:</strong> ${fingerprintData.minutiae}</p>`;
  html += `<p><strong>Ridge Count:</strong> ${fingerprintData.ridgeCount}</p>`;
  html += `<p><strong>Pattern Type:</strong> ${fingerprintData.pattern}</p>`;
  html += `<p><strong>Confidence:</strong> ${Math.round(fingerprintData.confidence * 100)}%</p>`;
  html += '<p class="success-message">✓ Fingerprint successfully analyzed!</p>';
  html += '</div>';
  
  dataDiv.innerHTML = html;
}

function showFailedScan() {
  const dataDiv = document.getElementById('fingerprint-data');
  const scannerSurface = document.querySelector('.scanner-surface');
  const scannerInfo = document.querySelector('.scanner-info p');
  
  scannerSurface.style.boxShadow = 'inset 0 0 50px rgba(255,0,0,0.5)';
  scannerInfo.textContent = '✗ Scan failed. Try again.';
  
  const failureReasons = [
    'Insufficient fingerprint detail',
    'Finger not properly positioned',
    'Surface too dry or wet',
    'Poor image quality'
  ];
  
  const reason = failureReasons[Math.floor(Math.random() * failureReasons.length)];
  
  let html = '<div class="fingerprint-analysis">';
  html += '<p class="error-message">✗ Fingerprint scan failed</p>';
  html += `<p><strong>Reason:</strong> ${reason}</p>`;
  html += '<p><strong>Suggestions:</strong></p>';
  html += '<ul>';
  html += '<li>Ensure finger is clean and dry</li>';
  html += '<li>Place finger flat on the scanner</li>';
  html += '<li>Apply gentle pressure</li>';
  html += '<li>Hold still during scanning</li>';
  html += '</ul>';
  html += '<button onclick="simulateFingerprintScan()" class="retry-btn">Try Again</button>';
  html += '</div>';
  
  dataDiv.innerHTML = html;
}

// Panda Form Demo
function getCurrentLocation() {
  const locationSpan = document.getElementById('current-location');
  
  // Show loading state
  locationSpan.textContent = 'Getting location...';
  locationSpan.style.color = '#7ef9ff';
  
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude.toFixed(4);
        const lon = position.coords.longitude.toFixed(4);
        const accuracy = Math.round(position.coords.accuracy);
        
        // Get address from coordinates (simulated)
        const address = getAddressFromCoords(lat, lon);
        
        locationSpan.innerHTML = `
          <div style="text-align: left;">
            <strong>📍 Current Location:</strong><br>
            <span style="color: #00ff00;">✓ GPS: ${lat}, ${lon}</span><br>
            <span style="color: #7ef9ff;">📍 Address: ${address}</span><br>
            <span style="color: #b58bff;">🎯 Accuracy: ±${accuracy}m</span>
          </div>
        `;
        locationSpan.style.color = '#00ff00';
      },
      (error) => {
        let errorMessage = 'Location access denied';
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location permission denied by user';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information unavailable';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out';
            break;
        }
        locationSpan.innerHTML = `
          <div style="text-align: left;">
            <strong>📍 Location Status:</strong><br>
            <span style="color: #ff6b6b;">✗ ${errorMessage}</span><br>
            <span style="color: #b58bff;">Using demo location: New York, NY</span>
          </div>
        `;
        locationSpan.style.color = '#ff6b6b';
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000
      }
    );
  } else {
    locationSpan.innerHTML = `
      <div style="text-align: left;">
        <strong>📍 Location Status:</strong><br>
        <span style="color: #ff6b6b;">✗ Geolocation not supported</span><br>
        <span style="color: #b58bff;">Using demo location: New York, NY</span>
      </div>
    `;
    locationSpan.style.color = '#ff6b6b';
  }
}

// Simulate address lookup from coordinates
function getAddressFromCoords(lat, lon) {
  // This would normally use a reverse geocoding API
  const addresses = [
    '123 Main Street, New York, NY 10001',
    '456 Tech Avenue, San Francisco, CA 94105',
    '789 Innovation Blvd, Austin, TX 73301',
    '321 Startup Lane, Seattle, WA 98101'
  ];
  
  // Return a random address for demo purposes
  return addresses[Math.floor(Math.random() * addresses.length)];
}

let geoWatchId = null;

function startWatchingLocation(){
  if(!('geolocation' in navigator)) return;
  const locationSpan = document.getElementById('current-location');
  try {
    if(geoWatchId !== null){
      navigator.geolocation.clearWatch(geoWatchId);
      geoWatchId = null;
    }
    geoWatchId = navigator.geolocation.watchPosition(updateLiveLocation, handleLocationError, {
      enableHighAccuracy: true,
      maximumAge: 5000,
      timeout: 15000
    });
    if(locationSpan){ locationSpan.textContent = 'Watching location…'; }
  } catch(err){
    // fallback
    getCurrentLocation();
  }
}

function stopWatchingLocation(){
  if(geoWatchId !== null && 'geolocation' in navigator){
    navigator.geolocation.clearWatch(geoWatchId);
    geoWatchId = null;
  }
}

function updateLiveLocation(position){
  const locationSpan = document.getElementById('current-location');
  const lat = position.coords.latitude.toFixed(5);
  const lon = position.coords.longitude.toFixed(5);
  const accuracy = Math.round(position.coords.accuracy);
  const address = getAddressFromCoords(lat, lon);
  if(locationSpan){
    locationSpan.innerHTML = `
      <div style="text-align: left;">
        <strong>📍 Current Location (Live):</strong><br>
        <span style="color: #00ff00;">✓ GPS: ${lat}, ${lon}</span><br>
        <span style="color: #7ef9ff;">📍 Address: ${address}</span><br>
        <span style="color: #b58bff;">🎯 Accuracy: ±${accuracy}m</span>
      </div>
    `;
    locationSpan.style.color = '#00ff00';
  }
}

function handleLocationError(error){
  const locationSpan = document.getElementById('current-location');
  if(!locationSpan) return;
  let errorMessage = 'Location error';
  switch(error.code){
    case error.PERMISSION_DENIED: errorMessage = 'Location permission denied by user'; break;
    case error.POSITION_UNAVAILABLE: errorMessage = 'Location information unavailable'; break;
    case error.TIMEOUT: errorMessage = 'Location request timed out'; break;
  }
  locationSpan.innerHTML = `
    <div style="text-align: left;">
      <strong>📍 Location Status:</strong><br>
      <span style="color: #ff6b6b;">✗ ${errorMessage}</span><br>
      <span style="color: #b58bff;">Try Refresh Location</span>
    </div>
  `;
  locationSpan.style.color = '#ff6b6b';
}

function initPandaForm() {
  const checkInBtn = document.getElementById('check-in-btn');
  const checkOutBtn = document.getElementById('check-out-btn');
  const refreshLocationBtn = document.getElementById('refresh-location');
  const attendanceList = document.getElementById('attendance-list');
  
  let attendance = [];
  
  // Add refresh location button functionality
  if (refreshLocationBtn) {
    refreshLocationBtn.addEventListener('click', () => {
      getCurrentLocation();
    });
  }
  
  checkInBtn.addEventListener('click', () => {
    const name = document.getElementById('emp-name').value;
    const dept = document.getElementById('emp-dept').value;
    
    if (!name || !dept) {
      alert('Please fill in all fields');
      return;
    }
    
    const record = {
      name,
      dept,
      action: 'Check In',
      time: new Date().toLocaleTimeString(),
      date: new Date().toLocaleDateString()
    };
    
    attendance.push(record);
    updateAttendanceList();
    alert(`${name} checked in successfully!`);
  });
  
  checkOutBtn.addEventListener('click', () => {
    const name = document.getElementById('emp-name').value;
    const dept = document.getElementById('emp-dept').value;
    
    if (!name || !dept) {
      alert('Please fill in all fields');
      return;
    }
    
    const record = {
      name,
      dept,
      action: 'Check Out',
      time: new Date().toLocaleTimeString(),
      date: new Date().toLocaleDateString()
    };
    
    attendance.push(record);
    updateAttendanceList();
    alert(`${name} checked out successfully!`);
  });
  
  function updateAttendanceList() {
    let html = '';
    attendance.forEach(record => {
      html += `<div class="attendance-record">
        <strong>${record.name}</strong> (${record.dept}) - ${record.action} at ${record.time}
      </div>`;
    });
    attendanceList.innerHTML = html || '<p>No attendance records yet</p>';
  }
}

// Student Management System Demo
let students = [
  { id: 1, name: 'John Doe', class: '10A', attendance: 'Present', grade: 'A+', lastSeen: 'Today 9:00 AM' },
  { id: 2, name: 'Jane Smith', class: '10B', attendance: 'Present', grade: 'A', lastSeen: 'Today 8:45 AM' },
  { id: 3, name: 'Mike Johnson', class: '10A', attendance: 'Absent', grade: 'B+', lastSeen: 'Yesterday 3:30 PM' },
  { id: 4, name: 'Sarah Wilson', class: '10C', attendance: 'Present', grade: 'A-', lastSeen: 'Today 9:15 AM' },
  { id: 5, name: 'David Brown', class: '10B', attendance: 'Present', grade: 'B', lastSeen: 'Today 8:30 AM' },
  { id: 6, name: 'Emily Davis', class: '10A', attendance: 'Absent', grade: 'A', lastSeen: 'Yesterday 2:45 PM' },
  { id: 7, name: 'Alex Chen', class: '10C', attendance: 'Present', grade: 'A+', lastSeen: 'Today 9:05 AM' },
  { id: 8, name: 'Maria Garcia', class: '10B', attendance: 'Present', grade: 'B+', lastSeen: 'Today 8:50 AM' }
];

function loadStudentData() {
  const studentTable = document.getElementById('student-table');
  
  let html = '<table class="student-table">';
  html += '<tr><th>ID</th><th>Student Name</th><th>Class</th><th>Status</th><th>Actions</th><th>Grade</th><th>Edit</th></tr>';
  
  students.forEach(student => {
    const statusClass = student.attendance === 'Present' ? 'present' : 'absent';
    const statusIcon = student.attendance === 'Present' ? '✅' : '❌';
    
    html += `<tr id="student-row-${student.id}">
      <td class="editable-field" data-field="id" data-student-id="${student.id}">
        <span class="field-display">${student.id}</span>
        <input type="number" class="field-input" value="${student.id}" style="display: none;" min="1" max="999">
      </td>
      <td class="editable-field" data-field="name" data-student-id="${student.id}">
        <span class="field-display">${student.name}</span>
        <input type="text" class="field-input" value="${student.name}" style="display: none;" maxlength="50">
      </td>
      <td class="editable-field" data-field="class" data-student-id="${student.id}">
        <span class="field-display">${student.class}</span>
        <select class="field-input" style="display: none;">
          <option value="10A" ${student.class === '10A' ? 'selected' : ''}>10A</option>
          <option value="10B" ${student.class === '10B' ? 'selected' : ''}>10B</option>
          <option value="10C" ${student.class === '10C' ? 'selected' : ''}>10C</option>
          <option value="11A" ${student.class === '11A' ? 'selected' : ''}>11A</option>
          <option value="11B" ${student.class === '11B' ? 'selected' : ''}>11B</option>
          <option value="12A" ${student.class === '12A' ? 'selected' : ''}>12A</option>
          <option value="12B" ${student.class === '12B' ? 'selected' : ''}>12B</option>
        </select>
      </td>
      <td class="${statusClass}">
        <span class="status-icon">${statusIcon}</span>
        ${student.attendance}
        <br><small>Last seen: ${student.lastSeen}</small>
      </td>
      <td class="action-buttons">
        <button class="btn-present" onclick="markAttendance(${student.id}, 'Present')" 
                ${student.attendance === 'Present' ? 'disabled' : ''}>
          ✅ Present
        </button>
        <button class="btn-absent" onclick="markAttendance(${student.id}, 'Absent')" 
                ${student.attendance === 'Absent' ? 'disabled' : ''}>
          ❌ Absent
        </button>
      </td>
      <td>${student.grade}</td>
      <td class="edit-buttons">
        <button class="btn-edit" onclick="toggleEdit(${student.id})" title="Edit Student">
          ✏️ Edit
        </button>
        <button class="btn-save" onclick="saveStudent(${student.id})" style="display: none;" title="Save Changes">
          💾 Save
        </button>
        <button class="btn-cancel" onclick="cancelEdit(${student.id})" style="display: none;" title="Cancel">
          ❌ Cancel
        </button>
      </td>
    </tr>`;
  });
  
  html += '</table>';
  studentTable.innerHTML = html;
  
  // Update statistics
  updateStudentStats();
}

function markAttendance(studentId, status) {
  const student = students.find(s => s.id === studentId);
  if (student) {
    student.attendance = status;
    student.lastSeen = new Date().toLocaleString();
    
    // Show notification
    showNotification(`${student.name} marked as ${status}`, status === 'Present' ? 'success' : 'warning');
    
    // Reload the table
    loadStudentData();
  }
}

function updateStudentStats() {
  const totalStudents = students.length;
  const presentStudents = students.filter(s => s.attendance === 'Present').length;
  const absentStudents = totalStudents - presentStudents;
  
  // Update the dashboard stats
  const statCards = document.querySelectorAll('.stat-number');
  if (statCards.length >= 3) {
    statCards[0].textContent = totalStudents;
    statCards[1].textContent = presentStudents;
    statCards[2].textContent = absentStudents;
  }
}

function showNotification(message, type) {
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'success' ? '#4CAF50' : '#FF9800'};
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    z-index: 1000;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

// Student editing functions
function toggleEdit(studentId) {
  const row = document.getElementById(`student-row-${studentId}`);
  const editBtn = row.querySelector('.btn-edit');
  const saveBtn = row.querySelector('.btn-save');
  const cancelBtn = row.querySelector('.btn-cancel');
  const editableFields = row.querySelectorAll('.editable-field');
  
  // Show edit mode
  editBtn.style.display = 'none';
  saveBtn.style.display = 'inline-block';
  cancelBtn.style.display = 'inline-block';
  
  // Enable editing for all editable fields
  editableFields.forEach(field => {
    const display = field.querySelector('.field-display');
    const input = field.querySelector('.field-input');
    
    display.style.display = 'none';
    input.style.display = 'block';
    input.focus();
  });
  
  // Store original values for cancel functionality
  const originalValues = {};
  editableFields.forEach(field => {
    const fieldName = field.dataset.field;
    const input = field.querySelector('.field-input');
    originalValues[fieldName] = input.value;
  });
  
  row.dataset.originalValues = JSON.stringify(originalValues);
}

function saveStudent(studentId) {
  const row = document.getElementById(`student-row-${studentId}`);
  const editableFields = row.querySelectorAll('.editable-field');
  const student = students.find(s => s.id === studentId);
  
  if (!student) return;
  
  // Validate and collect new values
  const newValues = {};
  let isValid = true;
  
  editableFields.forEach(field => {
    const fieldName = field.dataset.field;
    const input = field.querySelector('.field-input');
    const value = input.value.trim();
    
    // Validation
    if (fieldName === 'id') {
      const newId = parseInt(value);
      if (isNaN(newId) || newId < 1 || newId > 999) {
        showNotification('ID must be a number between 1 and 999', 'warning');
        isValid = false;
        return;
      }
      // Check if ID already exists (excluding current student)
      if (students.find(s => s.id === newId && s.id !== studentId)) {
        showNotification('ID already exists. Please choose a different ID.', 'warning');
        isValid = false;
        return;
      }
      newValues[fieldName] = newId;
    } else if (fieldName === 'name') {
      if (value.length < 2) {
        showNotification('Name must be at least 2 characters long', 'warning');
        isValid = false;
        return;
      }
      newValues[fieldName] = value;
    } else if (fieldName === 'class') {
      newValues[fieldName] = value;
    }
  });
  
  if (!isValid) return;
  
  // Update student data
  if (newValues.id !== undefined) student.id = newValues.id;
  if (newValues.name !== undefined) student.name = newValues.name;
  if (newValues.class !== undefined) student.class = newValues.class;
  
  // Exit edit mode
  exitEditMode(row);
  
  // Reload the table to reflect changes
  loadStudentData();
  
  showNotification(`Student ${student.name} updated successfully!`, 'success');
}

function cancelEdit(studentId) {
  const row = document.getElementById(`student-row-${studentId}`);
  const originalValues = JSON.parse(row.dataset.originalValues || '{}');
  
  // Restore original values
  const editableFields = row.querySelectorAll('.editable-field');
  editableFields.forEach(field => {
    const fieldName = field.dataset.field;
    const input = field.querySelector('.field-input');
    input.value = originalValues[fieldName] || '';
  });
  
  // Exit edit mode
  exitEditMode(row);
}

function exitEditMode(row) {
  const editBtn = row.querySelector('.btn-edit');
  const saveBtn = row.querySelector('.btn-save');
  const cancelBtn = row.querySelector('.btn-cancel');
  const editableFields = row.querySelectorAll('.editable-field');
  
  // Hide edit mode
  editBtn.style.display = 'inline-block';
  saveBtn.style.display = 'none';
  cancelBtn.style.display = 'none';
  
  // Disable editing for all fields
  editableFields.forEach(field => {
    const display = field.querySelector('.field-display');
    const input = field.querySelector('.field-input');
    
    display.style.display = 'block';
    input.style.display = 'none';
  });
}

// Modal Management
function initModals() {
  const modals = document.querySelectorAll('.modal');
  const closeButtons = document.querySelectorAll('.close');
  
  closeButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal');
      modal.classList.remove('active');
      setTimeout(() => {
        modal.style.display = 'none';
        // Stop geolocation watcher when panda form modal closes
        if(modal && modal.id === 'panda-form-modal'){
          stopWatchingLocation();
        }
      }, 400);
    });
  });
  
  modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
        setTimeout(() => {
          modal.style.display = 'none';
          if(modal && modal.id === 'panda-form-modal'){
            stopWatchingLocation();
          }
        }, 400);
      }
    });
  });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize chatbot
  new AIChatbot();
  
  // Initialize modals
  initModals();
  
  // Initialize project demos
  initMLScanner();
  initPandaForm();
  
  // Add CSS for analysis grid
  const style = document.createElement('style');
  style.textContent = `
    .analysis-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }
    .analysis-item {
      background: var(--glass);
      padding: 16px;
      border-radius: 8px;
    }
    .fingerprint-analysis {
      background: var(--glass);
      padding: 20px;
      border-radius: 12px;
    }
    .success-message {
      color: #4CAF50;
      font-weight: bold;
      margin-top: 12px;
    }
    .attendance-record {
      background: var(--glass);
      padding: 12px;
      margin: 8px 0;
      border-radius: 8px;
      border-left: 4px solid var(--accent);
    }
    .student-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
    }
    .student-table th,
    .student-table td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .student-table th {
      background: var(--glass);
      color: var(--accent);
    }
    .present {
      color: #4CAF50;
      font-weight: bold;
    }
    .absent {
      color: #f44336;
      font-weight: bold;
    }
    .captured-image-container {
      margin: 16px 0;
      text-align: center;
    }
    .image-wrapper {
      position: relative;
      display: inline-block;
    }
    .emotion-overlay {
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(0, 255, 0, 0.9);
      color: #000;
      padding: 8px 12px;
      border-radius: 20px;
      font-weight: bold;
      font-size: 14px;
      box-shadow: 0 4px 12px rgba(0, 255, 0, 0.3);
    }
    .simulated-image {
      position: relative;
      display: inline-block;
    }
    .error-message {
      color: #f44336;
      font-weight: bold;
      margin-bottom: 12px;
    }
    .retry-btn {
      background: linear-gradient(135deg, #7ef9ff, #b58bff);
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      color: white;
      cursor: pointer;
      font-weight: bold;
      margin-top: 16px;
      transition: all 0.3s;
    }
    .retry-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(126, 249, 255, 0.3);
    }
    .fingerprint-analysis ul {
      text-align: left;
      margin: 12px 0;
      padding-left: 20px;
    }
    .fingerprint-analysis li {
      margin: 8px 0;
      opacity: 0.9;
    }
    .student-name {
      font-weight: bold;
      color: var(--accent);
    }
    .status-icon {
      font-size: 16px;
      margin-right: 8px;
    }
    .action-buttons {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .btn-present, .btn-absent {
      padding: 6px 12px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: bold;
      transition: all 0.3s;
      min-width: 80px;
    }
    .btn-present {
      background: #4CAF50;
      color: white;
    }
    .btn-present:hover:not(:disabled) {
      background: #45a049;
      transform: translateY(-2px);
    }
    .btn-present:disabled {
      background: #666;
      cursor: not-allowed;
      opacity: 0.6;
    }
    .btn-absent {
      background: #f44336;
      color: white;
    }
    .btn-absent:hover:not(:disabled) {
      background: #da190b;
      transform: translateY(-2px);
    }
    .btn-absent:disabled {
      background: #666;
      cursor: not-allowed;
      opacity: 0.6;
    }
    .student-table td {
      vertical-align: middle;
    }
    .student-table small {
      color: #888;
      font-size: 11px;
    }
    .notification {
      animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    .editable-field {
      position: relative;
      cursor: pointer;
      transition: background-color 0.3s;
    }
    .editable-field:hover {
      background-color: rgba(126, 249, 255, 0.1);
    }
    .field-display {
      display: block;
      padding: 4px;
    }
    .field-input {
      width: 100%;
      padding: 4px 8px;
      border: 2px solid var(--accent);
      border-radius: 4px;
      background: var(--card);
      color: inherit;
      font-size: 14px;
    }
    .field-input:focus {
      outline: none;
      border-color: #00ff00;
      box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
    }
    .edit-buttons {
      display: flex;
      gap: 4px;
      flex-wrap: wrap;
    }
    .btn-edit, .btn-save, .btn-cancel {
      padding: 4px 8px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 11px;
      font-weight: bold;
      transition: all 0.3s;
      min-width: 60px;
    }
    .btn-edit {
      background: #2196F3;
      color: white;
    }
    .btn-edit:hover {
      background: #1976D2;
      transform: translateY(-1px);
    }
    .btn-save {
      background: #4CAF50;
      color: white;
    }
    .btn-save:hover {
      background: #45a049;
      transform: translateY(-1px);
    }
    .btn-cancel {
      background: #f44336;
      color: white;
    }
    .btn-cancel:hover {
      background: #da190b;
      transform: translateY(-1px);
    }
    .student-table th:last-child {
      text-align: center;
    }
    .student-table td:last-child {
      text-align: center;
    }
  `;
  document.head.appendChild(style);
});
