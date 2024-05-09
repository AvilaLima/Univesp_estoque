from django.shortcuts import render
from datetime import datetime
from score.models import Score,Funcionario,Produto,Estoque
from score.forms import ScoreForm,FuncionarioForm,ProdutoForm,EstoqueForm
# Create your views here.

def index(request):
    context = {}
    form = ScoreForm()
    scores = Score.objects.all()
    context['scores']= scores
    context['title']= 'Home'
    if request.method == 'POST':
        if 'save' in request.POST:            
            pk = request.POST.get('save')
            if not pk:
                form = ScoreForm(request.POST)
            else:
                score = Score.objects.get(id=pk)
                form = ScoreForm(request.POST, instance=score)
            form.save()            
            form = ScoreForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            score = Score.objects.get(id=pk)
            score.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            score = Score.objects.get(id=pk)
            form = ScoreForm(instance=score)
    context['form'] = form
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