from django.shortcuts import render
from datetime import datetime
from score.models import Score,Funcionario,Produto,Estoque,ItemEstoqueViewModel
from score.forms import ScoreForm,FuncionarioForm,ProdutoForm,EstoqueForm
from django.db.models import Sum
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

    # Obter os itens de entrada e saída do estoque
    itens_entrada = Estoque.objects.filter(acao='ENT').values('produto__id').annotate(total_quantidade=Sum('quantidade'))
    itens_saida = Estoque.objects.filter(acao='SAI').values('produto__id').annotate(total_quantidade=Sum('quantidade'))

    # Criar um dicionário para mapear o ID do produto ao total de entrada
    entrada_dict = {item['produto__id']: item['total_quantidade'] for item in itens_entrada}

    # Criar um dicionário para mapear o ID do produto ao total de saída
    saida_dict = {item['produto__id']: item['total_quantidade'] for item in itens_saida}

    # Calcular o saldo para cada produto
    estoque_final = {}
    for produto_id, quantidade_entrada in entrada_dict.items():
        quantidade_saida = saida_dict.get(produto_id, 0)
        saldo = quantidade_entrada - quantidade_saida
        # Buscar a descrição do produto pelo ID
        descricao = Estoque.objects.filter(produto__id=produto_id).first().produto.descricao
        estoque_final[produto_id] = {'descricao': descricao, 'saldo': saldo}

    # Criar instâncias da view model ItemEstoqueViewModel
    estoque_final_view_model = [ItemEstoqueViewModel(descricao=item['descricao'], saldo=item['saldo']) for produto_id, item in estoque_final.items()]

    # Passar o estoque_final_view_model para o template
    context['estoque_final'] = estoque_final_view_model
        
    return render(request, 'relatorio/list.html', context)