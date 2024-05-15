from flask import Flask, render_template, request, redirect, url_for
from dist.Controllers.LampController import *
from dist.Controllers.WindowController import *
from dist.Controllers.Cabinet_Controller import *
from wtforms import *
app = Flask(__name__)


def state(state):
    if state:
        return 'Включено'
    else:
        return 'Выключено'

# Функция вывода строки с тегами кнопок состояния секции кабинета
def button_on_off(state):
    if state:
        return '''<svg class="svg-width-50-px" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M58 18.5C69.855 18.5 79.5 28.145 79.5 40C79.5 51.855 69.855 61.5 58 61.5L22 61.5C10.145 61.5 0.500001 51.855 0.500002 40C0.500003 28.145 10.145 18.5 22 18.5L58 18.5Z"
                                fill="#C00606" />
                            <path
                                d="M22 61C10.421 61 1 51.579 1 40C1 28.421 10.421 19 22 19L58 19C69.579 19 79 28.421 79 40C79 51.579 69.579 61 58 61L22 61ZM22 62L58 62C70.15 62 80 52.15 80 40C80 27.85 70.15 18 58 18L22 18C9.85 18 2.98549e-06 27.85 1.9233e-06 40C8.61114e-07 52.15 9.85 62 22 62Z"
                                fill="#4E7AB5" />
                            <path
                                d="M22 24C13.163 24 6 31.163 6 40C6 48.837 13.163 56 22 56C30.837 56 38 48.837 38 40C38 31.163 30.837 24 22 24Z"
                                fill="white" />
                        </svg>'''
    else:
        return '''<svg class="svg-width-50-px" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M22 61.5C10.145 61.5 0.5 51.855 0.5 40C0.5 28.145 10.145 18.5 22 18.5H58C69.855 18.5 79.5 28.145 79.5 40C79.5 51.855 69.855 61.5 58 61.5H22Z" fill="#8BB7F0"/>
                        <path d="M58 19C69.579 19 79 28.421 79 40C79 51.579 69.579 61 58 61H22C10.421 61 1 51.579 1 40C1 28.421 10.421 19 22 19H58ZM58 18H22C9.85 18 0 27.85 0 40C0 52.15 9.85 62 22 62H58C70.15 62 80 52.15 80 40C80 27.85 70.15 18 58 18Z" fill="#4E7AB5"/>
                        <path d="M58 56C66.837 56 74 48.837 74 40C74 31.163 66.837 24 58 24C49.163 24 42 31.163 42 40C42 48.837 49.163 56 58 56Z" fill="white"/>
                    </svg>'''


# Функция вывода строк о состояния секции кабинета
def show_state(id):
    tags = ''
    lamp = LampController()
    index = 1
    for row in lamp.list_section(id):

        tags += f'''<div class="row justifi-content-between">
                        <p class="text-title">Секция {index}</p>
                        <p>{state(lamp.state_of_lamps_section(id,row))}</p>

                        {button_on_off(lamp.state_of_lamps_section(id,row))}                    
                        
                       
                    </div>'''
        index +=1
    return tags


# Путь - маршрут на главную
@app.route('/')
# Для данного маршрута создаём функцию
def index():
    return render_template('index.html')

# Маршрут с методом POST
@app.route('/',methods=['POST'])
def move_lighting():
    name_cabinet = request.form.get('')


@app.route('/lighting/<id>', methods = ['POST','GET'])
def lighting_id(id):
    lamp = LampController()

    # вывод состояния ламп первой секции
    # state_1 = lamp.state_of_lamps_section(id,1)
    # state_1 = state(state_1)

    # вывод состояния ламп второй секции
    # state_2 = lamp.state_of_lamps_section(id,2)
    # state_2 = state(state_2)
    tags = show_state(id)
    # вывод состояния ламп всех секций
    state_all = lamp.state_of_lamps(id)
    state_all = state(state_all)
    window = WindowController()
    windows = window.window_state(id)
    # Вывод названия кабинета
    cabinet = Cabinet_Controller()
    # словарь о кабите
    dist_cabinet = cabinet.show_name(id)
    name_cabinet = dist_cabinet.name
    deprtament_cabinet = dist_cabinet.department
    if request.method == "POST":
        lamp_all = request.form.get('btn-all-lamps')
        lamp.power_off_all(id, not state(state_all))
        return redirect(f'/lighting/{id}')
        pass
    return render_template("lighting.html", tags=tags, stateAll=state_all, windows=windows,
                           name_cabinet=name_cabinet, deprtament_cabinet=deprtament_cabinet)


@app.route('/climate')
def climate():
    return render_template('climate.html')

@app.route('/lighting')
def lighting():
    return render_template('lighting.html')

@app.route('/safety')
def safety():
    return render_template('safety.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/lighting/lamps')
def laps():
    return 'Это лампы'


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name_cabinet = request.form['name_cabinet']
        return redirect(url_for('lighting', name_cabinet=name_cabinet))
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
