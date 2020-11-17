from flask import Flask

#configuration
app = Flask(__name__)
app.config.from_object('config.Config')


from web import routes