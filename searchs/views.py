from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.http import HttpResponse

# Create your views here.
from itertools import chain
from django.views.generic import ListView
from oorax.models import *


class SearchView(ListView):
    template_name = 'search/view.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            cour_results        = Cour.objects.search(query)
            #annonce_results      = Annonce.objects.search(query=query)
            #pharma_results     = Pharmacie.objects.search(query=query)

            # combine querysets
            queryset_chain = chain(
                    cour_results,
                    #annonce_results,
                    #pharma_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Cour.objects.none() # just an empty queryset as default

def search_form(request):
    return render(request, 'search/view.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if q == "Cour":
            print(q)
            cours = Cour.objects.all()
            return render(request, 'search/result.html',{'cours': cours,'query': q})
        elif q == "Annonce":
                print(q)
                annonces = Annonce.objects.all()
                return render(request, 'search/result.html',{'annonces': annonces,'query':q})
        else:
            return HttpResponse("no corresponding")
    else:
        message = 'invalid.'
    return HttpResponse(message)
