from django.views.generic import (TemplateView, DetailView, ListView, CreateView)
from django.db.models import Q, Sum
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from inec_app.util_function import extra_context
from inec_app.models import PollingUnit, AnnouncedPuResults, Lga, States
from inec_app.forms import AnnouncedPuResultsForm


# Create your views here.
class IndexView ( TemplateView ):
    name = 'index'
    template_name = 'inec_app/index.html'
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        return extra_context ( context, 'Home' )



def get_sum ( request ):
    
    lga_id = request.GET.get('lga')
    pu_results = []
    count = 0
    
    if lga_id:
        try:
            # get all PU in local govt
            polling_units_lga = PollingUnit.objects.filter(lga_id = lga_id)
            queryset = None
            
            # get all polling unit results
            for polling_unit in polling_units_lga:
                announced_pu_results = AnnouncedPuResults.objects.filter( polling_unit_uniqueid = polling_unit.uniqueid)
                
                if queryset is None:
                    queryset = announced_pu_results
                else:
                    queryset = queryset | announced_pu_results
                
                
                for announced_pu_result in announced_pu_results:
                    count += int(announced_pu_result.party_score)
                    
                    
        except (PollingUnit.DoesNotExist, AnnouncedPuResults.DoesNotExist):
            queryset = ''
            count = 0
        
        if queryset is not None:
            queryset = zip(list(queryset), list(polling_units_lga))
            
    total_results = count

    context = { 'total_results' : total_results, 'pu_results' : queryset }
    return render ( request, 'inec_app/summed_total.html', context )



def load_lga ( request ):
    state_id = request.GET.get('state')
    
    if state_id:
        try:
            lgas = Lga.objects.filter(state_id = state_id).order_by('lga_name')
        except Lga.DoesNotExist:
            lgas = None
            
    return render ( request, 'inec_app/lga_drop_down_list.html', { 'lga' : lgas } )


    
class Question1View ( ListView ):
    name = 'question1'
    template_name = 'inec_app/question1.html'
    queryset = PollingUnit.objects.filter(polling_unit_number__icontains='DT').order_by('polling_unit_name')
    context_object_name = 'polling_units'
    paginate_by = 5
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        
        try:
            context['pu_count'] = self.queryset.count()
        except PollingUnit.DoesNotExist:
            context['pu_count'] = 0
            
        return extra_context ( context, 'Question 1' )
    
    
    
class Question1ResultView ( DetailView ):
    name = 'question1_result'
    template_name = 'inec_app/question1_result.html'
    context_object_name = 'polling_unit'
    model = PollingUnit
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        
        try:
            context['pu_results'] = AnnouncedPuResults.objects.filter(polling_unit_uniqueid__iexact = str(self.model.objects.get(uniqueid = self.kwargs['pk']).uniqueid))
        except (AnnouncedPuResults.DoesNotExist, PollingUnit.DoesNotExist):
            context['pu_results'] = None
            
        return extra_context ( context, 'Question 1 - Result' )
    
    
    
class Question2View ( TemplateView ):
    name = 'question2'
    template_name = 'inec_app/question2.html'
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        
        try:
            context['states'] = States.objects.all().order_by('state_name')
            state_id = States.objects.get(state_name = 'Abia').state_id
            context['lga'] = Lga.objects.filter(state_id = state_id).order_by('lga_name')
        except (Lga.DoesNotExist, States.DoesNotExist):
            context['states']  = None
            context['lga'] = None
        
        return extra_context ( context, 'Question 2' )
    
    
    
class Question3View ( CreateView ):
    name = 'question3'
    template_name = 'inec_app/question3.html'
    model = AnnouncedPuResults
    form_class = AnnouncedPuResultsForm
    success_url = reverse_lazy('inec_app:question3')
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        return extra_context ( context, 'Question 3' )
    
    def form_valid ( self, form ):
        flash_message = 'Data successfully entered!'
        messages.success( self.request,  flash_message )
        return  super().form_valid( form )
    
    

class PollingUnitSearchView ( ListView ):
    template_name = 'inec_app/search_result.html'
    name = 'search'
    context_object_name = 'polling_units'
    paginate_by = 5
    
    def get_context_data ( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        context['q'] = self.request.GET['q']
        return extra_context ( context, 'Search' )

    def get_queryset ( self ):
        try:
            name = self.request.GET['q']
        except:
            name = ''
            
        if name != '':
            object_list = PollingUnit.objects.filter(
                Q ( polling_unit_name__icontains = name ) | Q ( polling_unit_number__icontains = name )
            )
        else:
            object_list = PollingUnit.objects.all()
            self.paginate_by = 50
            
        return object_list