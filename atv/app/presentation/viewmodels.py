from pydantic import BaseModel


class Tarefa(BaseModel):
    id: str = None
    descricao: str
    responsavel: str = None
    nivel_da_prioridade: int
    situacao: str = None
    prioridade: int

    class Config:
        orm_mode = True

    @classmethod
    def from_dict(cls, tarefa_dict):
        nova_tarefa = Tarefa(
            id=str(tarefa_dict.get('_id')),
            descricao=tarefa_dict['descricao'],
            responsavel=tarefa_dict.get('responsavel'),
            nivel_da_prioridade=tarefa_dict['nivel'],
            situacao=tarefa_dict.get('situacao'),
            prioridade=tarefa_dict['prioridade']
        )
        return nova_tarefa

    def to_dict(self):
        return {
            "descricao": self.descricao,
            "responsavel": self.responsavel,
            "nivel": self.nivel_da_prioridade,
            "situacao": self.situacao,
            "prioridade": self.prioridade,
        }