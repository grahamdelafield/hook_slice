from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
Bootstrap(app)

@app.route('/')
def home():
    return render_template('/home.html')

@app.route('/home')
def about():
    return render_template('/home.html')

@app.route('/track', methods=["GET", "POST"])
def track():
    print(request.method)

    if request.method == 'POST':
        if not request.form.get('first-name') == '' and not request.form.get('last-name') == '':
            if request.form.get('month-selector') != 'Choose...' and request.form.get('day-selector') != 'Choose...' and request.form.get('year-selector') != 'Choose...':
                
                with open('data/data.json', 'a') as f:
                    d = {
                        request.form.get('first-name') + ' ' + request.form.get('last-name'):{
                            request.form.get('year-selector') + '-' + request.form.get('month-selector') + '-' + request.form.get('month-selector'):request.form
                        }
                    }
                    f.write(json.dumps(d))
                return ('', 204)
            else:
                return ('', 204)

        else:
            
            return ('', 204)
        
    else:   
        return render_template('track.html')
    

# @app.route('/analyze')
@app.route('/analyze', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
        <form method="POST">
            <div><label>Language: <input type="text" name="language"></label></div>
            <div><label>Framework: <input type="text" name="framework"></label></div>
            <input type="submit" value="Submit">
        </form>'''

def my_print():
    print('HATE')

if __name__=='__main__':
    app.run(debug=True)