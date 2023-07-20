
## Setup & Installations
```
python3.11 -m venv venv
source venv/bin/activate
# on windows use
venv\Scripts\activate

pip install -r requirements.txt

# migrations
alembic upgrade head
```
## Run
```
uvicorn main:app --reload
```



### Note for Creating database and tables with Alembic
1. alembic init alembic
2. Edit alembic.ini and add sqlalchemy.url = sqlite:///./db.sqlite3
3. alembic/env.py define following
```
from models import Base
target_metadata = Base.metadata
```
4. alembic revision --autogenerate -m "init models"
5. alembic upgrade head
