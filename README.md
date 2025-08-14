# **🎙 Podcast RAG – AI-Powered Podcast Search & Answering**

Podcast RAG is a Python-based application that lets you **search across podcast transcripts** and get **AI-generated answers**.
It works by:

1. **Ingesting** transcripts into a **vector database** for fast searching.
2. **Retrieving** the most relevant parts when you ask a question.
3. **Generating** a detailed, context-aware answer.

**How It Works**

* **RAG** means **Retrieval-Augmented Generation**.
* Instead of the AI guessing from scratch, it **first searches your podcast transcripts**, then uses that context to give better answers.


 **Step-by-Step Setup**

**1. Download the Project**

First, get the code from GitHub:

```bash
git clone https://github.com/yourusername/podcast-rag.git
cd podcast-rag-main
```

This puts all project files on your computer.



**2. Create a Virtual Environment**

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



**3. Install Required Libraries**

```bash
pip install -r requirements.txt
```

This installs everything your project needs (like Chroma DB, LangChain, etc.).



**4. Configure Environment Variables**

The app may need API keys or special settings.

1. Copy the example config:

   ```bash
   cp .env.example .env   # macOS/Linux
   copy .env.example .env # Windows
   ```
2. Open `.env` in a text editor and fill in your keys/settings.


**5. Ingest Podcast Transcripts**

This step reads your transcripts and stores them in the **vector database** so they can be searched quickly.

```bash
python rag/ingest.py --input data/raw --transcripts data/transcripts --collection podcasts --persist vectorstore
```

💡 Your `data/raw` and `data/transcripts` folders are already in the project — just make sure your transcript files are inside.


**6. Search Your Podcasts**

Try asking a question:

```bash
python rag/retrieve.py --query "What did the guest say about AI in healthcare?"
```

The app will:

1. Search your vector database for matching transcript parts.
2. Show the most relevant results.



**7. Run the Full Application**

If you want to run the main app:

```bash
python app/main.py
```

This will start your custom interface or script logic for using RAG.



 **📂 Project Structure (Simple View)**
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


**🛠 Example Usage**

```bash
# Step 1: Process transcripts into the database
python rag/ingest.py --input data/raw --transcripts data/transcripts --collection podcasts --persist vectorstore

# Step 2: Ask a question
python rag/retrieve.py --query "Explain blockchain from episode 5"

# Step 3: Run main app
python app/main.py
```

<img width="1918" height="964" alt="Screenshot 2025-08-14 175048" src="https://github.com/user-attachments/assets/5545d1e4-a1bb-4a49-95ca-6e385651b890" />

<img width="1918" height="964" alt="Screenshot 2025-08-14 175048" src="https://github.com/user-attachments/assets/364967f4-a47c-456e-84db-94255d0af6a8" />

<img width="1919" height="976" alt="Screenshot 2025-08-14 174800" src="https://github.com/user-attachments/assets/7a0a6637-b5aa-4a19-8cb7-41e82ee05b71" />


**👤 Author**

**Shrishti Singh**






