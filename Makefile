CC=python3

all:
	$(CC) src/scraper_interface/manage.py crawl
	$(CC) src/scraper_interface/manage.py runserver

serve:
	$(CC) src/scraper_interface/manage.py runserver

shell:
	$(CC) src/scraper_interface/manage.py shell

migrate:
	$(CC) src/scraper_interface/manage.py makemigrations
	$(CC) src/scraper_interface/manage.py migrate

dep:
	pip install -r requirements.txt

docker:
	docker build -t jn-scraper .

docker_run:
	docker run -t --network=host -it jn-scraper
