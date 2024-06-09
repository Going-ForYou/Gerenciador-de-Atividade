from django.shortcuts import render, get_object_or_404, redirect, reverse
from perfis.models import Users
from .forms import Inscrever_na_AtividadeForm, AtividadeForm, Usuario_ExternoForm, Lista_PrecencaForm, ServicoAtividadeForm
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required
from .models import Inscrever_na_Atividade, Atividade, Usuario_Externo,Servico,DiaAtividade
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError



# TODO Fazer Update e Delete dos usuarios Internos e Externo
@xframe_options_exempt
@login_required(login_url='login')
@has_permission_decorator('cadastro_externo')
def cadastro_externo(request):
    if request.method == 'GET':
        form = Usuario_ExternoForm()
        return render(request, 'cadastro_UserExterno.html', {'form': form})

    if request.method == 'POST':
        form = Usuario_ExternoForm(request.POST)

        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            usuario = Usuario_Externo.objects.filter(cpf=cpf)

            if usuario.exists():
                messages.add_message(request, messages.ERROR, 'Usuario ja existe!')
                return render(request, 'cadastro_UserExterno.html', {'form': form})

            form.save()
            messages.add_message(request, messages.SUCCESS, 'Usuario Externo cadastrado com sucesso!')
            return redirect(reverse('cdE'))

        else:
            messages.add_message(request, messages.ERROR,
                                 'Erro ao cadastrar usuario externo. Verifique os dados e tente novamente.')
            return render(request, 'cadastro_UserExterno.html', {'form': form})


'''SAMUEL ESTEVE AQUI  Atualizar usuario Externo'''
@login_required(login_url='login')
@has_permission_decorator('cadastro_externo')
def update_usuario_externo(request, pk):
    usuario = get_object_or_404(Usuario_Externo, pk=pk)
    if request.method == 'POST':
        form = Usuario_ExternoForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Usuário Externo atualizado com sucesso!')
            return redirect(reverse('update_usuario_externo', args=[pk]))
    else:
        form = Usuario_ExternoForm(instance=usuario)
    return render(request, 'update/update_usuario_externo.html', {'form': form, 'usuario': usuario})
#ATÈ AQUI


@xframe_options_exempt
@login_required(login_url='login')
@has_permission_decorator('cadastro_atividade')
def cadastro_atividade(request):
    if request.method == 'GET':
        form = AtividadeForm()
        return render(request, 'cadastro_atividade_aula/cadastro_atividade_aula.html', {'form': form})

    elif request.method == 'POST':
        form = AtividadeForm(request.POST)

        if form.is_valid():
            atividade = form.save(commit=False)
            form.save_m2m()
            atividade.save()
            messages.add_message(request, messages.SUCCESS, 'Atividade cadastrada com sucesso!')
            return redirect(reverse('cdA'))
        else:
            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro ao cadastrar')
            return render(request, 'cadastro_atividade_aula/cadastro_atividade_aula.html', {'form': form})


@xframe_options_exempt
@login_required(login_url='login')
@has_permission_decorator('cadastro_atividade')
def cadastro_servico(request):
    if request.method == 'GET':
        form = ServicoAtividadeForm()
        return render(request, 'cadastro_atividade_servicos/cadastro_atividade_servicos.html', {'form': form})

    elif request.method == 'POST':
        form = ServicoAtividadeForm(request.POST)
        if form.is_valid():

            dia_atividade = form.cleaned_data['dia_atividade']
            responsavel = form.cleaned_data['responsavel']
            if Servico.objects.filter(dia_atividade=dia_atividade, responsavel=responsavel).exists():
                messages.add_message(request, messages.ERROR, 'Já existe um serviço cadastrado para esse responsável nesse dia')
                return render(request, 'cadastro_atividade_servicos/cadastro_atividade_servicos.html', {'form': form})

            form.save()
            messages.add_message(request, messages.SUCCESS, 'Atividade cadastrada com sucesso!')
            return redirect(reverse('cdS'))
        else:
            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro ao cadastrar')
            return render(request, 'cadastro_atividade_servicos/cadastro_atividade_servicos.html', {'form': form})


# UPDATE---------------------------------------------------------------
@xframe_options_exempt
@login_required(login_url='login')
@has_permission_decorator('cadastro_externo')
def update_aula(request, id):
    atividade = get_object_or_404(Atividade, pk=id)
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)
        print(form)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Atividade atualizada com sucesso!')
            return redirect(reverse('update_aula', args=[id]))
    else:
        form = AtividadeForm(instance=atividade)
    return render(request, 'update/update_aula.html', {'form': form, 'atividade': atividade})


@xframe_options_exempt
@login_required(login_url='login')
def update_servico(request,id):
    servico = get_object_or_404(Servico, pk=id)
    if request.method == 'POST':
        form = ServicoAtividadeForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect(reverse(update_servico, args=[id]))
    else:
        form = ServicoAtividadeForm(instance=servico)

    return render(request, 'update/update_servico.html', {'form': form, 'servico': servico})

