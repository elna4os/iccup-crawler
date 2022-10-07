### [iCCup.com](https://iccup.com/) crawler

---

![Alt text](images/slark.png "Title")

---

Features:

- Parse player profile
- Parse game profile (in progress)

---

To run this project:

- Create and activate virtualenv

- Install dependencies:

```shell
pip install -r app/requirements.txt --no-cache-dir
```

- Run API:

```shell
uvicorn app:APP --host <host> --port <port> --reload
```
