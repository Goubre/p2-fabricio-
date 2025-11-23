from pydantic import BaseModel, Field

class Passageiro(BaseModel):
    nome: str
    telefone: str

class Motorista(BaseModel):
    nome: str
    nota: float

class Corrida(BaseModel):
    id_corrida: str = Field(...)
    passageiro: Passageiro
    motorista: Motorista
    origem: str
    destino: str
    valor_corrida: float
    forma_pagamento: str

    class Config:
        allow_population_by_field_name = True
