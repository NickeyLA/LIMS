from django.urls import path
from .views import lab_xa_page
from .views import get_probe_data
from .views import save_analysis
from .views import delete_analysis_results_by_probe_indicator

urlpatterns = [
    path('', lab_xa_page, name="lab_xa_page"),
    path('get_probe_data/<int:probe_id>/', get_probe_data, name='get_probe_data'),
    path('save_analysis/', save_analysis, name='save_analysis'),
    path('delete-analysis-results/', delete_analysis_results_by_probe_indicator, name='delete_analysis_results'),
]