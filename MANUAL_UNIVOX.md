# 🎓 User Manual: Univox Study Assistant

Welcome to **Univox**, your intelligent AI-powered assistant designed to support university study through Retrieval-Augmented Generation (RAG). This manual will guide you through the system’s features, both as a study participant and as a developer.

***

## 🚀 1. Quick Start

To launch the system on Windows:
1. Make sure Python is installed.
2. Run the `start_univox.bat` file located in the root folder.
3. The application will automatically open in your browser at `http://localhost:8501`.

***

## 🔬 2. Participant Mode (User Study)

This mode is dedicated to system evaluation and follows a guided workflow:

### A. Informed Consent
Before starting, you must read the privacy notice. You are required to select **“I consent”** in the first mandatory section to proceed. You can download the full notice in PDF directly from the screen.

### B. Subject and Scenario Selection
You will choose one of the available subjects (e.g., **MRI**, **SIIA**, **LP**, **Calculus**). The system will assign you a random **study scenario** with a specific objective (e.g., clarify a concept, identify differences between two technologies).

### C. Study Chat
- **Free Questions**: Ask the tutor about course materials. The AI will use uploaded slides and books to answer.
- **Sources**: Below each response, you can see which documents were used (🔧 **Tools**).
- **Study Materials**: In the left sidebar, you will find a dropdown menu to download slides and books related to the selected subject.

### D. Completion
Once you reach the objective, click **“Finish and Complete Questionnaire”** in the sidebar. Answer the questions (SUS scale and qualitative feedback) and click “Submit.” You will receive a unique completion code.

***

## 🛠️ 3. Developer Mode (Dev Mode)

Accessible by selecting “Start Dev Mode” on the initial screen.
- **Password**: The default password is `admin123`.

### Exclusive Features:
- **Chat Management**: Create new chats with custom names and navigate conversation history.
- **Advanced Configuration (Sidebar)**:
  - **LLM Provider**: Choose between *Google Gemini* or *Together AI*.
  - **Complexity Level**: Set the response tone (Basic, Intermediate, Advanced).
  - **Course Selection**: Force the system to focus on a specific subject.
  - **Streaming**: Enable or disable real-time response rendering.

***

## 🎙️ 4. Advanced Features

### 🎤 Voice Commands
Click the microphone icon (🎤) in the input bar to activate voice mode. Record your question and the system will automatically transcribe it. You can also listen to AI responses by clicking the speaker icon (🔊).

### 🖼️ Image Analysis
You can drag and drop images (PNG, JPG) into the chat. The AI will use tools like **Google Lens** or **Mathpix** to analyze graphs, handwritten exercises, or diagrams.

### 📄 Document Upload
You can upload your own PDF or TXT files. The system will temporarily analyze them to answer questions about their content.

***

## 📁 5. Folders & Results

If you are a researcher, here’s where to find the collected 
- **Questionnaire Results**: `userstudy/results/results.csv`
- **Session Logs**: `userstudy/logs/` (JSONL files with each interaction)
- **Analysis Plots**: `userstudy/results/plots/`

***

> [!TIP]
> To ensure optimal performance, make sure you have added all required API keys in the `.env` file inside the `system/` folder.
