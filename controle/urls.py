from .views import index, criar_projeto, editar_projeto, excluir_projeto
from .views import projeto, criar_analise, editar_analise, excluir_analise  
from .views import analise, criar_amostra, editar_amostra, excluir_amostra
from django.urls import path
from django.contrib.auth import views as auth_views
from .admin import admin_site

urlpatterns =[
    path('', index, name="index"),
    
    path('adicionar_projeto/', criar_projeto, name="adicionar_projeto" ),
    path('editar_projeto/<int:id>/', editar_projeto, name="editar_projeto" ),
    path('excluir_projeto/<int:id>/', excluir_projeto, name="excluir_projeto" ),
    #Analises
    path('projeto/<int:id>/', projeto, name="analise" ),
    path('criar_analise/<int:projeto_id>/', criar_analise, name="criar_analise"),
    path('projeto/<int:projeto_id>/editar_analise/<int:id>/', editar_analise, name="editar_analise"),
    path('projeto/<int:projeto_id>/excluir_analise/<int:id>/', excluir_analise, name="excluir_analise"),
    path('projeto/<int:projeto_id>/analise/<int:id>/', analise, name="amostras"),
    path('projeto/<int:projeto_id>/analise/<int:analise_id>/criar_amostra/', criar_amostra, name="criar_amostra"),
    path('projeto/<int:projeto_id>/analise/<int:analise_id>/editar_amostra/<int:id>/', editar_amostra, name="criar_amostra"),
    path('projeto/<int:projeto_id>/analise/<int:analise_id>/excluir_amostra/<int:id>/', excluir_amostra, name="excluir_amostra"),
    
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('acesso_negado/', index, name='acesso_negado'),
    path('admin/', admin_site.urls),
]