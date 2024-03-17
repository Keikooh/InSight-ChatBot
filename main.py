import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()
client = OpenAI(
    api_key=os.getenv('API_KEY')
)

app = Flask(__name__, template_folder='templates')

# Saving messages
messages = [
    dict(
        type='bot',
        content='Hi!'
    )
]

@app.route('/')
def principal():
    return render_template('index.html', messages=messages)


@app.route('/send', methods=['POST'])
def sendMessage():
    global messages
    question = request.form.get('question')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    ).choices[0].message.content

    messages.append(
        dict(
            type='user',
            content=question
        )
    )

    messages.append(
        dict(
            type='bot',
            content=response
        )
    )
    return render_template('index.html', messages=messages)


@app.route('/clear', methods=['GET'])
def clear():
    global messages
    messages = []

    return redirect(url_for('principal'))


if __name__ == '__main__':
    app.run(debug=True)



