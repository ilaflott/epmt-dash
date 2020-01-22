default: run

build: 
	rm -f requirements.txt.py3
	cp ../requirements.txt.py3 .
	docker build -f Dockerfiles/Dockerfile.epmt-interface -t epmt-interface:latest .
run: 
	#docker run -p 8050:8050 dash/app:latest
	#docker-compose up dash
	docker run -p 8050:8050 -v $(PWD)/..:/home -v $(PWD)/.:/home/dash epmt-interface:latest

dash-test:
	docker build -f Dockerfiles/Dockerfile.dash-test -t dash-test --build-arg EPMT_GUI_MOCK=1 .
	docker run --rm -it python-chromedriver:3.7

build-selenium:
	docker build -f Dockerfiles/Dockerfile.chromedriver-sel -t python-chromedriver:3.7 .

selenium-test:
	docker run --rm -it -w /usr/workspace/test -v $(pwd):/usr/workspace python-chromedriver:3.7 python selenium_test.py

build-chromedriver-service:
	docker build -f Dockerfiles/Dockerfile.chromedriver -t python-chromedriver-ser:latest .

start-chromedriver:
	docker run --rm  --name chromedriver -p 127.0.0.1:4444:4444 python-chromedriver-ser:latest