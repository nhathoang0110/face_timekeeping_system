import json
from datetime import datetime
from flask import render_template, abort, session, request, jsonify, flash, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy import extract, or_
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app import db
from app.models import Schedule
from . import admin
# import schedule as schedule_lib
from FACE_RECOGNITION.main import run
from run import scheduler
from run import PATH_TO_MODULE_RECOGNITION

from apscheduler.triggers.combining  import OrTrigger
from apscheduler.triggers.cron import CronTrigger



@admin.route('/schedule', methods=['GET'])
@login_required
def schedule():

	try:
		current_schedule =  db.session.query(Schedule).order_by(Schedule.id.desc()).first()
		current_schedule = current_schedule.__dict__
		del current_schedule['_sa_instance_state']

		# print(type(current_schedule['start_date']))

		if current_schedule['start_date']:
			current_schedule['start_date'] = current_schedule['start_date'].strftime('%d-%m-%Y')

		if current_schedule['end_date']:
			current_schedule['end_date'] = current_schedule['end_date'].strftime('%d-%m-%Y')

		if current_schedule['start_time_in']:
			current_schedule['start_time_in'] = current_schedule['start_time_in'].strftime('%H:%M:%S')

		if current_schedule['end_time_in']:
			current_schedule['end_time_in'] = current_schedule['end_time_in'].strftime('%H:%M:%S')

		if current_schedule['start_time_out']:
			current_schedule['start_time_out'] = current_schedule['start_time_out'].strftime('%H:%M:%S')

		if current_schedule['end_time_out']:
			current_schedule['end_time_out'] = current_schedule['end_time_out'].strftime('%H:%M:%S')

		if current_schedule['correct_time_in']:
			current_schedule['correct_time_in'] = current_schedule['correct_time_in'].strftime('%H:%M:%S')

		if current_schedule['correct_time_out']:
			current_schedule['correct_time_out'] = current_schedule['correct_time_out'].strftime('%H:%M:%S')

	except:
		current_schedule = {'start_date':'', 'end_date':'', 'start_time_in':'', 'end_time_in':'', 
							'start_time_out':'', 'end_time_out':'', 'correct_time_in':'', 'correct_time_out':''}
	# print(current_schedule)
	
	return render_template('admin/create_schedule.html', current_schedule=current_schedule)


@admin.route('/schedule', methods=['POST'])
@login_required
def schedule_post():
	mess = "Tạo lịch mới thành công"

	try:

		start_date = datetime.strptime(request.form.get('start_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
		end_date = datetime.strptime(request.form.get('end_date'), '%d/%m/%Y').strftime('%Y-%m-%d')

		start_time_in = datetime.strptime(request.form.get('start_time_in'), '%H:%M').strftime('%H:%M:%S')
		start_time_out = datetime.strptime(request.form.get('start_time_out'), '%H:%M').strftime('%H:%M:%S')
		end_time_in = datetime.strptime(request.form.get('end_time_in'), '%H:%M').strftime('%H:%M:%S')
		end_time_out = datetime.strptime(request.form.get('end_time_out'), '%H:%M').strftime('%H:%M:%S')
		correct_time_in = datetime.strptime(request.form.get('correct_time_in'), '%H:%M').strftime('%H:%M:%S')
		correct_time_out = datetime.strptime(request.form.get('correct_time_out'), '%H:%M').strftime('%H:%M:%S')

		S = Schedule(start_date=start_date,
					end_date=end_date,
					start_time_in=start_time_in,
					start_time_out=start_time_out,
					end_time_in=end_time_in,
					end_time_out=end_time_out,
					correct_time_in=correct_time_in,
					correct_time_out=correct_time_out)

		db.session.add(S)
		db.session.commit()


		modify_schedule(start_time_in, start_time_out)

	except:
		mess = "Nhập thiếu hoặc sai rồi kìa. Vui lòng kiểm tra lại !!!"

	flash(mess)
	return redirect(url_for('admin.schedule'))



def modify_schedule(start_time_in, start_time_out):
	print(scheduler.get_jobs())
	
	start_time_in = start_time_in.split(':')
	start_time_out = start_time_out.split(':')
	print(start_time_in)
	print(start_time_out)

	morning = CronTrigger(hour=int(start_time_in[0]), minute=int(start_time_in[1]), day_of_week='mon-sun')
	afternoon = CronTrigger(hour=int(start_time_out[0]), minute=int(start_time_out[1]), day_of_week='mon-sun')

	trigger = OrTrigger([morning, afternoon])
	print(trigger)

	scheduler.reschedule_job('my_job', trigger=trigger)


# def start():
#     print('Start')
#     path_detection= PATH_TO_MODULE_RECOGNITION + "model_detection_2021/face-detection-0204.xml"
#     path_vectori= PATH_TO_MODULE_RECOGNITION + "model_vectori/face_v2_16.xml"
#     folder_vector= PATH_TO_MODULE_RECOGNITION + "database/vectors/"
#     path_to_headpose= PATH_TO_MODULE_RECOGNITION + "model_headpose/"
#     flag=0 # 0 is morning 1 is afternoon
#     type_cam=0  # 0 is front, 1 is high camera
#     run(0,type_cam,path_detection,path_vectori,path_to_headpose,folder_vector, time_open=60)


