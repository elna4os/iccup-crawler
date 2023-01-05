### [iCCup.com](https://iccup.com/) crawler

An API for parsing player/game profile

---

<ins>Install deps</ins>

```shell
pip install -r app/requirements.txt --no-cache-dir
```

<ins>Run</ins>:

- Locally:

    ```shell
    uvicorn app:APP --host <host> --port <port> --reload
    ```

- Docker image:

    ```shell
  docker run -d -p 8000:8000 shiriusu/iccup-crawler:<tag>
  ```