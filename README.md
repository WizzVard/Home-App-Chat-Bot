# HomeHapp

HomeHapp is an AI-powered assistant designed to help users find their ideal homes by engaging in natural conversations. It aims to understand users' lifestyle preferences, living spaces, and housing requirements, providing valuable insights and recommendations to make the house-hunting process more efficient and enjoyable. HomeHapp can quickly identify homes that closely match users' visions and requirements.

##Demo video
[Watch the demo video](files/homeapp_cover.png)(https://github.com/WizzVard/Home-App-Chat-Bot/tree/main/files/2024-08-06_14-05-45 - COMPRESS.mp4)

## Key Features

- **Responsive Queries:** Understands and responds to user's queries related to finding the property they are looking for.
- **Personalized Advice:** Offers personalized advice and recommendations based on user preferences.
- **Engaging Conversations:** Generates human-like text for natural, engaging conversations.
- **Criteria Definition:** Focuses on helping users express and define their criteria and preferences for property selection.
- **US Market Focus:** Currently serves USA homes priced between 100,000 to 3 million. HomeHapp doesn't currently serve properties outside of the USA.
- **Information Prompting:** Asks for missing information, encourage detailed preferences, and summarize requirements.
- **Presents with available houses:** Presents house details with advantages and disandvantages of each house in a user-friendly format allowing users to quickly grasp important information.

## Main underlying techniques used in this chatbot:
- Knowledge graph construction
- Cypher query
- LLM agent

## Installation

1. Clone the repository.
2. Install the required dependencies from the requirements.txt file.
3. Install the Neo4j Desktop app.
4. Install "APOC" and "Graph Data Science" Library plugins.
5. Modify the neo4j.con.
   
## Usage

1. Run the Neo4j graph database.
1. Run the HomeApp.py file
2. Open your web browser and go to `http://localhost:7860` to access the Gradio interface.

---

HomeHapp is crafted to enhance the home search experience by providing detailed, personalized property insights, ensuring that users find the home that best fits their needs.
