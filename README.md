# 🎥 VideoVerse AI

> Transform Videos into Intelligent Conversations using Generative AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

VideoVerse AI is a multilingual AI-powered video intelligence platform that converts YouTube videos and local media into searchable knowledge using Retrieval-Augmented Generation (RAG).
It supports AI-powered transcription, summarization, semantic search, multilingual speech recognition, and conversational question answering.

---

## 🚀 Features

- 🎥 YouTube Video Processing
- 📁 Local Audio & Video Upload
- 🎙️ English Transcription (Whisper)
- 🗣️ Hinglish Transcription (Sarvam AI)
- ✂️ Automatic Audio Chunking
- 🧠 Retrieval-Augmented Generation (RAG)
- 📚 ChromaDB Vector Database
- 🤖 Mistral AI Chatbot
- 📝 AI Summary Generation
- ✅ Action Items Extraction
- 📌 Key Decisions Detection
- ❓ Open Questions Identification
- 💬 Interactive Chat Interface
- 🌐 Streamlit Web Application

---

## 🏗️ Project Architecture

```text
        YouTube / Local Video
                  │
                  ▼
          yt-dlp / File Upload
                  │
                  ▼
            Audio Conversion
             (16kHz Mono WAV)
                  │
                  ▼
      Whisper / Sarvam AI STT
                  │
                  ▼
             Transcript
                  │
                  ▼
     Recursive Text Splitter
                  │
                  ▼
      HuggingFace Embeddings
                  │
                  ▼
             ChromaDB
                  │
                  ▼
         LangChain Retriever
                  │
                  ▼
            Mistral LLM
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
   Chatbot     Summary    Insights
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| UI | Streamlit |
| LLM | Mistral AI |
| Speech-to-Text | Whisper, Sarvam AI |
| Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace |
| Audio Processing | FFmpeg, Pydub |
| Video Download | yt-dlp |
| Environment | Python Virtual Environment |

---

## 📂 Project Structure

```text
videoverse-ai/
│
├── app.py                # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md
├── .env.example           # Template for required environment variables
├── core/                  # Transcription, summarization, extraction, RAG logic
├── database/              # ChromaDB persistence
├── downloads/             # yt-dlp video/audio downloads
├── outputs/               # Generated transcripts, summaries, exports
├── temp/                  # Intermediate audio chunks
├── ui/                    # Streamlit UI components
├── utils/                 # Audio processing helpers
└── assets/                # Images/icons used in the app
```

---

## ⚙️ Installation

Clone the repository
```bash
git clone https://github.com/Jayaprakash733/videoverse-ai.git
```

Go to project
```bash
cd videoverse-ai
```

Create virtual environment
```bash
python -m venv venv
```

Activate

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Set up environment variables

Copy the example file and fill in your keys:
```bash
cp .env.example .env
```

```env
MISTRAL_API_KEY=your_key
SARVAM_API_KEY=your_key
```

Run
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🧭 Usage

1. Open the sidebar and paste a **YouTube URL** or a **local file path**.
2. Choose a **language** — `english` or `hinglish`.
3. Click **⚡ Analyse** and watch the pipeline progress through audio processing, transcription, summarization, extraction, and RAG indexing.
4. Review the generated **title**, **summary**, **transcript**, **action items**, **key decisions**, and **open questions**.
5. Use the **chat panel** to ask natural-language questions about the video — answers are retrieved from the transcript via RAG.
6. Clear the chat at any time to start a fresh conversation on the same video.

---

## 📸 Screenshots

```text
screenshots/
├── home.png
├── upload.png
├── summary.png
├── chatbot.png
```

---

## 🔮 Future Improvements

- Multi-language translation
- Speaker diarization
- PDF export
- Timestamped summaries
- Cloud deployment
- Meeting analytics
- Video chapter generation

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Jayaprakash Sahani**
B.Tech CSE | Generative AI Developer

GitHub: [@subhankarpradhan2005](https://github.com/subhankarpradhan2005)

---

## ⭐ Support

If you like this project, ⭐ star the repository.
