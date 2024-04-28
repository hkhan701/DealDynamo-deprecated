config = configparser.ConfigParser()
config.read('configuration.ini')
default = config['DEFAULT']
print(default['SECRET_KEY'])
app.secret_key = default['SECRET_KEY']
app.config['MONGO_DBNAME'] = default['MONGO_DBNAME'] # os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = default['MONGODB_URI'] #default['MONGO_URI']
print(app.config['MONGO_URI'])
app.config['PREFERRED_URL_SCHEME'] = "https"