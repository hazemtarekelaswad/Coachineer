from app import app, db
from app.models import User

db.create_all()

u1 = User(fName='John',lName='Doe',password='password',email='',gender='male',age=20,weight=70,height=170,activityLevel='sedentary',goal='lose weight',dietType='vegetarian'
)
