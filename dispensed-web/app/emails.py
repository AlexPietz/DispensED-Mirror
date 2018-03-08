from flask import render_template
from flask_mail import Message
from app import app, mail
from app.models import Patient
from threading import Thread
from config import Config_Disp
import logging
from logging.handlers import SMTPHandler
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

CHECK_PERIOD = 15   # 15 minutes


# Check for undispensed drugs and
# send an email notification to current logged user
def undispensed_drugs_check():
    patients = Patient.query.all()
    undispensed_drugs = []
    for patient in patients:
        for assoc in patient.drugs:
            if (assoc.dispensed == 0):
                time = datetime.datetime.now()
                drug_time = assoc.time
                drug_time = drug_time.replace(year=time.year, month=time.month,
                                              day=time.day)
                if (time > drug_time):
                    delta = time - drug_time
                    if (delta.seconds > (CHECK_PERIOD * 60) and
                            delta.seconds < (CHECK_PERIOD * 4 * 60)):
                        # 15 to 60 minutes after drug time
                        undispensed_drugs.append(
                            {'patient_id': patient.patient_id,
                             'patient_name': patient.name,
                             'drug_id': assoc.drug.drug_id,
                             'drug_name': assoc.drug.name,
                             'qty': assoc.qty,
                             'time': assoc.time.strftime('%H:%M')}
                        )
    if (len(undispensed_drugs) > 0):
        email_notification("DispensED notification message",
                           [Config_Disp.MAIL_DEFAULT_RECIPIENT],
                           undispensed_drugs)


# Notify by email
def email_notification(subject, recipients, drugs):
    send_email(subject,
               Config_Disp.MAIL_DEFAULT_SENDER,
               recipients,
               text_body(drugs),
               html_body(drugs))


# Send an email in a background thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Send an email
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


# Render text and html bodies from email.txt and email.html templates
def text_body(drugs):
    with app.app_context():
        return render_template("email.txt", undispensed_drugs=drugs)


def html_body(drugs):
    with app.app_context():
        return render_template("email.html", undispensed_drugs=drugs)


# SMTP init
credentials = None
if Config_Disp.MAIL_USERNAME or Config_Disp.MAIL_PASSWORD:
    credentials = (Config_Disp.MAIL_USERNAME, Config_Disp.MAIL_PASSWORD)
mail_handler = SMTPHandler((Config_Disp.MAIL_SERVER, Config_Disp.MAIL_PORT),
                           'no-reply@' + Config_Disp.MAIL_SERVER,
                           [Config_Disp.MAIL_DEFAULT_SENDER],
                           'DispensED notification',
                           credentials)
mail_handler.setLevel(logging.INFO)
app.logger.addHandler(mail_handler)

# Start the scheduler
logging.basicConfig()
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=undispensed_drugs_check,
    trigger=IntervalTrigger(minutes=CHECK_PERIOD),
    id='checking_job',
    name='Check for undispensed drugs',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
