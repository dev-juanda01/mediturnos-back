from env_variables import envs

class Config:
    SQLALCHEMY_DATABASE_URI = envs["DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = envs["TRACK_MODIFICATIONS"]
