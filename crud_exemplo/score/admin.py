from django.contrib import admin
from score.models import Score,Funcionario,Setor,Produto,Estoque

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['name','value']

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome','setor']
    
class SetorAdmin(admin.ModelAdmin):
    list_display = ['nome']
    
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['marca','descricao','unidade_medida']

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto','funcionario','acao','quantidade','data_controle','data_vencimento']

# Register your models hee.
admin.site.register(Score, ScoreAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Estoque, EstoqueAdmin)
