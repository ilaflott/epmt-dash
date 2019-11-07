default: run

build: 
	docker build -f Dockerfiles/Dockerfile.epmt-interface -t epmt-interface:latest .
run: 
	docker run -p 8050:8050 epmt-interface:latest
