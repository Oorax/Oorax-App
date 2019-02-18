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
            cour_results = Cour.objects.search(query)
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
        list_cour=[]
        list_result=[]
        cours=Cour.objects.all()

        for cr in cours:
            list_cour.append(cr.titre)

        print('deco', list_cour)
        nom_comm=[]

        if q in list_cour:
            cours = Cour.objects.filter(titre=q)
            comm=Commentaire.objects.all()
            for com in comm:
                for c in cours:
                    if com.cour_comment_id is c.id:
                        nom_comm.append(com.cour_comment_id)
            cat = Categorie.objects.all()
            dom = Domaine.objects.all()
            auteur=CustomUser.objects.all()
            print(len(nom_comm))
            inscrip = Inscrit.objects.all()
            liste_inscri = []
            for ins in inscrip:
                liste_inscri.append(ins.cour_id)

            return render(request, 'search/result.html',{'liste_inscri':liste_inscri,'auteur':auteur,'dom':dom,'cat':cat,'comm':comm,'nom_comm':nom_comm,'cours': cours,'query': q})

        elif q not in list_cour:
            decoup=(q.split())
            print('decoup',decoup)
            for x in decoup:
                if x in list_cour:
                    print('1', x)
                    list_result.append(x)
            cour = Cour.objects.all()
            auteur = CustomUser.objects.all()
            inscrip=Inscrit.objects.all()
            liste_inscri=[]
            for ins in inscrip:
                liste_inscri.append(ins.cour_id)

            return render(request, 'search/result.html', {'liste_inscri':liste_inscri,'auteur':auteur,'list_result': list_result,'cour':cour, 'query': q})
        else:
            return HttpResponse("no corresponding")

    else:
        message = 'invalid.'
        return HttpResponse(message)

def inscription(request,id):
    cour = Cour.objects.get(id=id)
    #service = Service.object.all()

    id = cour.id
    titre=cour.titre
    prix=cour.prix
    return render(request, "registration/achat_lesson.html",{'titre':titre,'prix':prix,'id':id})

