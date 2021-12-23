from flask import Flask, render_template, redirect, url_for, request
import json
import time
import psycopg2


app = Flask(__name__)
POSTGRES_URI = 'postgres://mewzpjro:LmVUqseI178MBoRAAXmk_RiTXLu3Kwa7@castor.db.elephantsql.com/mewzpjro'

connection = psycopg2.connect(POSTGRES_URI)
with connection:
    with connection.cursor() as cursor:
        try:
            cursor.execute("CREATE TABLE data (name TEXT, course TEXT, date TEXT, hole TEXT, club TEXT, flight_path TEXT, scale TEXT, misshit TEXT)")
        except:
            print('TABLE data has already been constructed. Moving on...')
            pass

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

                resp = handle_data(request.form)

                with connection:
                    with connection.cursor() as cursor:
                        for r in resp:
                            cursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", r)
                time.sleep(1)
                return render_template('success.html')
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
    return render_template('analyze.html')

def handle_data(form):
    print('here')
    first_name = form.get('first-name')
    last_name = form.get('last-name')

    course_name = form.get('course-name')

    year = request.form.get('year-selector')
    month = request.form.get('month-selector')
    day = request.form.get('day-selector')

    holes = [v for (k, v) in form.items() if k.startswith('hole')]
    holes = map_values(holes, 'holes')

    clubs = [v for (k, v) in form.items() if k.startswith('club')]
    clubs = map_values(clubs, 'clubs')

    paths = [v for (k, v) in form.items() if k.startswith('flight')]
    paths = map_values(paths, 'paths')

    scales = [v for (k, v) in form.items() if k.startswith('shot-scale')]
    scales = map_values(scales, 'scales')
    
    misses = [v for (k, v) in form.items() if k.startswith('shot-mis')]
    misses = map_values(misses, 'misses')

    user_name = [first_name + ' ' + last_name]*len(clubs)
    courses = [course_name]*len(clubs)
    date = [year + '-' + month + '-' + day]*len(clubs)

    return zip(user_name, courses, date, holes, clubs, paths, scales, misses)

def map_values(vals, kind):

    if kind == 'holes':
        lookup = {
            '1':'1',
            '2':'2',
            '3':'3',
            '4':'4',
            '5':'5',
            '6':'6',
            '7':'7',
            '8':'8',
            '9':'9',
            '10':'10',
            '11':'11',
            '12':'12',
            '12':'12',
            '13':'13',
            '14':'14',
            '15':'15',
            '16':'16',
            '17':'17',
            '18':'18'
        }

    if kind == 'clubs':
        lookup = {
            "13":"Driver",
            "14":"3 Wood",
            "15":"5 Wood",
            "1":"Hybrid",
            "2":"2 Iron",
            "3":"3 Iron",
            "4":"4 Iron",
            "5":"5 Iron",
            "6":"6 Iron",
            "7":"7 Iron",
            "8":"8 Iron",
            "9":"9 Iron",
            "10":"Pitching Wedge",
            "11":"Sand Wedge",
            "16":"Putter"
        }

    elif kind == 'paths':
        lookup = {
            '1':'Left',
            '2':'Straight',
            '3':'Right'
        }
    
    elif kind == 'scales':
        lookup = {
            '0':'0',
            '1':'1',
            '2':'2',
            '3':'3',
        }

    elif kind == 'misses':
        lookup = {
            '0':'No',
            '1':'Yes'
        }
    
    return [lookup[v] if v in lookup else 'None' for v in vals]

