from flask import Flask, render_template, request, jsonify
import pickle
import threading

app = Flask(__name__, static_url_path='/static')

# Define placeholders for models and tokenizers

english_to_odia_model = None
english_to_odia_tokenizer = None

def load_models():
    global english_to_odia_model, english_to_odia_tokenizer
    
    english_to_odia_model = load_model('Eng_odia_model.pkl')
    english_to_odia_tokenizer = load_tokenizer('tokenizer_eng_odia.pkl')

def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as f:
        tokenizer = pickle.load(f)
    return tokenizer

# Asynchronously load models and tokenizers
load_thread = threading.Thread(target=load_models)
load_thread.start()

# Translation functions remain unchanged

# Translation function for Odia to Hindi


# Translation function for English to Odia
def english_to_odia_translate(source_text):
    input_ids_e_o = english_to_odia_tokenizer.encode(source_text, return_tensors="pt")
    translated_ids_e_o = english_to_odia_model.generate(input_ids_e_o)
    translated_text = english_to_odia_tokenizer.decode(translated_ids_e_o[0], skip_special_tokens=True)
    #translated_text = tokenizer.translate(source_text)
    return translated_text
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    global  english_to_odia_model, english_to_odia_tokenizer
    
    if  english_to_odia_model is None or english_to_odia_tokenizer is None:
        return jsonify({'error': 'Models and tokenizers are still loading. Please try again later.'}), 503

    if request.method == 'POST':
        data = request.get_json()
        source_text = data['source_text']
        source_language = data['source_language']
        target_language = data['target_language']
        
        if  source_language == 'English' and target_language == 'Odia':
            translated_text = english_to_odia_translate(source_text)
        else:
            translated_text = "Translation not supported for the selected language pair"
        
        return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