# ---------------------------------------------------------------------


@login_required(login_url='login')
@has_permission_decorator('cadastro_inscricao')
def inscricao(request):
    if request.method == 'GET':
        form = Inscrever_na_AtividadeForm()
        responsaveis = Users.objects.filter(is_superuser=False)
        return render(request, 'inscricao.html', {'form': form, 'responsaveis': responsaveis})

    elif request.method == 'POST':
        form = Inscrever_na_AtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Inscrição realizada com sucesso!')
            return redirect(reverse('lista_inscricao'))
        else:
            messages.add_message(request, messages.ERROR, 'Erro ao realizar inscrição. Verifique os dados e tente novamente.')
            return render(request, 'inscricao.html', {'form': form})



@login_required(login_url='login')
@has_permission_decorator('lista_presenca')
def menu_atividade(request):
    atividades = Atividade.objects.filter(responsavel=request.user)
    return render(request, 'menu_atividade.html', {'atividades': atividades})


@login_required(login_url='login')
@has_permission_decorator('lista_de_atividade')
def lista_presenca(request, atividade_id):
    atividade = get_object_or_404(Atividade, pk=atividade_id, responsavel=request.user)
    alunos = Inscrever_na_Atividade.objects.filter(atividade=atividade)
    form = Lista_PrecencaForm()
    return render(request, 'precenca.html', {'form': form, 'alunos': alunos})

#TODO Ver as permissões
# lista---------------------------------------------------------------

@cache_page(60)
@login_required(login_url='login')
def lista_usuario_interno(request):
    internoList = Usuario_Externo.objects.all()
    return render(request, 'lista/listagemUsuariosInternos.html', {'internoList': internoList})



@cache_page(60)
@login_required(login_url='login')
def lista_usuario_externo(request):
    externoList = Usuario_Externo.objects.all()
    return render(request, 'lista/listagemUsuariosExternos.html', {'externoList': externoList})


@xframe_options_exempt
@login_required(login_url='login')
def lista_aula(request):
    pesquisa = request.GET.get('pesquisa')

    if pesquisa:
        aulaList = Atividade.objects.all()
        aulaList = aulaList.filter(nome_atividade__icontains=pesquisa)


    else:
        aulaList = Atividade.objects.all()

    return render(request, 'lista/listagemAulas.html', {'aulaList': aulaList})


@xframe_options_exempt
@login_required(login_url='login')
def lista_servico(request):
    pesquisa = request.GET.get('pesquisa')

    if pesquisa:

        servicoList = Servico.objects.all()
        servicoList = servicoList.filter(nome_servico__icontains=pesquisa)

    else:
        servicoList = Servico.objects.all()

    return render(request, 'lista/listagemServicos.html', {'servicoList': servicoList})


@login_required(login_url='login')
def lista_inscricao(request):
    inscrito = Inscrever_na_Atividade.objects.all()
    return render(request, 'lista/lista_inscricao.html', {'inscrito': inscrito})


# ---------------------------------------------------------------------


# Delete---------------------------------------------------------------

@login_required(login_url='login')
@has_permission_decorator('cadastro_interno')
def deletar_cliente(request, slug):
    usuario = get_object_or_404(Usuario_Externo, slug=slug)
    form = Usuario_ExternoForm(request.POST or None, instance=usuario)

    if request.method == 'POST':
        usuario.delete()
        messages.add_message(request, messages.SUCCESS, 'Deletado com Sucesso')
        return redirect(reverse('lista'))

    return render(request, 'delete/deletar_externo.html', {'form': form})


@login_required(login_url='login')
@has_permission_decorator('cadastro_interno')
@require_POST
def deletar_aula(request, id):
    atividade = get_object_or_404(Atividade, id=id)
    atividade.delete()
    return JsonResponse({'message': 'Aula deletada com sucesso!'})


@login_required(login_url='login')
@has_permission_decorator('cadastro_interno')
@require_POST
def deletar_servico(request, id):
    servico = get_object_or_404(Servico, id=id)
    servico.delete()
    return JsonResponse({'message': 'Serviço deletado com sucesso!'})


@has_permission_decorator('cadastro_interno')
@login_required(login_url='login')
def deletar_inscricao(request, id):
    inscricao = get_object_or_404(Inscrever_na_Atividade, pk=id)
    form = Inscrever_na_AtividadeForm(request.POST or None, instance=inscricao)
    if request.method == 'POST':
        inscricao.delete()
        messages.add_message(request, messages.SUCCESS, 'Inscricao deletada com Sucesso')
        return redirect(reverse('deletar_inscricao'))

    return render(request, 'delete/deletar_inscricao.html', {'form': form})

# ---------------------------------------------------------------------


