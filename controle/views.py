from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projeto, Amostra, Analise
from .forms import ProjetoForm, AnaliseForm, AmostraForm

# Create your views here.

@login_required
def index(request):
    # Se o usuário for administrador, ele pode ver todos os projetos
    if request.user.administrador:
        projetos = Projeto.objects.all().order_by('-ativo','-data')
    else:
        # Caso contrário, busca projetos onde o usuário é o criador ou onde ele tem permissão de visualização
        projetos = Projeto.objects.filter(
            criado_por=request.user
        ) | Projeto.objects.filter(
            permissaoprojeto__usuario=request.user, 
            permissaoprojeto__pode_visualizar=True
        ).order_by('-ativo','-data')

    return render(request, "index.html", {"projetos": projetos})

@login_required
def criar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            # Passa o usuário logado para o formulário ao salvar
            form.save(usuario=request.user)  # O usuário logado é passado aqui
            return redirect('index')  # Redireciona para a lista de projetos ou outro local
    else:
        form = ProjetoForm()

    return render(request, 'criar_projeto.html', {'form': form})

@login_required
def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            # Atribui o usuário logado ao campo 'alterado_por'
            projeto = form.save(commit=False)  # Não salva automaticamente
            projeto.alterado_por = request.user  # Atribui o usuário logado
            projeto.save()  # Salva o projeto com a alteração do usuário
            return redirect('index')  # Redireciona para a lista de projetos
    else:
        print(projeto.data)
        form = ProjetoForm(instance=projeto)
        form.fields['data'].initial = '2020-11-11'#projeto.data.strftime('%Y-%m-%d')
        print(form.fields['data'].initial)

    return render(request, 'editar_projeto.html', {'form': form, 'projeto': projeto})

@login_required
def excluir_projeto(request, id):
    # Verifica se o usuário é administrador
    if not request.user.administrador:
        messages.error(request, "Você não tem permissão para excluir projetos.")
        return redirect('index')  # Redireciona de volta para a página inicial ou outra página desejada

    projeto = get_object_or_404(Projeto, id=id)

    # Exclui o projeto
    projeto.delete()

    messages.success(request, "Projeto excluído com sucesso.")
    return redirect('index')


##Carregand os dados do projeto
@login_required
def projeto(request, id):
    analises = Analise.objects.all().filter(projeto_id = id ).order_by('-id')
    return render(request, "projeto.html", {"analises": analises, "projeto_id": id})


@login_required
def criar_analise(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)  # Obtém o projeto
    if request.method == "POST":
        form = AnaliseForm(request.POST, projeto=projeto)  # Passa o projeto
        if form.is_valid():
            form.save(usuario=request.user)  # Passa o usuário logado
            return redirect('analise', id=projeto.id)  # Redireciona
    else:
        form = AnaliseForm(projeto=projeto)  # Passa o projeto ao formulário

    return render(request, 'criar_analise.html', {'form': form, 'projeto': projeto})

@login_required
def editar_analise(request, projeto_id,id):
    analise = get_object_or_404(Analise, id=id)

    if request.method == 'POST':
        form = AnaliseForm(request.POST, instance=analise)
        if form.is_valid():
            # Atribui o usuário logado ao campo 'alterado_por'
            analise = form.save(commit=False)  # Não salva automaticamente
            analise.alterado_por = request.user  # Atribui o usuário logado
            analise.save()  # Salva o projeto com a alteração do usuário
            return redirect('analise', id=projeto_id)  # Redireciona    s
    else:
        
        form = AnaliseForm(instance=analise)
        

    return render(request, 'editar_analise.html', {'form': form, 'analise': analise})

@login_required
def excluir_analise(request, projeto_id, id):

    analise = get_object_or_404(Analise, id=id)

    # Exclui o projeto
    analise.delete()

    messages.success(request, "Projeto excluído com sucesso.")
    return redirect('analise', id=projeto_id)  # Redireciona    

@login_required
def analise(request, projeto_id,id):
    amostras = Amostra.objects.all().filter(analise_id = id ).order_by('-id')
    return render(request, "amostra.html", {"amostras": amostras, "projeto_id": projeto_id, "analise_id": id})

@login_required
def criar_amostra(request, projeto_id,analise_id):
    analise = get_object_or_404(Analise, id=analise_id)  # Obtém a análise

    if request.method == "POST":
        form = AmostraForm(request.POST, analise=analise)  # Passa a análise ao formulário
        if form.is_valid():
            form.save(usuario=request.user)  # Passa o usuário logado
            return redirect('amostras', projeto_id = projeto_id, id=analise.id)  # Redireciona após salvar
    else:
        form = AmostraForm(analise=analise)  # Passa a análise ao formulário

    return render(request, 'criar_amostra.html', {'form': form, 'analise': analise, 'projeto_id': projeto_id, 'analise_id': analise_id})

@login_required
def editar_amostra(request, projeto_id, analise_id, id):
    amostra = get_object_or_404(Amostra, id=id)

    if request.method == 'POST':
        form = AmostraForm(request.POST, instance=amostra)
        if form.is_valid():
            # Atribui o usuário logado ao campo 'alterado_por'
            amostra = form.save(commit=False)  # Não salva automaticamente
            amostra.alterado_por = request.user  # Atribui o usuário logado
            amostra.save()  # Salva o projeto com a alteração do usuário
            return redirect('amostras', projeto_id = projeto_id, id=analise_id)  # Redireciona após salvar
    else:
        form = AmostraForm(instance=amostra)

    return render(request, 'editar_amostra.html', {'form': form, 'amostra': amostra, 'projeto_id': projeto_id, 'analise_id': analise_id})

@login_required
def excluir_amostra(request, projeto_id,analise_id, id):


    projeto = get_object_or_404(Amostra, id=id)

    # Exclui o projeto
    projeto.delete()

    messages.success(request, "Projeto excluído com sucesso.")
    return redirect('amostras', projeto_id = projeto_id, id=analise_id)  # Redireciona após salvar

def acesso_negado(request):
    return render(request, 'acesso_negado.html')