from flask import Flask, request, make_response
from flask_cors import CORS
from translation_utils import translate_statement_pairs, translate_statements, warm_up
from evaluation_utils import evaluate_gemba, evaluate_ssa
from config import settings

app = Flask(__name__)
# Support multiple origins from the FRONTEND_URL setting
origins = settings.FRONTEND_URL.split(',')
CORS(app, origins=origins)

# Pre-load translation models to prevent freezing on first request
warm_up('en', 'pt')

@app.route('/translate', methods = ['POST'])
def translate():
    try:
        # Grab request contents
        req = request.get_json()
        data = req['data']
        translation_type = req['listType']
        from_lang = req['sourceLang']
        to_lang = req['targetLang']

        # Translate based on list type (single / pairs)
        # TODO VALIDATE REQUEST BETTER
        translated_data = []
        if translation_type == 'single':
            translated_data = translate_statements(data, from_lang, to_lang)
        elif translation_type == 'pairs':
            translated_data = translate_statement_pairs(data, from_lang, to_lang)
        else:
            return make_response({'error': 'Invalid list type! Should be single or pairs.'})

        # Return translated response
        res = make_response({'translated': translated_data}, 200)
        return res
    
    except Exception as e:
        return make_response({'error': str(e)}, 500)

@app.route('/evaluate', methods = ['POST'])
def evaluate():
    try:
        # Grab request contents
        req = request.get_json()
        list_type = req['listType']
        source_items = req['sourceItems']
        new_items = req['newItems']
        bt_items = req['backtranslatedItems']
        from_lang = req['sourceLang']
        to_lang = req['targetLang']

        # 1. GEMBA (src + new)

        gemba_res = evaluate_gemba(source_items, new_items, from_lang, to_lang, list_type)

        if 'error' in gemba_res:
            raise AssertionError(gemba_res['error'])
        
        # 2. Semantic similarity assessment

        ssa_res = evaluate_ssa(source_items, new_items, from_lang, to_lang, list_type)

        if 'error' in ssa_res:
            raise AssertionError(ssa_res['error'])
        
        # TODO: COMPARE EXPRESSIONS FOR A SECOND SIMILARITY SCORE?

        return make_response({
            'gemba': gemba_res['score'],
            'semantic': ssa_res
        }, 200)

    except Exception as e:
        return make_response({'error': str(e)}, 500)

if __name__ == '__main__':
    # Run server on host 0.0.0.0 and port from settings
    # Moving this to the end ensures all routes are registered
    app.run(host='0.0.0.0', port=settings.PORT, debug=True)