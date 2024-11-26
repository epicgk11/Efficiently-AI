sudo systemctl start mongod
source ../.linuxenv/bin/activate
python manage.py runserver
deactivate
sudo systemctl stop mongod