default: run
.PHONY: unit-test dash-test test

build: 
	rm -f requirements.txt.py3
	cp ../requirements.txt.py3 .
	docker build -f Dockerfiles/Dockerfile.epmt-interface -t epmt-interface:latest .
run: 
	#docker run -p 8050:8050 dash/app:latest
	#docker-compose up dash
	docker run -p 8050:8050 -w /home -v $(PWD)/..:/home epmt-interface:latest ./epmt gui

	#docker run -p 8050:8050 dash/app:latest
	#docker-compose up dash
test: unit-test dash-test
run-mock: 
	docker run --rm -p 8050:8050 -e EPMT_GUI_MOCK=1 -v $(PWD)/..:/home -v $(PWD)/.:/home/dash epmt-interface:latest
dash-test:
	#docker run -it --rm -w /usr/workspace/test -v $(PWD):/usr/workspace python-chromedriver:3.7 python find_and_click.py
	docker-compose up test
build-selenium:
	docker build -f Dockerfiles/Dockerfile.chromedriver-sel -t python-chromedriver:3.7 .
selenium-test:
	docker run --rm -it -w /usr/workspace/test -v $(PWD):/usr/workspace python-chromedriver:3.7 python find_and_click.py http://10.0.0.12:8050
build-chromedriver-service:
	docker build -f Dockerfiles/Dockerfile.chromedriver -t python-chromedriver-ser:latest .
start-chromedriver:
	docker run --rm  --name chromedriver -p 127.0.0.1:4444:4444 python-chromedriver-ser:latest
unit-test:
	EPMT_GUI_MOCK=1 python -m pytest test/test_urlparse.py
