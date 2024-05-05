'''
LINGUANA WEB SERVER v1.0
Linguistics Fingerprint Analyser
Author: https://x.com/037
Repo: https://github.com/649/Linguana/

Application designed to boot web interface.
Purpose is to draw conclusions if two bodies of text share authorship.
'''
import main
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField

import hashlib
from autocorrect import Speller
from _thread import start_new_thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
main.DATABASE = {}
VERSION = '1.1'
class DataForm(FlaskForm):
    data_input = TextAreaField('Document Content:')
    input_field = StringField('Profile Name:')
    delim_field = StringField('Delimiters:')
    submit = SubmitField('Analyse')
    version = '1.4'
    server = VERSION
    logo = main.LOGO
    top_list = main.TOP_LIST
    n_terms = main.N_TERMS

def single_request(delimiter_list, data):
    '''
    Main function for running multi threads for each analyser
    '''
    main.STYLE_FINGERPRINT = []
    main.spell = Speller(lang='en')
    delimiter_list = delimiter_list.split(" ")
    if(len(delimiter_list) == 1 and delimiter_list[0] == ''):
        delimiter_list = [' ']
    main.parsed_words = []
    print("[*] Processing words... Please wait.")
    for line in data.splitlines():
        # No new lines and lower case per line
        line = line.rstrip().lower()
        if(line == ''):
            pass
        else:
            for delimiter in delimiter_list:
                line = line.replace(delimiter, ' ')
            main.parsed_words.append(line.split(' '))
    status = []
    thread_id = 0
    threads = [main.wpl_analyser, main.cpw_analyser, main.word_frequency_analyser, main.n_gram_analyser, main.spelling_analyser]
    for thread in threads:
        status.extend([0]*1)
        main.thread_creator(thread, (status, thread_id, ), status, thread_id)
        thread_id += 1
    main.thread_waiter(status)
    response = "------[BEGIN LINGUANA FINGERPRINT]------" + '\n'
    main.STYLE_FINGERPRINT.sort()
    for fp in main.STYLE_FINGERPRINT:
        response += fp + '\n'
    response += "------[END LINGUANA FINGERPRINT]------" + '\n'
    return response

@app.route('/saved')
def saved():
    data = list(main.DATABASE.items())
    return render_template('diff.html', data=data)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DataForm()
    if form.validate_on_submit():
        # Process the data here
        data = single_request(form.delim_field.data, form.data_input.data)
        profile_name = form.input_field.data
        delim = form.delim_field.data
        # Prints to console
        # print(data)
        main.DATABASE[profile_name] = data
        return render_template('result.html', result=data, profile_name=profile_name, delim=delim)
    return render_template('index.html', form=form)

if __name__ == "__main__":
    '''
    Main function for running multi threads for each analyser
    '''
    print(f"[*] LINGUANA WEB SERVER v{VERSION} - Linguistics Fingerprint Analyser")
    app.run(debug=True)
