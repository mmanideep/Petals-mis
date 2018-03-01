*Database Config
from petals_mis.models.models import *
db.create_all()
db.session.commit()
