import os

REGION = raw_input("Region? [US/eu] ").strip().lower() != "eu"
if REGION:
    REGION = "us"
else:
    REGION = "eu"
PROJECT_NAME = raw_input("Project name: ")
USE_PGSQL = raw_input("Use PostgreSQL app? [Y/n] ").strip().lower() != "n"
USE_MYSQL = raw_input("Use MySQL app? [y/N] ").strip().lower() == "y"
USE_MONGODB = raw_input("Use MongoHQ app? [y/N] ").strip().lower() == "y"
USE_MEMCACHE = raw_input("Use MemCachier app? [Y/n] ").strip().lower() != "n"
USE_REDIS = raw_input("Use Redis app? (You have to pay for workers) [y/N] ").strip().lower() == "y"
if USE_REDIS:
    USE_CLOUDAMQP = raw_input("Use CloudAMQP app for Message Queuing? [Y/n] ").strip().lower() != "n"
else:
    USE_CLOUDAMQP = False

USE_SENDGRID = raw_input("Use SendGrid for sending emails? [Y/n] ").strip().lower() != "n"
USE_LOGENTRIES = raw_input("Use LogEntries for log management? [y/N] ").strip().lower() == "y"
USE_TINFOIL = raw_input("Use TinFoil Security for vulnerability scans? [y/N] ").strip().lower() == "y"
USE_NEWRELIC = raw_input("Use NewRelic for system monitoring? [y/N] ").strip().lower() == "y"


commands = """
sudo apt-get install libevent-dev libpq-dev libmemcached-dev zlib1g-dev libssl-dev python-dev build-essential
sudo pip install virtualenv
virtualenv --distribute general_venv
. general_venv/bin/activate
pip install Django==1.5.4
export DJANGO_SETTINGS_MODULE=""
python general_venv/lib/python2.7/site-packages/django/bin/django-admin.py startproject --template=https://github.com/aladagemre/django-skel/zipball/master {PROJECT_NAME}
cd {PROJECT_NAME}
virtualenv --distribute venv
. venv/bin/activate
pip install -r reqs/dev.txt
echo "export DJANGO_SETTINGS_MODULE={PROJECT_NAME}.settings.dev" >> venv/bin/activate
. venv/bin/activate
rm -rf docs README.md
git init .
echo "venv" >> .gitignore
git add .; git commit -m 'First commit using django-skel!'
heroku apps:create --region {REGION} {PROJECT_NAME}
heroku config:add DJANGO_SETTINGS_MODULE={PROJECT_NAME}.settings.prod
""".format(**locals())

if USE_MYSQL:
    commands += "heroku addons:add cleardb:ignite\n"
if USE_PGSQL:
    commands += "heroku addons:add heroku-postgresql:dev\n"
if USE_MONGODB:
    commands += "heroku addons:add mongohq:sandbox\n"
if USE_MEMCACHE:
    commands += "heroku addons:add memcachier:dev\n"
if USE_REDIS:
    commands += "heroku addons:add rediscloud:20\n"
if USE_CLOUDAMQP:
    commands += "heroku addons:add cloudamqp:lemur\n"
if USE_SENDGRID:
    commands += "heroku addons:add sendgrid:starter\n"
if USE_LOGENTRIES:
    commands += "heroku addons:add logentries:tryit\n"
if USE_TINFOIL:
    commands += "heroku addons:add tinfoilsecurity:limited\n"
if USE_NEWRELIC:
    commands += "heroku addons:add newrelic:standard\n"
    
commands += """
python manage.py syncdb
python manage.py migrate
python manage.py runserver
firefox http://127.0.0.1:8000/admin
""" % {'PROJECT_NAME': PROJECT_NAME}
    
print commands
f = open("tmp.sh", "w")
f.write(commands)
f.close()
os.system("sh tmp.sh")
