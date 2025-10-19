from django import forms
from .models import Projeto, Analise, Amostra
from django.utils import timezone

class CustomDateInput(forms.DateInput):
    input_type = 'date'


    def render(self, name, value, attrs=None, renderer=None):
        if value:
            # Garantir que o valor esteja no formato 'YYYY-MM-DD'
            value = value.strftime('%Y-%m-%d')  # Formato correto para input[type="date"]
        return super().render(name, value, attrs, renderer)
    

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'data', 'ativo']  # Campos que você quer permitir que o usuário preencha
    
    # Adicionando classes de Bootstrap aos campos do formulário
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    descricao = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    #initial=timezone.localtime(timezone.now()).date().strftime('%Y-%m-%d'),
    data = forms.DateField(  initial=timezone.now().date(), widget=CustomDateInput(attrs={'class': 'form-control', 'type': 'date'}))
    ativo = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    


    
    def save(self, *args, **kwargs):
        # Preenche o campo 'criado_por' com o usuário logado antes de salvar
        usuario = kwargs.pop('usuario', None)  # Pega o usuário passado como argumento
        instance = super(ProjetoForm, self).save(*args, **kwargs)  # Salva o projeto
        if usuario:
            instance.criado_por = usuario  # Associa o usuário ao campo 'criado_por'
            instance.save()  # Salva novamente com o campo 'criado_por' preenchido
        return instance
    

class AnaliseForm(forms.ModelForm):
    class Meta:
        model = Analise
        fields = ['nome']  # Apenas o campo 'nome' será preenchido pelo usuário
    
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.projeto = kwargs.pop('projeto', None)  # Recebe o projeto como argumento
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        instance = super().save(commit=False)  # Cria a instância, mas não salva ainda

        if usuario:
            instance.criado_por = usuario  # Define o usuário que criou a análise

        if self.projeto:
            instance.projeto = self.projeto  # Associa a análise ao projeto

        if commit:
            instance.save()  # Salva a instância no banco de dados

        return instance
    
class AmostraForm(forms.ModelForm):
    class Meta:
        model = Amostra
        fields = ['nome', 'peso_cap_vazia', 'amostra_inicial', 'peso_final']  # Campos que o usuário pode preencher

    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    peso_cap_vazia = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amostra_inicial = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    peso_final = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.analise = kwargs.pop('analise', None)  # Pega a análise passada na view
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Obtém o usuário logado
        instance = super().save(commit=False)  # Cria a instância sem salvar

        if usuario:
            instance.criado_por = usuario  # Define o usuário que criou a amostra
            instance.atualizado_por = usuario  # Inicialmente, o mesmo usuário

        if self.analise:
            instance.analise = self.analise  # Associa a amostra à análise correta

        if commit:
            instance.save()  # Salva no banco

        return instance