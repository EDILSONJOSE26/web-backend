from typing import TypedDict

from bson.objectid import ObjectId
from decouple import config
from pymongo import MongoClient
from typing import List
from ..presentation.viewmodels import Tarefa


class Tarefa_Mongo(TypedDict):
    _id: ObjectId
    descricao: str
    responsavel: str | None
    nivel: int
    situacao: str
    prioridade: int

class TarefaMongoDBRepositorio:

    def __init__(self):
        # Connect to MongoDB
        # uri = 'mongodb://localhost:27017'
        uri = config('MONGODB_URL')
        client = MongoClient(uri)
        db = client['tarefasapp']
        self.tarefas = db['tarefas']

    def listar_tarefas(self, skip: int = 0, take: int = 0) -> List[Tarefa]:
        # Retorna uma lista de todas as tarefas no banco de dados.
        tarefas_encontradas = self.tarefas.find().skip(skip).limit(take)
        return list(map(Tarefa.fromDict, tarefas_encontradas))

    def salvar_tarefa(self, tarefa: Tarefa) -> Tarefa:
        # Salva uma nova tarefa no banco de dados e retorna a tarefa salva.
        _id = self.tarefas.insert_one(tarefa.toDict()).inserted_id
        tarefa.id = str(_id)
        return tarefa

    def obter_tarefa_por_id(self, tarefa_id: str) -> Tarefa:
        # Retorna a tarefa correspondente ao ID fornecido ou None se não existir.
        filtro = {"_id": ObjectId(tarefa_id)}
        tarefa_encontrada = self.tarefas.find_one(filtro)
        return Tarefa.fromDict(tarefa_encontrada) if tarefa_encontrada else None

    def remover_tarefa_por_id(self, tarefa_id: str) -> None:
        # Remove a tarefa correspondente ao ID fornecido.
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tarefas.delete_one(filtro)

    def atualizar_tarefa(self, tarefa_id: str, tarefa: Tarefa) -> Tarefa:
        # Atualiza a tarefa correspondente ao ID fornecido e retorna a tarefa atualizada.
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tarefas.update_one(filtro, {'$set': tarefa.toDict()})
        tarefa.id = tarefa_id
        return tarefa

    def alterar_situacao_da_tarefa(self, tarefa_id: str, situacao: str) -> None:
         # Atualiza a situação da tarefa correspondente ao ID fornecido.
        filtro = {"_id": ObjectId(tarefa_id)}
        update = {"$set": {"situacao": situacao}}
        self.tarefa.update_one(filtro, update)



