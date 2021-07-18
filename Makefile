build-image:
	docker build -t chat_app

run-image:
	docker run --rm --name chat_app -p 8080:8080 --env-file .env.dev chat_app