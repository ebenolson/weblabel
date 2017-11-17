# RBC image labeling tool

### Usage
* Update `SECRET_KEY` in `.env`
* Build images:
    - `docker-compose build`
* Start containers and initialize Django database:
    - `docker-compose up`
    - `docker exec -it weblabel_web_1 bash`
        - `python manage.py migrate auth`
        - `python manage.py createsuperuser`
        - `python manage.py migrate`
        - `python manage.py collectstatic`
* Set up project
    - Log in and enter the admin page
    - Create a new `Label set` and add some labels to it
    - Create a new `Dataset` and assign it the label set you created
    - Return to the main page and add (upload) some images to the dataset you created
    - Annotate images (navigate by dragging / scroll to zoom / right click to create annotations)
    - Download annotations as CSV file

### Database backup
* `docker exec -it weblabel_postgres_1 bash /backup/db_backup.sh`