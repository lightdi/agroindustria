from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Amostra, Projeto, Analise, Usuario
from .models import PermissaoAmostra, PermissaoAnalise, PermissaoProjeto
from django.shortcuts import redirect

# Substituindo o comportamento do login do Django Admin
class CustomAdminSite(admin.AdminSite):
    def login(self, request, extra_context=None):
        user = request.user
        if not user.is_authenticated or not user.administrador:
            return redirect('acesso_negado')  # Redireciona para uma página de acesso negado
        return super().login(request, extra_context)
    


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    """Classe base para definir automaticamente os usuários de criação e atualização"""
    exclude = ("criado_por", "atualizado_por")  # Oculta os campos no formulário

    def save_model(self, request, obj, form, change):
        """Define automaticamente os campos de usuário ao salvar"""
        if not obj.pk:  # Se for um novo objeto
            obj.criado_por = request.user
        obj.atualizado_por = request.user  # Sempre atualizado pelo usuário atual
        super().save_model(request, obj, form, change)
# Criando um site admin personalizado
admin_site = CustomAdminSite(name='custom_admin')

# Administração do modelo Projeto
admin_site.register(Projeto)
class ProjetoAdmin(BaseAdmin):
    list_display = ("nome", "ativo", "data", "criado_por", "atualizado_por")

# Administração do modelo Analise
admin_site.register(Analise)
class AnaliseAdmin(BaseAdmin):
    list_display = ("nome", "projeto", "criado_por", "atualizado_por")

# Administração do modelo Amostra
admin_site.register(Amostra)
class AmostraAdmin(BaseAdmin):
    list_display = ("nome", "analise", "peso_cap_vazia", "amostra_inicial", "peso_final", "umidade", "criado_por", "atualizado_por")


class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ("Permissões Personalizadas", {"fields": ("administrador",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Permissões Personalizadas", {"fields": ("administrador",)}),
    )

admin_site.register(Usuario, CustomUserAdmin)

admin_site.register(PermissaoProjeto)

