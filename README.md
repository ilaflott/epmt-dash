This Dash interface currently works with EPMT using Pony and sqlite.  

You can use the EPMT library with this interface from the epmt command gui

/build/epmt$ ./epmt -v gui

To run with mock api use python index.py from the ui directory with

environemnt variable "EPMT_GUI_MOCK" set

/build/epmt/ui$ EPMT_GUI_MOCK=1 bash -c 'python index.py'

Once running a main job table will display on localhost:8050

Job graphs are currently displayed with jobid querys

for example:

http://asus:8050/graph?jobid=1234059&groupby=exename


├── EPMT/

│   ├── ui/

│   │   ├── app.py

│   │   ├── index.py

│   │   ├── layout.py

│   │   ├── callbacks.py

│   │   ├── epmt_query_mock.py

│   │   └── ...

│   ├── epmt_query.py

│   ├── epmt

│   ├── settings.py

│   └── ...

Make and run the dash interface.

make build && make run

Visit:
    http://localhost:8050

Make build uses the Dockerfiles/Dockerfile.epmt-interface to build the container

The container is tagged with epmt-interface:latest

Make Run mounts container port 8050 to local 8050

Mounts volume parent directory (EPMT) to container /home

Mounts volume current directory (Dash) to container /home/dash

Testing:

make targets:

make build-selenium

make selenium-test

make build-chromedriver-service

make start-chromedriver

This appears to be prebuilt chromedriver with selenium:

https://github.com/joyzoursky/docker-python-chromedriver

Quick setup with the above:

https://hub.docker.com/r/joyzoursky/python-chromedriver/

git clone https://github.com/joyzoursky/docker-python-chromedriver.git

cd py3/py3.7-selenium

docker run -it -w /usr/workspace -v $(pwd):/usr/workspace joyzoursky/python-chromedriver:3.7-selenium bash


(epmt376) chris@asus:~/epmtwd$ cd ui/
(dash376) chris@asus:~/epmtwd/ui$ docker run -it -w /usr/workspace -v $(pwd):/usr/workspace joyzoursky/python-chromedriver:3.7-selenium bash
Unable to find image 'joyzoursky/python-chromedriver:3.7-selenium' locally
3.7-selenium: Pulling from joyzoursky/python-chromedriver
16ea0e8c8879: Pulling fs layer 
50024b0106d5: Pulling fs layer 
ff95660c6937: Pulling fs layer 
9c7d0e5c0bc2: Waiting 
29c4fb388fdf: Waiting 
8659dae93050: Waiting 
1da0ab556051: Pull complete 
e92ae9350d4a: Pull complete 
c648cb7fc575: Pull complete 
1739cc5c00d0: Pull complete 
8861e94fd428: Pull complete 
d5ee738df783: Pull complete 
c80627325249: Pull complete 
a6bf3cc55daa: Pull complete 
026e3d619a36: Pull complete 
c93d83d159d1: Pull complete 
eb7a8ed5a773: Pull complete 
cbea621af59a: Pull complete 
Digest: sha256:3f89cb97b9208f5bd858374838802825d4b93767a740b5eecfe4e527b827570a
Status: Downloaded newer image for joyzoursky/python-chromedriver:3.7-selenium
root@78d1d1a05101:/usr/workspace# ls
Dockerfiles  README.md    app.py        components          epmt_mock.py           index.py    names.py                 test
Makefile     __init__.py  assets        dash_config.py      epmt_outliers_mock.py  jobs.py     refs.py
NOTES.txt    __pycache__  callbacks.py  docker-compose.yml  epmt_query_mock.py     layouts.py  requirements-ui.txt.py3
root@78d1d1a05101:/usr/workspace# cd test
root@78d1d1a05101:/usr/workspace/test# ls
__pycache__  bsly001.py  selenium_test.py
root@78d1d1a05101:/usr/workspace/test# python selenium_test.py 
test_case_1 (__main__.TestTemplate)
Find and click top-right button ... selenium_test.py:18: DeprecationWarning: use options instead of chrome_options
  self.driver = webdriver.Chrome(chrome_options=chrome_options)
ok
test_case_2 (__main__.TestTemplate)
Find and click Learn more button ... selenium_test.py:18: DeprecationWarning: use options instead of chrome_options
  self.driver = webdriver.Chrome(chrome_options=chrome_options)
ok

----------------------------------------------------------------------
Ran 2 tests in 13.347s

OK
root@78d1d1a05101:/usr/workspace/test#