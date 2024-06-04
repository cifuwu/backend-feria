python3 -m venv .venv  //crear entorno virtual

source .venv/bin/activate     // entrar al entorno virtual

deactivate                  // salir del entorno virtual

pip3 install django     // instalacion de django

pip3 install -r requirements.txt     // instalar los paquetes de requirements.txt

django-admin startproject name    //  creacion proyecto django 

python3 manage.py makemigrations    // crear las migraciones de los datos (cuando se cambia la BD)

python3 manage.py migrate            // hacer las migraciones de los datos 

python3 manage.py runserver          // Correr servidor 

python3 manage.py createsuperuser     // super usuario

python3 manage.py startapp name       // crear app



celery -A backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler   // correr servidor periodico

celery -A backend worker -l INFO     /// correr worker celery
