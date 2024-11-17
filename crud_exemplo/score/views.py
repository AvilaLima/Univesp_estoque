from django.shortcuts import render
from score.models import Funcionario, Produto, Estoque, ItemRelatorioViewModel
from score.forms import FuncionarioForm, ProdutoForm, EstoqueForm
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from collections import defaultdict
from barcode import EAN13
from barcode.writer import ImageWriter
from tempfile import gettempdir
from PIL import Image
import zxing  # ZXing deve estar instalado e configurado
import logging
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def gerar_codigo_barras(produto_id):
    # Gere um código EAN-13 com base no ID do produto ou outro identificador único
    produto_id = produto_id + 1
    codigo = f"78912345{str(produto_id).zfill(5)}"  # Ajuste conforme necessário
    ean = EAN13(codigo)  # O módulo EAN13 calcula automaticamente o dígito verificador
    return ean.get_fullcode()


def index(request):
    context = {}
    return render(request, "index.html", context)


def about(request):
    context = {}
    context["title"] = "About"
    return render(request, "about.html", context)


def funcionarios(request):
    context = {}
    form = FuncionarioForm()
    context["title"] = "Lista de Funcionários"
    funcionarios = Funcionario.objects.all()
    context["funcionarios"] = funcionarios
    if request.method == "POST":
        if "save" in request.POST:
            pk = request.POST.get("save")
            if not pk:
                form = FuncionarioForm(request.POST)
            else:
                funcionario = Funcionario.objects.get(id=pk)
                form = FuncionarioForm(request.POST, instance=funcionario)
            form.save()
            form = FuncionarioForm()
        elif "delete" in request.POST:
            pk = request.POST.get("delete")
            funcionario = Funcionario.objects.get(id=pk)
            try:
                funcionario.delete()
            except:
                context["error"] = (
                    "Não é possível deletar esse funcionário porque tem um ou mais produto(s) em estoque em seu nome"
                )
        elif "edit" in request.POST:
            pk = request.POST.get("edit")
            funcionario = Funcionario.objects.get(id=pk)
            form = FuncionarioForm(instance=funcionario)
    context["form"] = form
    return render(request, "funcionarios/list.html", context)


def produtos(request):
    context = {}
    form = ProdutoForm()
    context["title"] = "Lista de Produtos"
    produtos = Produto.objects.all()
    context["produtos"] = produtos
    if request.method == "POST":
        if "save" in request.POST:
            pk = request.POST.get("save")
            if not pk:
                form = ProdutoForm(request.POST)
                if form.is_valid():
                    produto = form.save(commit=False)
                    produto_id = (
                        produto.id if produto.id else Produto.objects.count() + 1
                    )
                    codigo_barras = gerar_codigo_barras(produto_id)

                    # Verificar se o código de barras gerado é único
                    while Produto.objects.filter(codigo_barras=codigo_barras).exists():
                        produto_id += 1
                        codigo_barras = gerar_codigo_barras(produto_id)
                    produto.codigo_barras = codigo_barras
            else:
                produto = Produto.objects.get(id=pk)
                form = ProdutoForm(request.POST, instance=produto)
                if form.is_valid():
                    produto = form.save(commit=False)
                    produto_id = (
                        produto.id if produto.id else Produto.objects.count() + 1
                    )
                    codigo_barras = gerar_codigo_barras(produto_id)

                    # Verificar se o código de barras gerado é único
                    while Produto.objects.filter(codigo_barras=codigo_barras).exists():
                        produto_id += 1
                        codigo_barras = gerar_codigo_barras(produto_id)
                    produto.codigo_barras = codigo_barras
            form.save()
            form = ProdutoForm()
        elif "delete" in request.POST:
            pk = request.POST.get("delete")
            produto = Produto.objects.get(id=pk)
            try:
                produto.delete()
            except:
                context["error"] = (
                    "Não é possível deletar esse produto porque ele se encontra em estoque"
                )
        elif "edit" in request.POST:
            pk = request.POST.get("edit")
            produto = Produto.objects.get(id=pk)
            form = ProdutoForm(instance=produto)
    context["form"] = form
    return render(request, "produtos/list.html", context)


def estoque(request):
    context = {}
    form = EstoqueForm()
    context["title"] = "Estoque"
    estoque = Estoque.objects.all()
    context["estoque"] = estoque
    if request.method == "POST":
        if "save" in request.POST:
            pk = request.POST.get("save")
            if not pk:
                form = EstoqueForm(request.POST)
            else:
                estoque = Estoque.objects.get(id=pk)
                form = EstoqueForm(request.POST, instance=estoque)
            form.save()
            form = EstoqueForm()
        elif "delete" in request.POST:
            pk = request.POST.get("delete")
            estoque = Estoque.objects.get(id=pk)
            try:
                estoque.delete()
            except:
                context["error"] = "Não é possível deletar essa entrada no estoque"
        elif "edit" in request.POST:
            pk = request.POST.get("edit")
            estoque = Estoque.objects.get(id=pk)
            estoque.data_vencimento = str(estoque.data_vencimento)
            form = EstoqueForm(instance=estoque)
    context["form"] = form
    return render(request, "estoque/list.html", context)


