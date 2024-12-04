sudo systemctl start mongod
source ../.Effenv/bin/activate
python manage.py runserver
deactivate
sudo systemctl stop mongod