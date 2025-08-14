# 🎬 AI Video Generator

A modern web application that generates high-quality videos from text prompts using advanced AI models with intelligent prompt enhancement.

## ✨ Features

- **AI Video Generation**: Transform text descriptions into videos using Wan-AI/Wan2.2-TI2V-5B model
- **RAG-Enhanced Prompts**: Intelligent prompt improvement with contextual keywords
- **Instant Download**: Save generated videos directly to your device
- **Clean UI**: Modern, responsive interface with example prompts
- **Real-time Processing**: Live status updates during video generation
- **Secure API Handling**: Environment-based credential management

## 🛠 Tech Stack

- **Backend**: FastAPI (Python 3.10)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Provider**: Hugging Face Inference API via Replicate
- **Deployment**: Vercel (Serverless)
- **Security**: Environment variables, input validation

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
conda create -n video-gen python=3.10
conda activate video-gen

# Install dependencies
pip install -r requirements.txt
```

### 2. API Configuration

1. Get your Hugging Face token:
   - Visit: https://huggingface.co/settings/tokens
   - Create token with "Inference API" permissions
   - Copy the token (starts with `hf_`)

2. Create `.env` file:
```env
HF_TOKEN=your_hugging_face_token_here
```

### 3. Local Development

```bash
# Start the application
python main.py

# Access at: http://127.0.0.1:8000
```

## 📁 Project Structure

```
ai-video-generator/
├── main.py                 # FastAPI application with RAG enhancement
├── static/
│   ├── index.html         # Frontend interface
│   ├── style.css          # Modern styling
│   └── script.js          # Interactive functionality
├── requirements.txt       # Python dependencies
├── vercel.json           # Deployment configuration
├── .env                  # Environment variables (local)
└── README.md             # Documentation
```

## 🌐 Deployment

### Vercel (Recommended)

1. **GitHub Integration**:
   ```bash
   # Push to GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Vercel Dashboard**:
   - Connect GitHub repository
   - Add environment variable: `HF_TOKEN`
   - Deploy automatically

3. **CLI Deployment**:
   ```bash
   npm i -g vercel
   vercel --prod
   ```

## 🧠 RAG Enhancement System

The application uses a Retrieval-Augmented Generation approach for prompt optimization:

### Enhancement Categories
- **Cinematic**: Professional lighting, smooth motion
- **Nature**: Natural lighting, scenic beauty
- **Action**: Dynamic movement, high energy
- **Portrait**: Detailed focus, realistic rendering
- **Urban**: City atmosphere, modern aesthetics

### Example Enhancement
```
Input:  "A dog running on the beach"
Output: "A dog running on the beach, dynamic movement, exciting, 
         fast-paced, high energy, 5 seconds duration, HD quality, 
         smooth transitions"
```

## 🎯 Usage Examples

### Basic Prompts
- `"A person walking in a forest"`
- `"Cars driving on a highway"`
- `"Flowers blooming in spring"`

### Advanced Prompts
- `"A chef preparing pasta in a modern kitchen"`
- `"Children playing in a park during sunset"`
- `"A cat sitting by a window watching rain"`

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/generate-video` | POST | Video generation with prompt |
| `/health` | GET | Service health check |
| `/api/info` | GET | API information |

## 🔒 Security Features

- **Environment Variables**: Secure credential storage
- **Input Validation**: Prompt length and content checks
- **Error Handling**: Comprehensive error management
- **Logging**: Request tracking and debugging
- **HTTPS**: Secure data transmission (production)

## 📊 Performance

- **Model**: Wan-AI/Wan2.2-TI2V-5B (5B parameters)
- **Provider**: Replicate (optimized inference)
- **Generation Time**: 30-60 seconds typical
- **Output Quality**: HD video, 5-second duration
- **Rate Limits**: Based on Hugging Face free tier

## 🐛 Troubleshooting

### Common Issues

**Token Not Found**:
```bash
# Check .env file exists and contains:
HF_TOKEN=hf_your_actual_token
```

**Module Not Found**:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Video Generation Fails**:
- Verify token has correct permissions
- Check Hugging Face API status
- Try simpler prompts first

## 📝 License

Educational project for demonstrating AI video generation capabilities.

## 🤝 Contributing

This is a student assignment project. For production use, consider:
- Adding user authentication
- Implementing video caching
- Adding more AI models
- Enhanced error recovery

---

**Built with ❤️ for AI video generation**