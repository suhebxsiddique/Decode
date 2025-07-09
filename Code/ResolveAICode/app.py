import nltk
nltk.download('popular')
nltk.download('punkt_tab')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('model.h5')
import json
import random




from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector


# translator pipeline for english to swahili translations

eng_swa_tokenizer = AutoTokenizer.from_pretrained("Rogendo/en-sw")
eng_swa_model = AutoModelForSeq2SeqLM.from_pretrained("Rogendo/en-sw")

eng_swa_translator = pipeline(
    "text2text-generation",
    model = eng_swa_model,
    tokenizer = eng_swa_tokenizer,
)

def translate_text_eng_swa(text):
    translated_text = eng_swa_translator(text, max_length=128, num_beams=5)[0]['generated_text']
    return translated_text


# translator pipeline for swahili to english translations

swa_eng_tokenizer = AutoTokenizer.from_pretrained("Rogendo/sw-en")
swa_eng_model = AutoModelForSeq2SeqLM.from_pretrained("Rogendo/sw-en")

swa_eng_translator = pipeline(
    "text2text-generation",
    model = swa_eng_model,
    tokenizer = swa_eng_tokenizer,
)

def translate_text_swa_eng(text):
  translated_text = swa_eng_translator(text,max_length=128, num_beams=5)[0]['generated_text']
  return translated_text


def get_lang_detector(nlp, name):
    return LanguageDetector()

nlp = spacy.load("en_core_web_sm")

Language.factory("language_detector", func=get_lang_detector)

nlp.add_pipe('language_detector', last=True)





intents = json.loads(open('intents.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
def getResponse(ints, intents_json):
    if ints: 
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    else:
        return "Sorry, I didn't understand that."

def chatbot_response(msg):
    doc = nlp(msg)
    detected_language = doc._.language['language']
    print(f"Detected language chatbot_response:- {detected_language}")
    
    chatbotResponse = "Loading bot response..........."

    if detected_language == "en":
        res = getResponse(predict_class(msg, model), intents)
        chatbotResponse = res
        print("en_sw chatbot_response:- ", res)
    elif detected_language == 'sw':
        translated_msg = translate_text_swa_eng(msg)
        res = getResponse(predict_class(translated_msg, model), intents)
        chatbotResponse = translate_text_eng_swa(res)
        print("sw_en chatbot_response:- ", chatbotResponse)

    return chatbotResponse

    
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Example fallback responses for emotional intelligence
EMPATHETIC_RESPONSES = [
    "I'm here for you. Would you like to talk more about it?",
    "That sounds tough. Remember, it's okay to feel this way.",
    "Thank you for sharing. How can I support you right now?",
    "You are not alone. Let's work through this together.",
    "I'm listening. Tell me more if you'd like."
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg', '').strip().lower()
    # Simple keyword-based demo logic (replace with AI for production)
    if not user_text:
        return "I'm here whenever you're ready to talk."
    if any(word in user_text for word in ["sad", "upset", "depressed", "unhappy"]):
        return "I'm sorry you're feeling this way. Would you like to try a calming exercise or talk more about it?"
    if any(word in user_text for word in ["happy", "good", "great", "excited"]):
        return "That's wonderful to hear! What made you feel this way today?"
    if "anxious" in user_text or "anxiety" in user_text:
        return "Anxiety can be overwhelming. Would you like some breathing tips or to talk it out?"
    if "motivation" in user_text or "motivated" in user_text:
        return "Let's find some motivation together! What's one small thing you'd like to achieve today?"
    if "relax" in user_text or "calm" in user_text:
        return "Let's take a deep breath together. Inhale... Exhale... How do you feel now?"
    # Fallback: empathetic, supportive
    return random.choice(EMPATHETIC_RESPONSES)

if __name__ == "__main__":
    app.run(debug=True)
