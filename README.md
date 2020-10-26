# foodgram-project

Пока не запускал на контейнере


Some useful hints:
```
# dump data to fixtures.json
python manage.py dumpdata --exclude=contenttypes > fixtures.json

# build docker image 
docker build -t kiramipt/foodgram_project .

# push docker image to dockerhub
docker push kiramipt/foodgram_project


# run shell on docker
docker exec -it <CONTAINER ID> bash
# collect all static
python manage.py collectstatic
# migrate db
python manage.py migrate --no-input
# create super user
python manage.py createsuperuser
# load temp data
python manage.py loaddata fixtures.json

# run docker container
docker run -it -p 8000:8000 kiramipt/yamdb:latest


# remove volumes
docker-compose down --volumes
docker volume rm api_yamdb_postgres_data
docker volume prune

# Delete all containers using the following command:
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)

# stop local postgres service
sudo service postgresql stop
```