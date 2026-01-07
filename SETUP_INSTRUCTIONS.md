# Oil & Gas Plant Safety Bot - Website

A modern web-based chatbot for educational safety information in oil & gas plant operations.

## 📋 Project Structure

```
├── index.html          # Main website interface
├── style.css          # Responsive styling
├── script.js          # Frontend JavaScript (chat logic)
├── server.py          # Flask backend API
├── run.py            # Python startup script
├── start.bat         # Windows batch startup script
├── requirements.txt   # Python dependencies
├── .env              # API configuration (API key)
└── .gitignore        # Git ignore rules
```

## 🚀 Getting Started

### Option 1: Using Python Script (Recommended)

```bash
# On Windows
python run.py

# On macOS/Linux
python3 run.py
```

This will:
1. Check for required Python packages
2. Install missing dependencies
3. Start the Flask server on `http://localhost:5000`

### Option 2: Using Batch Script (Windows Only)

```bash
start.bat
```

### Option 3: Manual Setup

```bash
# Install dependencies
pip install Flask google-generativeai python-dotenv

# Start the server
python server.py
```

## ⚙️ Configuration

1. **Create `.env` file** with your Google Generative AI API key:
   ```
   GENAI_API_KEY=your_api_key_here
   ```

2. Get your API key from: https://ai.google.dev/

## 🌐 Using the Website

1. Start the server using one of the methods above
2. Open your browser to: **http://localhost:5000**
3. Ask safety-related questions in the chat
4. View responses from the AI assistant

## 📝 Features

- **Modern Chat Interface**: Clean, professional design
- **Real-time Connection Status**: Visual indicator of server connection
- **Sample Queries**: Pre-loaded safety questions for quick access
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Message History**: Chat history during the session
- **Educational Focus**: Explains safety concepts and procedures
- **Safety Disclaimers**: Includes important safety and compliance notices

## 🔒 Safety & Compliance

The bot provides **educational information only** and:
- ✅ Explains safety zones and procedures
- ✅ Describes emergency protocols
- ✅ Clarifies PPE requirements
- ✅ Answers safety training questions
- ❌ Does NOT approve operations
- ❌ Does NOT assess hazard risks
- ❌ Does NOT replace professional audits
- ❌ Does NOT provide operational guidance

## 🛠️ API Endpoints

### Health Check
```
GET /api/health
Response: { "status": "connected", "message": "...", "timestamp": "..." }
```

### Chat Query
```
POST /api/chat
Request:  { "query": "What is a safety zone?" }
Response: { "status": "success", "response": "...", "timestamp": "..." }
```

### Bot Information
```
GET /api/info
Response: { "name": "...", "version": "...", "capabilities": [...] }
```

## 📦 Requirements

- Python 3.7+
- Flask 2.0+
- Google Generative AI
- python-dotenv

See `requirements.txt` for full details.

## 🐛 Troubleshooting

### Server won't start
- Check Python is installed: `python --version`
- Check .env file has correct API key
- Ensure port 5000 is not in use

### Connection refused
- Make sure Flask server is running
- Check that you're visiting `http://localhost:5000` (not https)
- Try refreshing the page

### API key errors
- Verify GENAI_API_KEY is set in .env
- Check API key is valid and has proper permissions
- Visit https://ai.google.dev/ to manage keys

### Chat not responding
- Check server console for error messages
- Verify internet connection (API calls require network)
- Try reloading the page

## 📚 More Information

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Generative AI Docs](https://ai.google.dev/docs)
- [Safety Documentation](./SAFETY_GUIDELINES.txt)

## ⚠️ Important Disclaimers

This bot provides educational information only. For operational decisions and compliance verification, always consult:
- Certified safety professionals
- Regulatory compliance experts
- Your organization's safety protocols
- Professional safety auditors

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2024
