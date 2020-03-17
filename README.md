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



ui $ make dash-test

docker-compose up test

ui_dash_1 is up-to-date

Starting ui_test_1 ... done

Attaching to ui_test_1

test_1  | test_case_1 (__main__.TestTemplate)

test_1  | Find and click Recent Jobs tab ... ok

....

test_1  | 

test_1  | ----------------------------------------------------------------------

test_1  | Ran 12 tests in 91.517s

test_1  | 

test_1  | OK

ui_test_1 exited with code 0


Unit Testing with pytest:
make unit-test