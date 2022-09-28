from pydantic import BaseModel


class GameInfo(BaseModel):
   id_: str
   date: str
   name: str
   host: str
   length: str
   server: str
   map_version: str

