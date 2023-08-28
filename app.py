from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

def load_history_from_file():
    try:
        with open('history.json', 'r') as file:
            history_data = json.load(file)
            return history_data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return []


history = load_history_from_file()

def save_history_to_file():
    with open('history.json', 'w') as file:
        json.dump(history, file)

def parse_and_calculate(expression):
    operators = {'plus': '+', 'minus': '-', 'into': '*', 'divided': '/'}
    tokens = expression.split('/')
    result = []

    for token in tokens:
        if token in operators:
            result.append(operators[token])
        else:
            result.append(token)

    evaluated_expression = ''.join(result)
    return evaluated_expression

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/<path:expression>')
def calculate(expression):
    clean_expression = expression.replace('plus', '+').replace('minus', '-').replace('into', '*').replace('divided', '/')
    operation = parse_and_calculate(clean_expression)
    
    try:
        answer = eval(operation)
        question = expression.replace('/', ' ')
        history.append({'question': question, 'answer': answer})
        save_history_to_file()  # Save the history to file after every update
        return jsonify({'question': question, 'answer': answer})
    except Exception as e:
        return str(e), 400
    
    

@app.route('/history')
def get_history():
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
