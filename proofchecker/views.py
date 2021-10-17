from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ProofForm
from .models import Proof


# Create your views here.
def home(request):
    proofs = Proof.objects.all()
    context = {"proofs": proofs}
    return render(request, "proofchecker/home.html", context)


# class HomeView(TemplateView):
#     template_name = "proofchecker/home.html"
#
#     def get_context_data(self):
#         context = super().get_context_data()
#         context["proofs"] = Proof.objects.all()
#         return context


class ProofView(ListView):
    model = Proof
    template_name = "proofchecker/allproofs.html"


class ProofCreateView(CreateView):
    model = Proof
    template_name = "proofchecker/add_proof.html"
    form_class = ProofForm


class ProofUpdateView(UpdateView):
    model = Proof
    template_name = "proofchecker/edit_proof.html"
    form_class = ProofForm


class PostDeleteView(DeleteView):
    model = Proof
    template_name = "proofchecker/delete_proof.html"
    success_url = "/allproofs/"
