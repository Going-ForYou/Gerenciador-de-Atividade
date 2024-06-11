# Generated by Django 5.0.4 on 2024-06-11 02:56

import cadastro.validator
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaAtividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('Segunda-feira', 'Segunda-feira'), ('Terça-feira', 'Terça-feira'), ('Quarta-feira', 'Quarta-feira'), ('Quinta-feira', 'Quinta-feira'), ('Sexta-feira', 'Sexta-feira'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Externo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True, validators=[cadastro.validator.validate_nome])),
                ('cpf', models.CharField(max_length=14, validators=[cadastro.validator.validate_cpf], verbose_name='CPF')),
                ('nascimento', models.DateField()),
                ('responsavel_nome', models.CharField(blank=True, max_length=50, null=True, validators=[cadastro.validator.validate_nome])),
                ('responsavel_cpf', models.CharField(blank=True, max_length=14, null=True, validators=[cadastro.validator.validate_cpf])),
                ('telefone', models.CharField(max_length=15, validators=[cadastro.validator.validate_cpf])),
                ('endereco', models.CharField(max_length=80)),
                ('cidade', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=60, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_atividade', models.CharField(max_length=50, validators=[cadastro.validator.validate_nome])),
                ('descricao', models.TextField(blank=True)),
                ('limite_alunos', models.IntegerField(validators=[cadastro.validator.quantidade_turma], verbose_name='Limite de Alunos')),
                ('hora_atividade', models.TimeField(verbose_name='Hora da Aula')),
                ('responsavel', models.ForeignKey(blank=True, limit_choices_to={'is_superuser': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
                ('dia_atividade', models.ManyToManyField(to='cadastro.diaatividade')),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_servico', models.CharField(max_length=30, verbose_name='Nome do Servico')),
                ('descricao', models.TextField(verbose_name='Descrição do Serviço')),
                ('dia_atividade', models.DateField(blank=True, null=True)),
                ('hora_inicio', models.TimeField(verbose_name='Hora Inicio')),
                ('hora_intervalo', models.TimeField(verbose_name='Hora Intervalo')),
                ('hora_fim_atividade', models.TimeField(verbose_name='Hora Fim')),
                ('responsavel', models.ForeignKey(blank=True, limit_choices_to={'is_superuser': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserService', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inscrever_Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_servico', models.TimeField(verbose_name='Hora do Servico')),
                ('dia_servico', models.DateField()),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('servico_atividade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.servico', verbose_name='Nome do servico')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.usuario_externo', verbose_name='Aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Inscrever_Aula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_aula', models.TimeField(verbose_name='Hora da Aula')),
                ('nome_atividade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.atividade', verbose_name='Nome da Atividade')),
                ('responsavel', models.ForeignKey(blank=True, limit_choices_to={'is_superuser': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsavel', to=settings.AUTH_USER_MODEL)),
                ('nome_aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.usuario_externo', verbose_name='Nome do aluno')),
            ],
        ),
    ]
