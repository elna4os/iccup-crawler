### [iCCup.com](https://iccup.com/) crawler

---

![Alt text](images/slark.png "Title")

---

Features:

- Parse player profile
- Parse game profile
- Parse players list (to do)

---

Run (locally):

- Create and activate virtualenv

- Install dependencies:

```shell
pip install -r app/requirements.txt --no-cache-dir
```

- Run:

```shell
uvicorn app:APP --host <host> --port <port> --reload
```

---

Run (Docker):

- Build an image:

```shell
docker build -t shiriusu/iccup-crawler:<tag> .
```

- Run:

```shell
docker run -d -p 8000:8000 shiriusu/iccup-crawler:<tag>
```