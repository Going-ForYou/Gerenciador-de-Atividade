from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from .forms import UserFormTemplate
from .models import Users
from django.contrib.auth import update_session_auth_hash
from .forms import PasswordChangeFormTemplate
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_permission_decorator
from django.core.mail import send_mail
from gerenciador.gerardor import gerar_senha

@login_required(login_url='login')
@has_permission_decorator('cadastro_interno')
def cadastro_usuario(request):
    if request.method == "GET":
        grupoForm = UserFormTemplate

        return render(request, 'cadastro_usuario.html', {"grupoForm": grupoForm})

    elif request.method == 'POST':
        email = request.POST.get('email')

        #Gerado de senha automatico
        senha = gerar_senha()
        print(senha)

        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        grupo = request.POST.get('grupo_de_acesso')

        print(grupo)

        #pegando do user da model e verficando se o email é igual
        user = Users.objects.filter(email=email)


        if user.exists():
            return HttpResponse('Email existe')

        #caso o usuario não exista crie ele
        #o username é obrigatorio ou seja como nossa inscrição é pelo email coloquei o email no username
        user = Users.objects.create_user(username=email, email=email, password=senha, grupo_de_acesso=grupo,
                                         first_name=nome, last_name=sobrenome)
        user.save()
        send_mail(f'Senha do Cadastro Avante', f'Sua conta no sistema avante foi cadastrada com sucesso!.\nSua senha é: {senha} \nentre e mude a sua senha para uma personalizada', 'pedro@programador.com.br',[f'{email}'])
        return HttpResponse('Conta Criada')


def login(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            #Se o usuario estiver autenticado nao precisa carregar o template login vai para cadastro usuario
            return redirect(reverse('cadastro_usuario'))
        return render(request, 'login.html')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            return redirect(reverse('cadastro_usuario'))

        email = request.POST.get('email')
        senha = request.POST.get('senha')
        #gerador de senha automatico user


        #passando os parametros para o user para ver se ele existe no banco
        user = auth.authenticate(username=email, password=senha)

        #Se o usuario for invalido ou seja nao achae ele no banco
        if not user:
            return HttpResponse('Usuario Invalido')#TODO coloar mensagem de erro

        print(user.last_login)
        if user.last_login is None:
            auth.login(request, user)
            form = PasswordChangeFormTemplate(request.user)
            return render(request,'primeiro_login.html', {'form': form})

        #SE existe
        auth.login(request, user)
        return redirect(reverse('cadastro_usuario'))

@login_required(login_url='login')
def alterar_senha(request):

    if request.method == 'GET':
        form = PasswordChangeFormTemplate(request.user)
        return render(request, 'primeiro_login.html', {'form': form})

    elif request.method == 'POST':
        form = PasswordChangeFormTemplate(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return redirect(reverse('cadastro_usuario'))

        else:
            return HttpResponse("primeiro_login.html")#TODO coloar mensagem de erro
    else:
        form = PasswordChangeFormTemplate(request.user)
        # Se o formulário não for válido, renderize o formulário novamente com os erros
        return render(request, 'primeiro_login.html', {'form': form})


#TODO linkar URL sair/ a um botão de logout
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))





