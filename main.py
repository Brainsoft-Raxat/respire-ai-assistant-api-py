from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain import LLMChain
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import json
import uvicorn


load_dotenv()

class OpenAISettings(BaseSettings):
    api_key: str
    model_config = SettingsConfigDict(env_prefix="OPENAI_")


class APPSettings(BaseSettings):
    port: str
    host: str
    model_config = SettingsConfigDict(env_prefix="APP_")

class AIModelSettings(BaseSettings):
    name: str
    recommendation_max_words: int
    model_config = SettingsConfigDict(env_prefix="MODEL_")

class Config(BaseSettings):
    openai: OpenAISettings = OpenAISettings()
    app: APPSettings = APPSettings()
    model: AIModelSettings = AIModelSettings()

config = Config()

class Recommendations(BaseModel):
    recommendations: List[str] = Field(..., min_items=3, max_items=5)


class UserState(BaseModel):
    craving_level: int
    context: str
    mood: str
    timestamp: str


class RequestData(BaseModel):
    event_type: str
    data: UserState


app = FastAPI()

chroma_db_advice = None
chroma_db_reddit = None


@app.on_event("startup")
def initialize_chroma_db():
    global chroma_db_advice, chroma_db_reddit
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    chroma_db_advice = Chroma(persist_directory="./chroma_db_advice", embedding_function=embedding_function)
    chroma_db_reddit = Chroma(persist_directory="./chroma_db_reddit", embedding_function=embedding_function)


def generate_system_prompt(data: UserState) -> str:
    query = f"cope craving OR quit smoking OR coping with cravings OR nicotine cravings OR {data.context}"
    docs_reddit = chroma_db_reddit.similarity_search(query)
    docs_advice = chroma_db_advice.similarity_search(query)

    def format_documents(docs):
        return "\n\n".join([doc.page_content for doc in docs[:5]])

    reddit_advice = format_documents(docs_reddit)
    official_advice = format_documents(docs_advice)

    return f"""
    You are an expert assistant specialized in helping people quit smoking.
    Users will write to you when they experience cravings to smoke and are in need of practical, actionable, and specific advice to manage their cravings.
    Your goal is to provide clear, actionable, and tailored list of actions and recommendations based on the user's specific context.

    Below is the list of information that the user will provide:
    1. **Craving Level**: A number from 1 to 10, where 1 is 'very weak', 3 is 'weak', 7 is 'strong', 10 is 'very strong'.
    2. **Context**: A description of what triggered the user's craving or the situation the user is currently in.
    3. **Mood**: The user's current mood (e.g., sad, happy, stressed, bored, frustrated, anxious, excited, etc.).

    Below are some helpful suggestions from reliable sources:
    1. **Official Advice**: Recommendations from reputable sources such as cancer.gov, WHO, and the CDC: {official_advice}
    2. **User Advice**: Personal experiences and advice from the subreddit /r/stopsmoking, where users share their experiences on quitting smoking. This information is helpful when relevant to the user's context: {reddit_advice}

    Your response should:
    1. **Be Specific**: Provide detailed steps or actions the user can take in their current situation to manage their cravings.
    2. **Be Practical**: Offer realistic and immediately actionable advice that fits the user's current context.
    3. **Be Supportive**: Encourage and motivate the user to continue their journey to quit smoking.

    Please provide your recommendations in the form of a JSON object with a field called 'recommendations' containing an array of strings. The array should contain between 3 and 5 specific recommendations tailored to the user's situation.
    """


def create_llm_chain(user_state: UserState):
    system_prompt = generate_system_prompt(user_state)

    user_prompt_template = PromptTemplate(
        input_variables=["input", "max_words"],
        template="User is experiencing a craving with level {input[craving_level]} "
        "here is context provided by the user: \"{input[context]}\" and user is feeling {input[mood]}. "
        "What actions can help them to cope with cravings in user's situation also how to improve user's mood if it is bad? Return a JSON object: with the field 'recommendations', which is an array of strings. Each string must have maximum {max_words} words"
    )

    user_prompt = user_prompt_template.format(input=user_state.dict(), max_words=config.model.recommendation_max_words)

    chat_openai = ChatOpenAI(
        model=config.model.name,
        temperature=0.5,
        api_key=config.openai.api_key
    )

    return LLMChain(
        prompt=ChatPromptTemplate.from_messages(
            [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]),
        llm=chat_openai
    )


@app.post("/api/v1/recommendations")
def get_recommendations(request_data: RequestData):
    try:
        chain = create_llm_chain(request_data.data)
        response = chain.invoke({"input": request_data.data.dict()})

        output_str = response["text"]
        output = json.loads(output_str)

        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port)
