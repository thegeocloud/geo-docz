import string, random
import os, config
from sqlalchemy import Column, String, ForeignKey, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import qrcode

db = SQLAlchemy()

'''
Binds a flask application and a SQLAlchemy service

'''
def setup_db(app, database_path=config.DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Document

'''
# Creates document field with all required fields
class Document(db.Model):  
  __tablename__ = 'documents'

  id = Column(Integer, primary_key=True, nullable=False)
  lat = Column(Float, nullable=False)
  lon = Column(Float, nullable=False)
  category = Column(String(30), nullable=False)
  name = Column(String(300), nullable=False)
  description = Column(String(300), nullable=False)
  document_id = Column(String(10), nullable=False)
  

  def __init__(self, lat, lon, category, name, description, document_id):
    self.lat = lat
    self.lon = lon
    self.category = category
    self.name = name
    self.description = description
    self.document_id = document_id
    

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # Formats document object into dictionary
  def format(self):
    return {
      'id': self.id,
      'lat': self.lat,
      'lon': self.lon,
      'category': self.category,
      'name': self.name,
      'description': self.description, 
      'document_id': self.document_id,
    }
    
  # Generate unique id and check if existing in database
  @classmethod
  def generate_document_id(self):
      exists = True
      
      while exists == True:
        letters = string.ascii_letters
        document_id = ''.join(random.choice(letters) for i in range(10))

        # Checks if document_id already exists in the database
        existing_ids = Document.query.filter(Document.document_id == document_id).one_or_none()
      
        if existing_ids == None:
          exists = False
          return(document_id)
    

  # Generate QRcode using submitted information
  @staticmethod
  def generate_qrcode(document_data):
    qrcode_folder = config.QR_CODE_FOLDER
    
    # Get document data into string
    data = json.dumps(document_data)
    
    # Output file name
    filename = qrcode_folder + "\\" +  document_data['document_id'] + '.png'
    
    # Generate qrcode
    img = qrcode.make(data)
    
    # Save img to a file
    img.save(filename)


'''
Project

'''
# Creates Project class with all required fields

class Project(db.Model):
  __tablename__ = 'projects'

  id = Column(Integer, primary_key=True, nullable=False)
  project_name = Column(String(100), nullable=False)
  description = Column(String(500), nullable=False)
  project_manager = Column(String(50), nullable=False)

  def __init__(self, project_name, description, project_manager):
    self.project_name = project_name
    self.description = description
    self.project_manager = project_manager
  
    
  # Formats project obejcts into dictionary
  def format(self):
    return {
        'id': self.id,
        'project_name': self.project_name,
        'description': self.description, 
        'project_manager': self.project_manager, 
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
 
