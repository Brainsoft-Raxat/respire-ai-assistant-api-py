# Respire AI Assistant API

Our project, "**respire.**", addresses smoking addiction by offering an AI-powered assistant to help users cope with cravings and improve their overall well-being. The backend, built with FastAPI, integrates AI technology to provide personalized recommendations and support for individuals on their journey to quit smoking.

## Table of Contents

- [Respire AI Assistant API](#respire-ai-assistant-api)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Technologies](#technologies)
  - [Core Functionalities](#core-functionalities)
    - [AI-Powered Smoking Craving Support](#ai-powered-smoking-craving-support)
    - [Personalized AI Assistant](#personalized-ai-assistant)
    - [Continuous Deployment](#continuous-deployment)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Clone the Repository](#clone-the-repository)
    - [Install Dependencies](#install-dependencies)
  - [Usage](#usage)
    - [Build and Run the Application](#build-and-run-the-application)
    - [Configuration](#configuration)
  - [API Endpoints](#api-endpoints)

## Overview

The backend of our mobile app is developed using FastAPI and integrates AI technology to provide personalized support to users experiencing nicotine cravings. The system utilizes ChromaDB for similarity searches and LangChain for natural language processing, ensuring tailored recommendations based on authoritative sources and user contexts.

## Technologies

<div align="center">
	<img height="60" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" title="FastAPI" />
	<img height="60" src="https://cdn.freebiesupply.com/logos/large/2x/python-5-logo-png-transparent.png" alt="Python" title="Python" />
    <img height="70" src="https://thirdeyedata.ai/wp-content/uploads/2021/07/VertexAI-512-color.png" alt="Vertex AI" title="Vertex AI" style="margin-left: 5px;" />
    <img height="70" src="https://media.licdn.com/dms/image/D4E12AQHQP9J275Q_uA/article-cover_image-shrink_600_2000/0/1700940849777?e=2147483647&v=beta&t=m0HEQrukIOqU4fe1K9M19PaHq3UbvEubLzeIH1shcSc" alt="LangChain" title="LangChain" style="margin-left: 2px;"/> 
    <img height="59" src="https://miro.medium.com/v2/resize:fit:793/0*RTW5byy6eH_eSWTP.png" alt="Chroma" title="Chroma" style="margin-left: 2px;"/> 
    <img height="60" src="https://firebase.google.com/images/brand-guidelines/logo-built_with_white@2x.png" alt="Firestore" title="Firestore" />
</div>

## Core Functionalities

### AI-Powered Smoking Craving Support
The backend provides tailored advice and recommendations for users experiencing nicotine cravings, leveraging authoritative sources like WHO and Cancer.gov.

### Personalized AI Assistant
Using LangChain and Vertex AI's Gemini Pro 1.5, the AI assistant offers personalized, actionable steps based on the user's context and mood.

### Continuous Deployment
All applications are deployed on Google Cloud Run with automatic scaling and continuous deployment, ensuring consistent performance and rapid updates.

## Installation

### Prerequisites

- Python (version 3.9+)
- FastAPI

### Clone the Repository

```bash
git clone https://github.com/Brainsoft-Raxat/respire-ai-assistant-api-py.git
cd repository
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage
### Build and Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
By default, the application will run on localhost:8080.

### Configuration
- Edit .env file according to your configurations.
- Set APP_HOST to localhost for local development.
- Set any port you want using APP_PORT.
- Set the OpenAI API key using OPENAI_API_KEY.
- Set the VertexAI API key using VERTEX_AI_API_KEY.

## API Endpoints
https://respire-ai-assistant-api-py-jc4tvs5hja-ey.a.run.app/docs