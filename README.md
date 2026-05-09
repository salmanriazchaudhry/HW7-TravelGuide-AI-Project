# TravelGuide-AI-Project

**Author:** Salman Chaudhry

---

# 1️⃣ Purpose

## Problem the Project Solves

This Python project helps users quickly generate personalized travel plans using Artificial Intelligence. Instead of manually researching destinations, attractions, restaurants, schedules, and travel considerations, the application collects user preferences and generates a structured travel itinerary automatically.

The project solves the following problems:

* Reduces time spent researching travel information
* Generates customized travel plans based on user interests
* Organizes travel recommendations into a readable format
* Allows users to download their travel plan as a PDF document
* Provides a simple user-friendly interface using Streamlit

## Relationship to AI or AI-Assisted Workflows

This project directly uses AI through the OpenAI API.

The application demonstrates an AI-assisted workflow by:

* Collecting structured user input
* Using prompt engineering to guide AI responses
* Sending prompts to an OpenAI language model
* Receiving AI-generated travel recommendations
* Validating and displaying AI-generated content
* Using fallback AI models if one model fails

The project shows how Large Language Models (LLMs) can automate planning, recommendation generation, and content organization.

---

# 2️⃣ What the Code Does

This application is a Streamlit-based AI travel planner written in Python.

## Main Features

### User Input Collection

The app asks the user for:

* Travel destination
* Number of travel days
* Interests (food, museums, nightlife, etc.)
* Things to avoid (too much walking, family restrictions, etc.)

### Prompt Engineering

The code creates:

* A **system prompt** that defines the AI behavior and formatting rules
* A **user prompt** containing the traveler’s preferences

This improves response quality and ensures structured AI output.

### OpenAI API Integration

The application connects to OpenAI models using the OpenAI Python SDK.

The code:

* Sends prompts to AI models
* Receives AI-generated travel plans
* Uses multiple fallback models if a request fails
* Tracks token usage and model information

### Response Validation

The generated response is validated to ensure:

* The output is not empty
* The AI response is usable before displaying it

### Streamlit User Interface

The application uses Streamlit to:

* Build a web-based interface
* Display generated travel plans
* Show diagnostics and model information
* Provide buttons and forms for interaction

### PDF Export

The app converts the AI-generated travel plan into a downloadable PDF using ReportLab.

### Error Handling

The code includes:

* Dependency validation
* API key checks
* Exception handling
* Diagnostic reporting for troubleshooting

---

# 3️⃣ How to Run or Use

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variable Setup

Create a `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run the Streamlit Application

```bash
streamlit run travel_guide.py
```

## How to Use the App

1. Open the Streamlit web application
2. Enter your travel destination
3. Select the number of travel days
4. Add interests and preferences
5. Add any travel constraints or things to avoid
6. Click **Generate Plan**
7. Review the AI-generated itinerary
8. Download the travel plan as a PDF if desired

---

# Step 5: Security & Safe Sharing (Required)

## API Key Protection

The OpenAI API key is stored in environment variables using a `.env` file instead of hardcoding sensitive credentials into the Python script.

## Safe Sharing Practices

Before sharing the project publicly:

* Do NOT upload `.env` files
* Do NOT expose API keys in GitHub repositories
* Add `.env` to `.gitignore`
* Remove personal or sensitive information before sharing

## Input Validation

The application checks for missing required inputs before sending requests to the AI model.

## Error Handling

The project includes exception handling to prevent crashes and provide safe error messages.

## AI Safety Considerations

The system prompt includes instructions to:

* Avoid hallucinated information
* Keep recommendations factual
* Generate structured and concise output
* Avoid unsupported assumptions about the user

These guardrails improve reliability and responsible AI usage.

