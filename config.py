class Config:
    SECRET_KEY = "supersecretkey"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root@localhost/insurance_flask"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = "shafyarik@gmail.com"
    MAIL_PASSWORD = "yforxgokudmckyqw"

    MAIL_DEFAULT_SENDER = "shafyarik@gmail.com"