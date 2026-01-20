from app.database import Base , engine
from app.auth.models import User


Base.metadata.create_all(bind=engine)

