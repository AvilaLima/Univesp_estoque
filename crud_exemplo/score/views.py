from django.shortcuts import render
from score.models import Funcionario,Produto,Estoque,ItemRelatorioViewModel
from score.forms import FuncionarioForm,ProdutoForm,EstoqueForm
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from collections import defaultdict
# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)

def about(request):
    context = {}
    context['title']= 'About'
    return render(request, 'about.html', context)

def funcionarios(request):
    context = {}
    form = FuncionarioForm()
    context['title']= 'Lista de Funcionários'
    funcionarios = Funcionario.objects.all()
    context['funcionarios']= funcionarios
    if request.method == 'POST':
        if 'save' in request.POST:            
            pk = request.POST.get('save')
            if not pk:
                form = FuncionarioForm(request.POST)
            else:
                funcionario = Funcionario.objects.get(id=pk)
                form = FuncionarioForm(request.POST, instance=funcionario)
            form.save()            
            form = FuncionarioForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            funcionario = Funcionario.objects.get(id=pk)
            try:
                funcionario.delete()
            except: 
                context['error'] = 'Não é possível deletar esse funcionário porque tem um ou mais produto(s) em estoque em seu nome'
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            funcionario = Funcionario.objects.get(id=pk)
            form = FuncionarioForm(instance=funcionario)
    context['form'] = form
    return render(request, 'funcionarios/list.html', context)

def produtos(request):
    context = {}
    form = ProdutoForm()
    context['title']= 'Lista de Produtos'
    produtos = Produto.objects.all()
    context['produtos']= produtos
    if request.method == 'POST':
        if 'save' in request.POST:            
            pk = request.POST.get('save')
            if not pk:
                form = ProdutoForm(request.POST)
            else:
                produto = Produto.objects.get(id=pk)
                form = ProdutoForm(request.POST, instance=produto)
            form.save()            
            form = ProdutoForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            produto = Produto.objects.get(id=pk)
            try:
                produto.delete()
            except: 
                context['error'] = 'Não é possível deletar esse produto porque ele se encontra em estoque'
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            produto = Produto.objects.get(id=pk)
            form = ProdutoForm(instance=produto)
    context['form'] = form
    return render(request, 'produtos/list.html', context)

def estoque(request):
    context = {}
    form = EstoqueForm()
    context['title']= 'Estoque'
    estoque = Estoque.objects.all()
    context['estoque']= estoque    
    if request.method == 'POST':
        if 'save' in request.POST:            
            pk = request.POST.get('save')
            if not pk:
                form = EstoqueForm(request.POST)
            else:
                estoque = Estoque.objects.get(id=pk)
                form = EstoqueForm(request.POST, instance=estoque)
            form.save()            
            form = EstoqueForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            estoque = Estoque.objects.get(id=pk)
            try:
                estoque.delete()
            except: 
                context['error'] = 'Não é possível deletar essa entrada no estoque'
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            estoque = Estoque.objects.get(id=pk)
            estoque.data_vencimento = str(estoque.data_vencimento)    
            form = EstoqueForm(instance=estoque)
    context['form'] = form
    return render(request, 'estoque/list.html', context)


def relatorio(request):
    context = {}
    
    # Dicionário de nomes dos meses
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    # Obter os itens de entrada e saída do estoque agrupados por mês
    entradas_por_mes = defaultdict(lambda: defaultdict(int))
    saidas_por_mes = defaultdict(lambda: defaultdict(int))
    
    # Obter entradas por mês
    itens_entrada = Estoque.objects.filter(acao='ENT') \
        .annotate(mes=ExtractMonth('data_controle')) \
        .values('produto__id', 'mes', 'produto__descricao') \
        .annotate(total_quantidade=Sum('quantidade'))
    
    for item in itens_entrada:
        produto_nome = item['produto__descricao']
        mes = meses[item['mes']]
        quantidade = item['total_quantidade']
        entradas_por_mes[produto_nome][mes] += quantidade
    
    # Obter saídas por mês
    itens_saida = Estoque.objects.filter(acao='SAI') \
        .annotate(mes=ExtractMonth('data_controle')) \
        .values('produto__id', 'mes', 'produto__descricao') \
        .annotate(total_quantidade=Sum('quantidade'))
    
    for item in itens_saida:
        produto_nome = item['produto__descricao']
        mes = meses[item['mes']]
        quantidade = item['total_quantidade']
        saidas_por_mes[produto_nome][mes] += quantidade
            
    # Calcular o saldo (ENT - SAI) para cada produto por mês
    saldo_por_produto = defaultdict(lambda: defaultdict(int))
    for produto_nome in set(entradas_por_mes.keys()).union(saidas_por_mes.keys()):
        for mes in set(entradas_por_mes[produto_nome].keys()).union(saidas_por_mes[produto_nome].keys()):
            saldo_por_produto[produto_nome][mes] = entradas_por_mes[produto_nome][mes] - saidas_por_mes[produto_nome][mes]
   
    # Calcular o saldo total por produto
    saldo_total_por_produto = {produto: sum(saldos.values()) for produto, saldos in saldo_por_produto.items()}

    # Criar lista de itens do relatório usando a view model
    itens_relatorio = []
    for produto_nome, meses_saldo in saldo_por_produto.items():
        for mes, saldo in meses_saldo.items():
            total_entrada = entradas_por_mes[produto_nome][mes]
            total_saida = saidas_por_mes[produto_nome][mes]
            itens_relatorio.append(ItemRelatorioViewModel(
                produto=produto_nome,
                mes=mes,
                total_entrada=total_entrada,
                total_saida=total_saida,
                saldo=saldo
            ))

    # Ordenar os itens do relatório por mês, produto e quantidade
    itens_relatorio.sort(key=lambda item: (list(meses.keys())[list(meses.values()).index(item.mes)], item.produto, item.saldo))

    # Passar os dados para o template
    context['itens_relatorio'] = itens_relatorio
    context['saldo_total_por_produto'] = saldo_total_por_produto

    return render(request, 'relatorio/list.html', context)