def relatorio(request):
    context = {}

    # Dicionário de nomes dos meses
    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    # Obter os itens de entrada e saída do estoque agrupados por mês
    entradas_por_mes = defaultdict(lambda: defaultdict(int))
    saidas_por_mes = defaultdict(lambda: defaultdict(int))

    # Obter entradas por mês
    itens_entrada = (
        Estoque.objects.filter(acao="ENT")
        .annotate(mes=ExtractMonth("data_controle"))
        .values("produto__id", "mes", "produto__descricao")
        .annotate(total_quantidade=Sum("quantidade"))
    )

    for item in itens_entrada:
        produto_nome = item["produto__descricao"]
        mes = meses[item["mes"]]
        quantidade = item["total_quantidade"]
        entradas_por_mes[produto_nome][mes] += quantidade

    # Obter saídas por mês
    itens_saida = (
        Estoque.objects.filter(acao="SAI")
        .annotate(mes=ExtractMonth("data_controle"))
        .values("produto__id", "mes", "produto__descricao")
        .annotate(total_quantidade=Sum("quantidade"))
    )

    for item in itens_saida:
        produto_nome = item["produto__descricao"]
        mes = meses[item["mes"]]
        quantidade = item["total_quantidade"]
        saidas_por_mes[produto_nome][mes] += quantidade

    # Calcular o saldo (ENT - SAI) para cada produto por mês
    saldo_por_produto = defaultdict(lambda: defaultdict(int))
    for produto_nome in set(entradas_por_mes.keys()).union(saidas_por_mes.keys()):
        for mes in set(entradas_por_mes[produto_nome].keys()).union(
            saidas_por_mes[produto_nome].keys()
        ):
            saldo_por_produto[produto_nome][mes] = (
                entradas_por_mes[produto_nome][mes] - saidas_por_mes[produto_nome][mes]
            )

    # Calcular o saldo total por produto
    saldo_total_por_produto = {
        produto: sum(saldos.values()) for produto, saldos in saldo_por_produto.items()
    }

    # Criar lista de itens do relatório usando a view model
    itens_relatorio = []
    for produto_nome, meses_saldo in saldo_por_produto.items():
        for mes, saldo in meses_saldo.items():
            total_entrada = entradas_por_mes[produto_nome][mes]
            total_saida = saidas_por_mes[produto_nome][mes]
            itens_relatorio.append(
                ItemRelatorioViewModel(
                    produto=produto_nome,
                    mes=mes,
                    total_entrada=total_entrada,
                    total_saida=total_saida,
                    saldo=saldo,
                )
            )

    # Ordenar os itens do relatório por mês, produto e quantidade
    itens_relatorio.sort(
        key=lambda item: (
            list(meses.keys())[list(meses.values()).index(item.mes)],
            item.produto,
            item.saldo,
        )
    )

    # Passar os dados para o template
    context["itens_relatorio"] = itens_relatorio
    context["saldo_total_por_produto"] = saldo_total_por_produto

    return render(request, "relatorio/list.html", context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Produto, Estoque


@csrf_exempt  # Use proteção CSRF correta em produção
def processar_estoque(request):
    if request.method == "POST" and request.FILES.get("image"):
        barcode = request.POST.get("barcode")
        acao = request.POST.get("acao")  # 'ENT' para entrada e 'SAI' para saída
        image_file = request.FILES["image"]

        # Salva a imagem temporariamente
        temp_image_path = os.path.join(gettempdir(), image_file.name)
        with open(temp_image_path, "wb+") as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        try:
            # Busca o produto pelo código de barras
            reader = zxing.BarCodeReader()
            barcode = reader.decode(temp_image_path)

            # Remove o arquivo temporário após a leitura
            os.remove(temp_image_path)

            produto = get_object_or_404(Produto, codigo_barras=barcode)

            if barcode:
                logger.info(f"Código de barras detectado: {barcode.parsed}")
                return JsonResponse({"status": "success", "barcode": barcode.parsed})
                # Realiza a operação de entrada ou saída
                if acao == "ENT":
                    # Lógica para entrada de estoque
                    Estoque.objects.create(produto=produto, quantidade=1, acao="ENT")
                elif acao == "SAI":
                    # Lógica para saída de estoque
                    Estoque.objects.create(produto=produto, quantidade=1, acao="SAI")
                return JsonResponse(
                    {
                        "status": "success",
                        "message": f"Operação '{acao}' realizada para o produto: {produto.descricao}",
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "message": "No barcode detected"}, status=400
                )

        except Exception as e:
            logger.error(f"Erro ao processar o código de barras: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to decode barcode"}, status=500
            )
        except Produto.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Produto não encontrado"}, status=404
            )
    return JsonResponse(
        {"status": "error", "message": "Método não permitido"}, status=405
    )


# método antigo q só le o código de barras


@csrf_exempt  # Certifique-se de usar a proteção CSRF em produção corretamente
def process_barcode_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]

        # Salva a imagem temporariamente
        temp_image_path = os.path.join(gettempdir(), image_file.name)
        with open(temp_image_path, "wb+") as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Processa a imagem com ZXing
        try:
            reader = zxing.BarCodeReader()
            barcode = reader.decode(temp_image_path)

            # Remove o arquivo temporário após a leitura
            os.remove(temp_image_path)

            if barcode:
                logger.info(f"Código de barras detectado: {barcode.parsed}")
                return JsonResponse({"status": "success", "barcode": barcode.parsed})
            else:
                return JsonResponse(
                    {"status": "error", "message": "No barcode detected"}, status=400
                )

        except Exception as e:
            logger.error(f"Erro ao processar o código de barras: {str(e)}")
            return JsonResponse(
                {"status": "error", "message": "Failed to decode barcode"}, status=500
            )

    # Caso não seja um POST com uma imagem, retorna erro
    return JsonResponse(
        {"status": "error", "message": "Invalid request method or no image provided"},
        status=405,
    )


def exibir_webcam(request):
    return render(request, "estoque/webcam.html")
