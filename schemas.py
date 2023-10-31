from pydantic import BaseModel

class PlantData(BaseModel):
  name: str
  description: str
  publish: bool

class PlantId(PlantData):
  id: int