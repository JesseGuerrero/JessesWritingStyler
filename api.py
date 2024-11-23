from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import fitz
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def detect_voice_distribution(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    active_count = 0
    passive_count = 0
    active = []
    passive = []

    for sent in doc.sents:
        is_passive = False
        for token in sent:
            # Check for auxiliary verbs that often indicate passive voice
            if token.dep_ == "auxpass" or (token.dep_ == "aux" and token.head.tag_ == "VBN"):
                is_passive = True
                break

        if is_passive:
            passive_count += 1
            passive.append(str(sent).strip())
        else:
            active_count += 1
            active.append(str(sent).strip())

    total_sentences = active_count + passive_count
    active_percentage = (active_count / total_sentences) * 100 if total_sentences else 0
    passive_percentage = (passive_count / total_sentences) * 100 if total_sentences else 0

    return {
        "total_sentences": total_sentences,
        "active_count": active_count,
        "passive_count": passive_count,
        "active_percentage": active_percentage,
        "passive_percentage": passive_percentage,
        "passive sentences": passive,
        "active sentences": active,
    }

@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Get JSON data from the request
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. Please provide 'text' in the request body."}), 400

    text = data['text']
    # Merge the text into one block without line breaks
    result = detect_voice_distribution(text)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)
