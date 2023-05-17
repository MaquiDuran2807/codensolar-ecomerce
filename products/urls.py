from django.urls import path
from .views import *

app_name = 'Products_app'

urlpatterns = [
    path('all', ProductView.as_view(), name='products-all'),
    path('cotizacion', CotizacionView.as_view(), name='cotizacion'),
    path('pdf', PdfView.as_view(), name='pdf'),
    path('pdf-page', PdfViewPage.as_view(), name='pdf'),
    path('quote', PdfViewPage.as_view(), name='pdfPage'),
    path('sendQuote', SendEmail.as_view(), name='email'),
    #path('products/<int:id>', ProductListView.as_view(), name='products'),
    # -----
    path('get/<str:obj>/<int:id>', GetObj.as_view(), name='get'),
    # -----
    path('shopping_car/<int:id>', ShoppingCar.as_view(), name='shopping_car'),
    path('vista_prueba', vistaprueba.as_view(), name='vista_prueba'),
    path('pdf_vista',PdfViewPage.as_view(), name='pdf_vista'),
    path('gen_pdf', GeneratePdf.as_view(), name='gen_pdf'),
]