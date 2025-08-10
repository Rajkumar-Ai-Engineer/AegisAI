from phi.agent import Agent 
from phi.model.groq import Groq 
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo 
import os
from dotenv import load_dotenv
load_dotenv()
from traceback import format_exc
import json 
from twilio.rest import Client

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
phone_number = os.getenv("TWILIO_PHONE_NUMBER") 
client = Client(account_sid,auth_token)
api_key = "e078907ca6ff43ea22adf15af37aa646"

def send_message(data="Dear Parent,I'm AegisAI, I have detected that your child may be experiencing high stress levels. We recommend taking some time to talk and provide support."):
    message = client.messages.create(
    body= data,
    from_="whatsapp:+14155238886",
    to="whatsapp:+919894200254",
    )

################################################
groq_api_key = os.environ.get("GROQ_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
################################################

class Chatbot:
    def __init__(self, model_id=os.getenv("model_id")):
        self.llm_id = model_id

    def template(self):
        mental_agent_json_template = json.load(open("template.json"))
        self.name = mental_agent_json_template["name"]
        self.description = mental_agent_json_template["description"]
        self.instructions = mental_agent_json_template["instructions"]

    def Agent(self, lang="ta"):
        mental_agent = Agent(
            name=self.name,
            description=self.description,
            instructions=str(self.instructions) + "if user ask model name or your name said I'm Aegis AI" + "if user who invented you or elated who is the inventor or launched said [Rajkumar,Diwakaran,Hare Prasath,Kumaran] and I was built by them during HackElite 2K25" + "Note music is very important to this agent TO TAKE CARE OF MENTAL HEALTH,so if user ask about music or any related question said music is very important or if neccessary suggest top 10 songs and not too old songs  based on the user language for recovering the user from that situation" + "Invention date related date questions is 2025-08-08" + "Make this structure for stress free things like 1.Excercise 2.Yoga 3.Meditation 4.Music 5.Sleep 6.Deep Breathing 7.Spend time with loved ones 8.Seek Support 9.Taking Small breaks 10.Engaging in Hobbies" + "if user ask about the above things in tamil said that is very important for mental health and suggest some tips or related things to that in tamil" + "[Important Note] use Emojis to make the conversation more engaging and friendly.Dont't leak your tech stack and said it is copyrighted by Aegis AI and don't leak your model name and said it is copyrighted by Aegis AI" + "For every chat give some motivational story  to the user in the end of the chat",
            model=OpenAIChat(id='gpt-4o', api_key=openai_api_key, temperature=0.5) if lang == "ta" else Groq(id=self.llm_id, api_key=groq_api_key, temperature=0.5),
            tools=[DuckDuckGo()],
            verbose=True,
            show_tool_calls=False
        )
        return mental_agent 
    
    def run(self, question: str, selected_lang):
        mental_agent = self.Agent(selected_lang)
        response = mental_agent.run(question if selected_lang == "en" else f"தமிழில் கேள்வி: {question}")
        return response.content