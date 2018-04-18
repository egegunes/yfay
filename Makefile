build:
	docker build -t yfay .

run:
	docker run -d --env-file ./secrets yfay
