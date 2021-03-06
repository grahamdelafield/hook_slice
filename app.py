from flask import Flask, render_template, redirect, url_for, request, Response, make_response
from pandas import DataFrame
from datetime import datetime
import altair as alt
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
                # user not complete
                return ('', 204)
        else:
            # user data not complete
            return ('', 204)
        
    else:   
        # serve first GET request
        return render_template('track.html')
    

# @app.route('/analyze')
@app.route('/analyze', methods=['GET', 'POST'])
def form_example():
    db_map = get_db_unique('name')
    database_names = list(db_map.items())

    if request.method == 'POST':
        player_name = request.form.get('player-name')
        metric_select = request.form.get('metric')
        metric_organizer = request.form.get('facet')
        for item in [player_name, metric_organizer, metric_select]:
            if item == 'Choose...':
                return ('', 204)
            else:
                query = custom_query(name=db_map[int(player_name)])
                data = get_custom_data(query)
                chart = make_chart(data, metric_select, metric_organizer).to_html()
                return render_template('analyze.html', names=database_names, plot=chart)
        return ('', 204)
    else:
        return render_template('analyze.html', names=database_names)

@app.route('/download', methods=['GET', 'POST'])
def get_data():

    db_map = get_db_unique('name')
    database_names = list(db_map.items())


    if request.method == 'POST':
        if request.form.get('player-name') == 'Player Name':
            return ('', 204)
        else:
            print('SHOULD SEND DATA')
            chosen_name = request.form.get('player-name')
            chosen_name = db_map[int(chosen_name)]
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * from data WHERE name = '{chosen_name}'")
                    player_data = cursor.fetchall()
            
            data = DataFrame(player_data, columns=['Name', 'Course', 'Date', 'Hole', 'Club', 'Flight Path', 'Scale', 'Misshit'])
            
            resp = make_response(data.to_csv(index=False))
            resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
            resp.headers["Content-Type"] = "text/csv"

            return resp

    else:
        return render_template('download.html', names=database_names)

def handle_data(form):
    print(form.items())
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

    for i, item in enumerate([user_name, courses, date, holes, clubs, paths, scales, misses]):
        print(i, len(item))

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

def get_db_unique(column):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT DISTINCT {column} from data")
            data = cursor.fetchall()

    data = sorted([i[0] for i in data])
    idx = range(len(data))
    data = dict(zip(idx, data))
    return data

def custom_query(name=None, course=None, club=None):
    
    where = []

    if name is not None:
        where.append(f"name = '{name}'")
    if course is not None:
        where.append(f"course = '{course}'")
    if club is not None:
        where.append(f"club = '{club}'")

    if where != []:
        where = ['WHERE ' + where[0]] + where[1:]
        where = ' AND '.join(where)

    qry = 'SELECT * FROM data ' + where 
    return qry

def get_custom_data(query):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()

    data = DataFrame(data, columns=['name', 'course', 'date', 'hole', 'club', 'flight_path', 'scale', 'misshit'])
    # data.loc[:, 'date'] = data.date.map(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    data.loc[:, 'hole'] = data.hole.astype(int)

    return data
    
def make_chart(dataframe, metric, facet):

    dataframe = dataframe.sort_values(['date', 'hole', 'club'], ascending=[True, True, True])

    tips = ['date:T']

    if facet == 'club':
        facet = alt.Facet('club', sort=[
            "Driver", "3 Wood", "5 Wood, Hybrid", "2 Iron",
            "3 Iron", "4 Iron", "5 Iron", "6 Iron", "7 Iron",
            "8 Iron", "9 Iron", "Pitching Wedge", "Sand Wedge",
            "Putter"
        ])
        num_cols = 4
    elif facet == 'hole':
        facet = alt.Facet('hole:Q', sort=[str(i) for i in range(1, 19)])
        num_cols = 6
    elif facet == 'course':
        facet = alt.Facet('course:N')
        num_cols = len(dataframe.course.unique())

    if metric == 'strokes':
        y=alt.Y('count()', title='Stroke Count')
        tips.append('count()')
    elif metric == 'misshits':
        dataframe = dataframe[dataframe.misshit=='Yes']
        y=alt.Y('count(misshits):Q', title='Number of Misshits')
        tips.append('count(misshits):Q')
    elif metric == 'scale':
        y=alt.Y('mean(scale):Q', title='Average Scale')
        tips.append('mean(scale):Q')


    dots = alt.Chart(dataframe).mark_circle(size=50).encode(
        x=alt.X('date:T'),
        y=y,
        tooltip=alt.Tooltip(tips)
    ).properties(
        width=100
    ) 

    lines = alt.Chart(dataframe).mark_line().encode(
        x=alt.X('date:T'),
        y=y,
    ).properties(
        width=100
    ) 


    return alt.layer(dots, lines).facet(facet, columns=num_cols)