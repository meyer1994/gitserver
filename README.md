# gitserver

[![build](https://github.com/meyer1994/gitserver/actions/workflows/build.yml/badge.svg)](https://github.com/meyer1994/gitserver/actions/workflows/build.yml)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A very simple git [smart HTTP][6] server.

## About

This was created as a learning experience on how to create, and possibly use,
a custom git server to upload your code. Also to play with some weird ideas...

## Install

We use [`fastapi`][1] to handle all the HTTP interface and [`uvicorn`][2] as the
[ASGI][3]
server.

```bash
$ pip install -r requirements.txt
```

## Usage

```bash
$ uvicorn app:app
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Now you have an HTTP git server running on `localhost:8000`. You can push your
code to it simply by adding a remote that points to it:

```bash
$ git remote add local http://localhost:8000/reponame
# push to it
$ git push local
# clone from it
$ git clone http://localhost:8000/reponame
```

Note that the username/password is currently 'admin' for both. This is found in the [`gitserver/app.py`](./gitserver/app.py) file,
and you can edit that file if you'd like to change the username/password.

Note that the directory where the code is saved is created using python's
`tempfile` module. Which means, when the program exists, or reloads, it **will**
be deleted.

## Docker

There is also a [docker][7] image if you prefer that:

```bash
$ docker run --rm -it -p 8000:8000 meyer1994/gitserver
```

## Thanks

This project would not have been possible without the code in the following
repositories. They helped me understand a lot about git http backend.

- [git_http_backend.py][4]
- [grack][5]


[1]: https://fastapi.tiangolo.com/
[2]: https://uvicorn.org/
[3]: https://asgi.readthedocs.io/en/latest/index.html
[4]: https://github.com/dvdotsenko/git_http_backend.py
[5]: https://github.com/schacon/grack
[6]: https://www.git-scm.com/book/fa/v2/Git-on-the-Server-Smart-HTTP
[7]: https://hub.docker.com/repository/docker/meyer1994/gitserver
