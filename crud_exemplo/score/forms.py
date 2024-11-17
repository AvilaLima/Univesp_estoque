from django import forms
from score.models import Score, Funcionario, Setor, Produto, Estoque
from datetime import date


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ["name", "value"]


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "setor"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control form-select-sm"}),
            "setor": forms.Select(attrs={"class": "form-select form-select-sm"}),
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["codigo_barras", "referencia", "marca", "descricao", "unidade_medida"]
        widgets = {
            "codigo_barras": forms.TextInput(
                attrs={"class": "form-control form-select-sm", "disabled": "disabled"}
            ),
            "referencia": forms.TextInput(
                attrs={"class": "form-control form-select-sm"}
            ),
            "marca": forms.TextInput(attrs={"class": "form-control form-select-sm"}),
            "descricao": forms.TextInput(
                attrs={"class": "form-control form-select-sm"}
            ),
            "unidade_medida": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
        }


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ["data_controle", "acao", "quantidade", "produto", "funcionario"]

        widgets = {
            "acao": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "produto": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "funcionario": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "quantidade": forms.TextInput(
                attrs={"class": "form-control", "type": "number"}
            ),
            "data_controle": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "value": date.today().strftime("%Y-%m-%d"),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EstoqueForm, self).__init__(*args, **kwargs)
        self.fields["data_controle"].initial = date.today().strftime("%d/%m/%Y")


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ["nome"]
