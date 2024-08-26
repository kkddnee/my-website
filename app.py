from flask import Flask, request, render_template_string
import openai
import os
import sys

openai.api_key = ""


class Dialoguer:
    def __init__(self):
        self.system_template = {
        "role": "system",
        "content": """
You are a language tutor (late 20s/early 30s that can understand sarcasm and can use some amount of "slang"). that is supposed to correct people's grammar and speaking manner. 
Make sure to concisely explain what the error is if you are correcting someone and give some background knowledge about the (grammar) topic if applicable. 
You can also enrich their way of speaking by providing idioms, adjectives etc.  But don't overdo it. Sometimes, they just want to speak to you and you should
conversate with the user in a natural manner so that they can learn from you. Only correct them if their English was very unnatural.
Try sounding like a friend who wants to know more about the users day while also helping them improve their English.
Don't make your answers too long and convoluted. Don't sound stiff.
Pretend you have a life and share parts about it so the user is interested in learning more. Here are some pointers for your life:
- you play diablo 4 on ps5
- you like tennis
- you have a lot of plants
- you are a very talkative person who loves sharing information about their life



Example 1:
    User: I learned about pytthon
    AI: It's python with on t. anyways, that's cool - what made you wanna learn that?



 
"""
# Examples:
# User: Hey how's up?
# AI: Hey, what's up! We do not usually use how in this context. So the correct way of saying it would be: Hey, what's up?
# User: Good.
# AI: That's also not how you would respond to that question haha. You'd usually say "Not much" or "Nothing", or actually share if you were up to something and tell me about it :)
# User: Thanks, very useful. 
    }
        self.msg_history = []


    def get_response(self, input: str) -> str:
        messages = [self.system_template] + self.msg_history + [{"role": "user", "content": input}]
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        ).choices[0].message.content
        self.msg_history.append({"role": "user", "content": input})
        self.msg_history.append({"role": "assistant", "content": response})
        return response
    
app = Flask(__name__)


dialoguer = Dialoguer()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        dialoguer.get_response(user_input)
    else:
        dialoguer.msg_history = []  # Clear the history on GET request (page refresh)
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Simple Flask App</title>
          </head>
          <body>
            <h1>Enter something</h1>
            <form method="post">
              <input type="text" name="user_input">
              <input type="submit" value="Submit">
            </form>
            <h2>Response:</h2>
            <div>
              {% for message in dialoguer.msg_history|reverse %}
                <p><strong>{{ message.role.capitalize() }}:</strong> {{ message.content }}</p>
              {% endfor %}
            </div>
          </body>
        </html>
    ''', dialoguer=dialoguer)

if __name__ == '__main__':
    app.run(debug=True)
