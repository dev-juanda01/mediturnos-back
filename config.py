import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DESKTOP-IMIOCSF\\SQLEXPRESS/medi_turnos?driver=SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
