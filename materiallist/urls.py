from . import views
from django.urls import path

urlpatterns = [    
    path('',views.home_view),
    path('material_list', views.material_List),
    path('create_material', views.create_Material),
    path('material_update/<uuid:id>', views.material_Update),
    path('main_list/<uuid:id>', views. material_View),
    path('master_page',views.master_Page),
    path('Create_Method',views.create_method),
    path('transact_list/',views.transact_list,name="transact_list"),
    path('update/<str:id>', views.update_method)  
   
]