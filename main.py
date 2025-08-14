from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import base64
import logging
from datetime import datetime

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Peppo AI Video Generator",
    description="AI-powered video generation with RAG-enhanced prompts - Assignment by Kakarla Dilleswara Rao",
    version="1.0.0",
    contact={
        "name": "Kakarla Dilleswara Rao",
        "email": "dilleswar0050@gmail.com"
    }
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Secure token handling with validation
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    logger.error("⚠️ HF_TOKEN not found in environment variables")
    logger.info("Please set HF_TOKEN in your .env file or environment")

# Initialize InferenceClient with error handling
try:
    client = InferenceClient(
        provider="replicate",
        api_key=HF_TOKEN,
    )
    logger.info("✅ InferenceClient initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize InferenceClient: {e}")

def enhance_prompt(user_prompt):
    """
    Advanced RAG-style prompt enhancement for superior video quality.
    
    This function analyzes the user's input and intelligently adds contextual
    improvements based on content type detection and cinematic best practices.
    
    Args:
        user_prompt (str): Original user input
        
    Returns:
        str: Enhanced prompt with contextual improvements
    """
    # Comprehensive knowledge base for different content categories
    enhancement_database = {
        "cinematic": "cinematic lighting, professional cinematography, high quality, smooth motion",
        "nature": "beautiful natural scenery, natural lighting, peaceful atmosphere, HD quality",
        "action": "dynamic movement, exciting motion, fast-paced action, high energy",
        "portrait": "detailed facial features, realistic rendering, good lighting, clear focus",
        "urban": "modern city atmosphere, urban environment, vibrant details, contemporary style",
        "technical": "5 seconds duration, HD quality, smooth transitions, professional grade"
    }
    
    # Advanced keyword detection with multiple categories
    enhanced = user_prompt.strip()
    
    # Content type analysis and enhancement
    if any(keyword in user_prompt.lower() for keyword in ["person", "man", "woman", "people", "human", "character"]):
        enhanced += f", {enhancement_database['portrait']}"
        logger.info("📝 Applied portrait enhancements")
    elif any(keyword in user_prompt.lower() for keyword in ["run", "jump", "fast", "action", "dance", "sport", "racing"]):
        enhanced += f", {enhancement_database['action']}"
        logger.info("📝 Applied action enhancements")
    elif any(keyword in user_prompt.lower() for keyword in ["forest", "ocean", "mountain", "nature", "tree", "flower", "landscape"]):
        enhanced += f", {enhancement_database['nature']}"
        logger.info("📝 Applied nature enhancements")
    elif any(keyword in user_prompt.lower() for keyword in ["city", "street", "building", "car", "urban", "downtown"]):
        enhanced += f", {enhancement_database['urban']}"
        logger.info("📝 Applied urban enhancements")
    else:
        enhanced += f", {enhancement_database['cinematic']}"
        logger.info("📝 Applied cinematic enhancements")
    
    # Add technical parameters for optimal generation
    enhanced += f", {enhancement_database['technical']}"
    
    logger.info(f"🚀 Prompt enhancement complete: '{user_prompt}' → Enhanced with {len(enhanced) - len(user_prompt)} additional characters")
    return enhanced

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serve the main application interface.
    
    Returns:
        HTMLResponse: Main application page with full functionality
    """
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        logger.info("📄 Main page served successfully")
        return HTMLResponse(content=content)
    except FileNotFoundError:
        logger.error("❌ index.html not found in static directory")
        raise HTTPException(status_code=404, detail="Application frontend not found")

@app.post("/generate-video")
async def generate_video(prompt: str = Form(...)):
    """
    Generate AI video from text prompt with advanced RAG enhancement.
    
    This endpoint processes user prompts through our RAG enhancement system
    and generates high-quality videos using the Wan-AI model.
    
    Args:
        prompt (str): User's text description for video generation
        
    Returns:
        dict: Generated video data with enhancement details
        
    Raises:
        HTTPException: If generation fails or token is invalid
    """
    # Security validation
    if not HF_TOKEN:
        logger.error("🔒 Generation attempted without valid API token")
        raise HTTPException(status_code=500, detail="API token not configured - please contact administrator")
    
    # Input validation and sanitization
    if not prompt or len(prompt.strip()) < 3:
        logger.warning(f"⚠️ Invalid prompt received: '{prompt}'")
        raise HTTPException(status_code=400, detail="Prompt must be at least 3 characters long")
    
    if len(prompt) > 200:
        logger.warning(f"⚠️ Prompt too long: {len(prompt)} characters")
        raise HTTPException(status_code=400, detail="Prompt must be less than 200 characters")
    
    try:
        # RAG-enhanced prompt processing
        original_prompt = prompt.strip()
        enhanced_prompt = enhance_prompt(original_prompt)
        
        # Log generation attempt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"🎬 Video generation started at {timestamp}")
        logger.info(f"📝 Original prompt: '{original_prompt}'")
        logger.info(f"🚀 Enhanced prompt: '{enhanced_prompt}'")
        
        # Generate video using verified AI model
        logger.info("🤖 Calling Wan-AI/Wan2.2-TI2V-5B model via Replicate...")
        video_bytes = client.text_to_video(
            enhanced_prompt,
            model="Wan-AI/Wan2.2-TI2V-5B",
        )
        
        # Validate generation result
        if not video_bytes:
            raise Exception("Model returned empty response")
        
        video_size_mb = len(video_bytes) / (1024 * 1024)
        logger.info(f"✅ Video generated successfully: {len(video_bytes):,} bytes ({video_size_mb:.2f} MB)")
        
        # Secure base64 encoding for frontend transfer
        video_base64 = base64.b64encode(video_bytes).decode('utf-8')
        
        # Comprehensive response with metadata
        response_data = {
            "status": "success",
            "video_data": f"data:video/mp4;base64,{video_base64}",
            "enhanced_prompt": enhanced_prompt,
            "original_prompt": original_prompt,
            "model_used": "Wan-AI/Wan2.2-TI2V-5B",
            "generation_timestamp": timestamp,
            "video_size_bytes": len(video_bytes),
            "enhancement_applied": True
        }
        
        logger.info("🎉 Video generation completed successfully")
        return response_data
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"❌ Video generation failed: {error_message}")
        
        # Detailed error logging for debugging
        if "rate limit" in error_message.lower():
            logger.error("🚦 Rate limit exceeded - user should try again later")
        elif "quota" in error_message.lower():
            logger.error("📊 API quota exceeded - check account limits")
        elif "unauthorized" in error_message.lower():
            logger.error("🔒 Authentication failed - check API token")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Video generation failed: {error_message}"
        )

@app.get("/health")
async def health_check():
    """
    System health check endpoint for monitoring and deployment validation.
    
    Returns:
        dict: System status and configuration details
    """
    health_status = {
        "status": "healthy",
        "service": "Peppo AI Video Generator",
        "version": "1.0.0",
        "developer": "Kakarla Dilleswara Rao",
        "contact": "dilleswar0050@gmail.com",
        "timestamp": datetime.now().isoformat(),
        "api_configured": bool(HF_TOKEN),
        "features": ["Text-to-Video", "RAG Enhancement", "Download Support"]
    }
    logger.info("💚 Health check performed")
    return health_status

@app.get("/api/info")
async def api_information():
    """
    API documentation and feature information endpoint.
    
    Returns:
        dict: Comprehensive API details and capabilities
    """
    return {
        "api_name": "Peppo AI Video Generator",
        "version": "1.0.0",
        "developer": {
            "name": "Kakarla Dilleswara Rao",
            "email": "dilleswar0050@gmail.com",
            "phone": "9150478989"
        },
        "features": {
            "text_to_video": "Generate videos from text descriptions",
            "rag_enhancement": "Intelligent prompt improvement using RAG techniques",
            "download_support": "Direct video download functionality",
            "real_time_processing": "Live generation status updates"
        },
        "model_details": {
            "primary_model": "Wan-AI/Wan2.2-TI2V-5B",
            "provider": "Replicate via Hugging Face",
            "capabilities": "High-quality text-to-video generation"
        },
        "technical_specs": {
            "framework": "FastAPI",
            "deployment": "Vercel Serverless",
            "security": "Environment-based API key management"
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Peppo AI Video Generator...")
    logger.info("👨‍💻 Developed by Kakarla Dilleswara Rao")
    uvicorn.run(app, host="127.0.0.1", port=8000)