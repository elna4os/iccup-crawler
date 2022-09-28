import click
import uvicorn
from fastapi import FastAPI

APP = FastAPI(title="iCCup crawler")


@APP.get("/players")
async def get_players():
    return {"Hello": "World"}

@APP.get("/task")


@click.command("Enables iCCup crawler API")
@click.option("--port", "-p", default=5000, type=int, help="Port")
def main(port: int):
    uvicorn.run(APP, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
