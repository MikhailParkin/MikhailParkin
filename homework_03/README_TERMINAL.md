PS C:\Users\muxa\PycharmProjects\MikhailParkin\homework_03> docker build . -t my_app
[+] Building 31.3s (12/12) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                                                  0.0s
 => => transferring dockerfile: 313B                                                                                                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-buster                                                                                                                                                                  0.0s
 => [1/7] FROM docker.io/library/python:3.9-buster                                                                                                                                                                                    0.0s
 => [internal] load build context                                                                                                                                                                                                     0.0s
 => => transferring context: 11.76kB                                                                                                                                                                                                  0.0s
 => CACHED [2/7] WORKDIR /var/app                                                                                                                                                                                                     0.0s
 => [3/7] RUN pip install poetry==1.1.11                                                                                                                                                                                             18.7s
 => [4/7] COPY pyproject.toml poetry.lock ./                                                                                                                                                                                          0.1s
 => [5/7] RUN poetry config virtualenvs.create false                                                                                                                                                                                  1.3s
 => [6/7] RUN poetry install                                                                                                                                                                                                          9.9s
 => [7/7] COPY my_app.py .                                                                                                                                                                                                            0.1s
 => exporting to image                                                                                                                                                                                                                1.1s
 => => exporting layers                                                                                                                                                                                                               1.1s
 => => writing image sha256:0aea9403ef8840ba73b6519e93c071083f0e2129c0d0fdeb0a6bd0ea6605fce1                                                                                                                                          0.0s
 => => naming to docker.io/library/my_app                                                                                                                                                                                             0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
PS C:\Users\muxa\PycharmProjects\MikhailParkin\homework_03> docker run -p 8000:8000 my_app
ERROR:    Error loading ASGI app. Could not import module "app".
PS C:\Users\muxa\PycharmProjects\MikhailParkin\homework_03> docker run -p 8000:8000 my_app
ERROR:    Error loading ASGI app. Could not import module "app".
PS C:\Users\muxa\PycharmProjects\MikhailParkin\homework_03> docker build . -t my_app
[+] Building 0.3s (12/12) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                                                  0.0s
 => => transferring dockerfile: 316B                                                                                                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-buster                                                                                                                                                                  0.0s
 => [1/7] FROM docker.io/library/python:3.9-buster                                                                                                                                                                                    0.0s
 => [internal] load build context                                                                                                                                                                                                     0.0s
 => => transferring context: 96B                                                                                                                                                                                                      0.0s
 => CACHED [2/7] WORKDIR /var/app                                                                                                                                                                                                     0.0s
 => CACHED [3/7] RUN pip install poetry==1.1.11                                                                                                                                                                                       0.0s
 => CACHED [4/7] COPY pyproject.toml poetry.lock ./                                                                                                                                                                                   0.0s
 => CACHED [5/7] RUN poetry config virtualenvs.create false                                                                                                                                                                           0.0s
 => CACHED [6/7] RUN poetry install                                                                                                                                                                                                   0.0s
 => CACHED [7/7] COPY my_app.py .                                                                                                                                                                                                     0.0s
 => exporting to image                                                                                                                                                                                                                0.1s
 => => exporting layers                                                                                                                                                                                                               0.0s
 => => writing image sha256:f3ba1e84a0b04f5c11207060a5243a36000f502b9a2baf228523e2c907a658ed                                                                                                                                          0.0s
 => => naming to docker.io/library/my_app                                                                                                                                                                                             0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
PS C:\Users\muxa\PycharmProjects\MikhailParkin\homework_03> docker run -p 8000:8000 my_app
INFO:     Started server process [8]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     172.17.0.1:41558 - "GET /ping/ HTTP/1.1" 200 OK
INFO:     172.17.0.1:41560 - "GET /ping/ HTTP/1.1" 200 OK
