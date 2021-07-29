start:
	docker-compose -f docker-compose.prod.yml up --build --remove-orphans

stop:
	docker-compose -f docker-compose.prod.yml down --remove-orphans -v
