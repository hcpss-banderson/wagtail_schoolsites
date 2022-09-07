#!/usr/bin/env bash

docker exec wagtail_db dropdb -U wagtail schools --force
docker exec wagtail_db createdb -U wagtail schools
rm -rf ./app/*/migrations/000*.py ./app/media/images/* ./app/media/original_images/*
docker exec wagtail_web ./manage.py makemigrations
docker exec wagtail_web ./manage.py migrate
docker exec wagtail_web ./manage.py createsuperuser --noinput

for acronym in "$@"
do
  docker exec wagtail_web ./manage.py hcpss_import $acronym /content/$acronym
done

docker exec wagtail_web ./manage.py runserver 0.0.0.0:8000
