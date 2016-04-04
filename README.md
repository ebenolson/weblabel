# RBC image labeling tool

### Usage
* Build images:
    - `docker build opencv-py27`
    - `docker-compose build`
* Start containers and initialize Django database:
    - `docker-compose up`
    - `docker exec -it weblabel_web_1 bash`
        - `python manage.py migrate auth`
        - `python manage.py createsuperuser`
        - `python manage.py migrate`
        - `python manage.py collectstatic`

### Database backup
* `docker exec -it weblabel_postgres_1 bash /backup/db_backup.sh`