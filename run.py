import os

from app import create_app, socketio, db
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time
from FACE_RECOGNITION.main import run
from apscheduler.triggers.combining  import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import json
from app.models import Schedule, Log

PATH_TO_MODULE_RECOGNITION = 'FACE_RECOGNITION/'
PATH_IMAGE_RECOGNITION = 'app/static/'

def start_func():
    print('Start')
    hour_now = datetime.now().hour
    flag = 0
    if hour_now > 12:
        flag = 1

    path_detection= PATH_TO_MODULE_RECOGNITION + "model_detection_2021/face-detection-0204.xml"
    path_vectori= PATH_TO_MODULE_RECOGNITION + "model_vectori/face_v2_16.xml"
    folder_vector= PATH_TO_MODULE_RECOGNITION + "database/vectors/"
    path_to_headpose= PATH_TO_MODULE_RECOGNITION + "model_headpose/"
    # flag=0 # 0 is morning 1 is afternoon
    type_cam=0  # 0 is front, 1 is high camera, 2 is cam laptop

    run(flag,type_cam,path_detection,path_vectori,path_to_headpose,folder_vector, time_open=3600)


    print('tắt camera')
    # write to table log in MySQL
    time_now = datetime.now()
    folder_current = str(time_now.day)+"_"+str(time_now.month)+"_"+str(time_now.year)
    if flag == 0:
        path_json = PATH_TO_MODULE_RECOGNITION + 'results/' + folder_current + '/' + 'morning.json'
    else:
        path_json = PATH_TO_MODULE_RECOGNITION + 'results/' + folder_current + '/' + 'afternoon.json'

    with open(path_json) as json_file:
        data = json.load(json_file)

    with app.app_context():
        current_schedule =  db.session.query(Schedule).order_by(Schedule.id.desc()).first()

        current_schedule = current_schedule.__dict__
        del current_schedule['_sa_instance_state']

        schedule_id = current_schedule['id']
        if current_schedule['correct_time_in']:
            correct_time_in = current_schedule['correct_time_in'].strftime('%H:%M:%S')

        if current_schedule['correct_time_out']:
            correct_time_out = current_schedule['correct_time_out'].strftime('%H:%M:%S')

        correct_time_in = datetime.strptime(correct_time_in, '%H:%M:%S')
        correct_time_out = datetime.strptime(correct_time_out, '%H:%M:%S')
        date = datetime.strptime(str(time_now.day)+"/"+str(time_now.month)+"/"+str(time_now.year), '%d/%m/%Y')

        if flag == 0:
            for k, v in data.items():
                user_id = k
                time_in = datetime.strptime(v, '%H:%M:%S')
                if time_in > correct_time_in:
                    tag_in = 2
                else:
                    tag_in = 1

                log = Log(user_id= int(user_id),
                          schedule_id= int(schedule_id),
                          date= date,
                          time_in= time_in,
                          tag_in = tag_in
                          )

                db.session.add(log)
                db.session.commit()

        if flag == 1:
            for k, v in data.items():
                user_id = k
                time_out = datetime.strptime(v, '%H:%M:%S')
                if time_out < correct_time_out:
                    tag_out = 2
                else:
                    tag_out = 1

                log = Log.query.filter(Log.user_id == int(user_id), Log.date == date).first()
                if log:
                    log.time_out = time_out
                    log.tag_out = tag_out
                    db.session.commit()
                else:
                    log = Log(user_id= int(user_id),
                              schedule_id= int(schedule_id),
                              date= date,
                              time_out= time_out,
                              tag_out = tag_out
                              )

                    db.session.add(log)
                    db.session.commit()



config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
scheduler = BackgroundScheduler()


morning = CronTrigger(hour=10, minute=18, day_of_week='mon-sun')
afternoon = CronTrigger(hour=13, minute=10, day_of_week='mon-sun')

trigger = OrTrigger([morning, afternoon])
# print(trigger)

scheduler.add_job(start_func, trigger, id='my_job')

scheduler.start()

print("zzzzzzzzzzzzz")
print(scheduler.get_jobs())
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# socketio = SocketIO(app)


# export FLASK_ENV=development
if __name__ == '__main__':
    # socketio.run(app)

    print('App Start ////////////////////////////////////////////')

    app.run(debug=True)
