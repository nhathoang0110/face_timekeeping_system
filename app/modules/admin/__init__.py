from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import emp_manager, log_manager, salary_manager, schedule_manager