CC=python3

all:
	# Do you have django/scrapy installed? It need those packages to run
	$(CC) src/scraper_interface/manage.py runserver
	
shell:
	$(CC) src/scraper_interface/manage.py shell

migrate:
	$(CC) src/scraper_interface/manage.py makemigrations
	$(CC) src/scraper_interface/manage.py migrate 

dep:
	pip install -r requirements.txt
