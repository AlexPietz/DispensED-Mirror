from app import app, db
from app.models import Nurse

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Nurse': Nurse}
