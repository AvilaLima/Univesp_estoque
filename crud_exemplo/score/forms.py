from django import forms
from score.models import Score,Funcionario,Setor,Produto,Estoque

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['name', 'value']

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome','setor']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['marca','descricao','unidade_medida']

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['acao','quantidade','data_vencimento','produto','funcionario']
    
        widgets = {
            'acao': forms.Select(attrs={'class':'form-select form-select-sm'}),
            'produto': forms.Select(attrs={'class':'form-select form-select-sm'}),
            'funcionario': forms.Select(attrs={'class':'form-select form-select-sm'}),
            'quantiade': forms.TextInput(attrs={'class':'form-control','type':"number"}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control','type':"date"}),
        }
class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome']