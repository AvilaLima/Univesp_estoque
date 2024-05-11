from django.db import models
from django.utils import timezone

# Create your models here.
class Score(models.Model):
    name = models.CharField(max_length=50)
    value = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-value'] #asc
        #ordering = ['name']

class Produto(models.Model):    
    UNIDADE_MEDIDAS = (
        ("UNID", "Unidade"),
        ("CX", "Caixa"),
        ("REACAO", "Reação"),
        ("ALIQ", "Alíquota"),
        ("KIT", "Kit"),
        ("PLACA", "Placa"),
        ("PCT", "Pacote"),
        ("RACK", "Rack"),
        ("TUBO", "Tubo"),
        ("uL", "Microlitro"),
        ("FR", "Fração"),
    )
    marca = models.CharField(max_length=200,null=False, blank=False)
    descricao = models.CharField(max_length=400, null=False, blank=False)
    unidade_medida = models.CharField(max_length=6, choices=UNIDADE_MEDIDAS, blank=False, null=False)
  
    def __str__(self):
        return self.descricao
    
    class Meta:
        ordering = ['marca','descricao','unidade_medida'] #asc

class Setor(models.Model):
    nome = models.CharField(max_length=100,null=False, blank=False)    

    def __str__(self):
        return self.nome
    
class Funcionario(models.Model):    
    nome = models.CharField(max_length=100,null=False, blank=False)
    setor = models.ForeignKey("Setor", on_delete=models.RESTRICT, related_name='setor')

    def __str__(self):
        return self.nome
    class Meta:
        ordering = ['nome','setor'] #asc
    
class Estoque(models.Model):
    TIPO_DE_ACAO = (
        ("ENT", "Entrada"),
        ("SAI", "Saída"),
    )    
    acao = models.CharField(max_length=6, choices=TIPO_DE_ACAO, blank=False, null=False)
    quantidade = models.PositiveSmallIntegerField()
    data_controle = models.DateTimeField(auto_now_add=True)
    data_vencimento = models.DateField(blank=False, null=False)
    produto = models.ForeignKey("Produto", on_delete=models.RESTRICT, related_name='produto')
    funcionario = models.ForeignKey("Funcionario", on_delete=models.RESTRICT, related_name='funcionario') 

    def __str__(self):
        return 'Produto={0}, Quantidade={1} e data de validade={2}'.format(self.produto, self.quantidade, self.data_vencimento)
    
    class Meta:
        ordering = ['produto','acao','data_controle','data_vencimento','funcionario'] #asc

class ItemEstoqueViewModel:
    def __init__(self, descricao, saldo):
        self.descricao = descricao
        self.saldo = saldo

    def __str__(self):
        return f"Produto: {self.descricao}, Saldo: {self.saldo}"
