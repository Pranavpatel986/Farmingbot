🌿 FarmerBot AI: Scientific Agricultural Assistant

FarmerBot is a high-performance RAG (Retrieval-Augmented Generation) chatbot designed to provide farmers with instant, verified scientific agricultural advice. Using Gemini 2.5 Flash and a custom-indexed version of the Farmer's Handbook on Basic Agriculture, this bot answers questions on soil science, seed treatment, irrigation, and pest management.



✨ Features
- Smart Retrieval: Uses LangChain and ChromaDB to search through a 150+ page technical manual.
- Modern UI: A floating web-app style widget with a professional "Smart Farming" landing page.
- Glassmorphism Design: Translucent UI elements for a premium, modern look.
- Responsive: Optimized for both Desktop and Mobile screens.
- Citations: Mentions the source of information to ensure reliability.

🛠️ Tech Stack
- AI Model: Google Gemini 2.5 Flash (via langchain-google-genai)
- Orchestration: LangChain (LCEL)
- Vector Database: ChromaDB
- Frontend: Gradio (Custom CSS/HTML)
- Language: Python 3.12+

🚀 Installation & Local Setup

1. Clone the repository
\\\bash
git clone https://github.com/Pranavpatel986/Farmingbot.git
cd Farmingbot
\\\

2. Create a Virtual Environment
\\\bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
\\\

3. Install Dependencies
\\\bash
pip install -r requirements.txt
\\\

4. Set Up Environment Variables
Create a \.env\ file in the root directory and add your Google API Key:
\\\env
GOOGLE_API_KEY=your_actual_api_key_here
\\\

 5. Run the Chatbot
\\\bash
python chatbot.py
\\\

🌐 Deployment
This project is configured for deployment on **Render**. 
- The \chroma_db\ is included in the repo to handle Render's ephemeral storage.
- The \PORT\ is dynamically assigned for cloud compatibility.

📄 Knowledge Base
The bot is currently trained on:
- Farmer's Handbook on Basic Agriculture (National Institute of Agricultural Extension Management).

🤝 Contributing
Contributions are welcome! Feel free to fork the repo and submit a PR.

---
Developed by Pranav Patel
