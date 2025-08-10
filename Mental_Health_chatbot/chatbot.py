import gradio as gr
from chat_bot_agent import Chatbot


bot = Chatbot()
bot.template()

def chat_response(message, history, language):
    try:
        response = bot.run(message, language)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(title="Mental Health Chatbot") as demo:
    gr.Markdown("# 🧠 Mental Health Chatbot - Aegis AI ")
    
    with gr.Row():
        language = gr.Dropdown(
            choices=[("English", "en"), ("Tamil", "ta")], 
            value="en", 
            label="Language"
        )
    
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(label="Your message", placeholder="Type your message here...")
    
    def respond(message, history, lang):
        if message:
            bot_response = chat_response(message, history, lang)
            history.append((message, bot_response))
        return history, ""
    
    msg.submit(respond, [msg, chatbot, language], [chatbot,msg])

if __name__ == "__main__":
    demo.launch(share=True,debug=True)