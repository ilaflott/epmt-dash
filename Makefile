default: run

build: 
	docker build -f Dockerfiles/Dockerfile.epmt-interface -t epmt-interface:latest .
run: 
	#docker run -p 8050:8050 dash/app:latest
	#docker-compose up dash
	docker run -p 8050:8050 -v $(PWD)/..:/home -v $(PWD)/.:/home/dash epmt-interface:latest
