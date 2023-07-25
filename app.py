from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API 인증 정보 설정
"""openai.organization = "소속코드" """
openai.api_key = "##################"

history_message = [
    
    {"role": "system", "content": "You are a helpful assistant."}
]

model_engine = "gpt-3.5-turbo"

def generate_chat(question):
     # 사용자의 질문을 대화 히스토리에 추가
    history_message.append({"role":"user", "content":question})
    
    # 대화 히스토리를 사용하여 챗봇이 이전 대화를 참조
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history_message
    )
    # API 응답에서 첫 번째 결과 메시지를 호출
    message = completions.choices[0].message.to_dict()
    # 응답으로부터 내용을 추출하고 공백 문자를 제거
    answer = message["content"].strip()
    # 응답 메시지를 대화 히스토리에 추가
    history_message.append(message)
    # 처리된 응답 반환
    return answer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = generate_chat(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
