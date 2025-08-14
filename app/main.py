import sys
import os
from rag.retrieve import retrieve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Imports ---
import streamlit as st
from rag.retrieve import retrieve
from rag.generate import extractive_answer, abstractive_answer, format_timestamp

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="🎧 Podcast RAG", layout="wide")

# --- App Title & Intro ---
st.title("🎧 Podcast Search — Audio → Text RAG")
st.markdown(
    "Welcome! This tool lets you search for **topics, keywords, or questions** "
    "across your podcast episodes, showing exactly where in the episode they appear."
)

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Search Settings")
    top_k = st.slider("Number of results (Top-K)", min_value=1, max_value=20, value=8, step=1)
    collection = st.text_input("Collection name", value="podcasts")
    persist_dir = st.text_input("Chroma persist directory", value="vectorstore")
    mode = st.radio(
        "Answer mode",
        options=["Extractive", "Abstractive"]
    )
    

# --- Search Input ---
st.write("Type a **topic**, **keyword**, or **question** below to search across your episodes.")
query = st.text_input("🔎 Search Query")
search = st.button("Search")

# --- Search Logic ---
if search and query.strip():
    try:
        # Retrieve relevant transcript segments
        hits = retrieve(
            query=query.strip(),
            k=top_k,
            collection_name=collection,
            persist_dir=persist_dir
        )

        if not hits:
            st.warning("❌ No results found. Try different keywords or rebuild the index.")
        else:
            # Display answer based on selected mode
            if mode.startswith("Extractive"):
                st.subheader("📄 Answer (Extractive)")
                st.markdown(extractive_answer(hits, max_chunks=3), unsafe_allow_html=True)
            else:
                st.subheader("🧠 Answer (Abstractive)")
                st.markdown("")
                answer = abstractive_answer(query.strip(), hits)
                st.markdown(answer)

            # Display relevant transcript segments with audio preview
            st.subheader("🎯 Relevant Segments")
            for _id, doc, meta in hits:
                ep = meta.get("episode_id", "episode")
                start = float(meta["start"])
                end = float(meta["end"])
                ts_label = f"{format_timestamp(start)} → {format_timestamp(end)}"

                # Show episode info & transcript snippet
                st.markdown(f"**{ep}** · `{ts_label}`")
                st.write(doc.strip())

                # Try to load local audio file for preview
                local_mp3 = f"data/raw/{ep}.mp3"
                local_wav = f"data/raw/{ep}.wav"
                if os.path.exists(local_mp3):
                    st.audio(local_mp3, start_time=int(start))
                elif os.path.exists(local_wav):
                    st.audio(local_wav, start_time=int(start))
                else:
                    st.caption("📂 Audio file not found locally. Place `<episode>.mp3` or `<episode>.wav` in `data/raw/` to preview.")

    except Exception as e:
        st.error(f"⚠️ Search failed: {e}")

