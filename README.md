# 🎙 Podcast RAG – AI-Powered Podcast Search & Answering

Podcast RAG is a Python-based application that lets you **search across podcast transcripts** and get **AI-generated answers**.
It works by:

1. **Ingesting** transcripts into a **vector database** for fast searching.
2. **Retrieving** the most relevant parts when you ask a question.
3. **Generating** a detailed, context-aware answer.

## 🧠 How It Works

* **RAG** means **Retrieval-Augmented Generation**.
* Instead of the AI guessing from scratch, it **first searches your podcast transcripts**, then uses that context to give better answers.



## 🚀 Step-by-Step Setup

### **1. Download the Project**

First, get the code from GitHub:

```bash
git clone https://github.com/yourusername/podcast-rag.git
cd podcast-rag-main
```

This puts all project files on your computer.



### **2. Create a Virtual Environment**

A virtual environment keeps your project’s Python libraries separate from the rest of your system.

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

When it’s activated, your terminal will show `(venv)` at the start.



### **3. Install Required Libraries**

```bash
pip install -r requirements.txt
```

This installs everything your project needs (like Chroma DB, LangChain, etc.).



### **4. Configure Environment Variables**

The app may need API keys or special settings.

1. Copy the example config:

   ```bash
   cp .env.example .env   # macOS/Linux
   copy .env.example .env # Windows
   ```
2. Open `.env` in a text editor and fill in your keys/settings.


### **5. Ingest Podcast Transcripts**

This step reads your transcripts and stores them in the **vector database** so they can be searched quickly.

```bash
python rag/ingest.py --input data/raw --transcripts data/transcripts --collection podcasts --persist vectorstore
```

💡 Your `data/raw` and `data/transcripts` folders are already in the project — just make sure your transcript files are inside.


### **6. Search Your Podcasts**

Try asking a question:

```bash
python rag/retrieve.py --query "What did the guest say about AI in healthcare?"
```

The app will:

1. Search your vector database for matching transcript parts.
2. Show the most relevant results.



### **7. Run the Full Application**

If you want to run the main app:

```bash
python app/main.py
```

This will start your custom interface or script logic for using RAG.



## 📂 Project Structure (Simple View)

```
podcast-rag-main/
├── app/              # Main application
├── rag/              # Core RAG logic
├── transformer/      # Model database
├── vectorstore/      # Saved vector data
├── data/raw/         # Original podcast files
├── data/transcripts/ # Transcript text files
├── .env.example      # Example settings
├── requirements.txt  # Libraries list
```

---

## 🛠 Example Usage

```bash
# Step 1: Process transcripts into the database
python rag/ingest.py --input data/raw --transcripts data/transcripts --collection podcasts --persist vectorstore

# Step 2: Ask a question
python rag/retrieve.py --query "Explain blockchain from episode 5"

# Step 3: Run main app
python app/main.py
```


## 💡 Tips

* You only need to **ingest** once, unless you add new transcripts.
* If you change `.env`, restart your app.
* Keep transcripts **clean and well-formatted** for best results.
Alright — here’s the **final human-friendly README** for your **Podcast RAG** project with **Author** and **License** sections added.

## 👤 Author

**Shrishti Singh**



## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
You’re free to use, modify, and distribute this project, provided you keep the license notice.




