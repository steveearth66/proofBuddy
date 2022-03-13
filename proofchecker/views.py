from accounts.decorators import instructor_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView,  DeleteView
from django.forms import inlineformset_factory
from proofchecker.forms import ProofForm, ProofLineForm
from proofchecker.models import Proof, Problem, ProofLine, Student, Course
from proofchecker.proofs.proofchecker import verify_proof
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj
from proofchecker.proofs.proofutils import get_premises
from proofchecker.utils import tflparser
from proofchecker.utils import folparser

from .forms import ProofCheckerForm, ProofForm, ProofLineForm, FeedbackForm
from .models import Proof, Problem, Assignment, Instructor, ProofLine, Feedback
from proofchecker.proofs.proofobjects import ProofObj, ProofLineObj, ProofResponse
from proofchecker.proofs.proofutils import get_premises
from proofchecker.proofs.proofchecker import verify_proof

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


def home(request):
    proofs = Proof.objects.all()
    context = {"proofs": proofs}
    return render(request, "proofchecker/home.html", context)


def SyntaxTestPage(request):
    return render(request, "proofchecker/testpages/syntax_test.html")


def proof_checker(request):
    ProofLineFormset = inlineformset_factory(
        Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    query_set = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(
        request.POST or None, instance=form.instance, queryset=query_set)
    response = None

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):

            parent = form.save(commit=False)

            if 'check_proof' in request.POST:
                # Create a new proof object
                proof = ProofObj(lines=[])

                # Grab premise and conclusion from the form
                # Assign them to the proof object
                proof.rules = str(parent.rules)
                proof.premises = get_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset.ordered_forms:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        # Create a proofline object
                        proofline = ProofLineObj()

                        # Grab the line_no, formula, and expression from the form
                        # Assign them to the proofline object
                        child = line.save(commit=False)
                        child.proof = parent

                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)

                        # Append the proofline to the proof object's lines
                        proof.lines.append(proofline)

                # Determine which parser to user based on selected rules
                if ((proof.rules == 'fol_basic') or (proof.rules == 'fol_derived')):
                    parser = folparser.parser
                else:
                    parser = tflparser.parser

                # Verify the proof!
                response = verify_proof(proof, parser)

                # Send the response back
                context = {
                    "form": form,
                    "formset": formset,
                    "response": response
                }

                return render(request, 'proofchecker/proof_checker.html', context)

    context = {
        "form": form,
        "formset": formset
    }
    return render(request, 'proofchecker/proof_checker.html', context)


@login_required
def proof_create_view(request):
    ProofLineFormset = inlineformset_factory(
        Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    query_set = ProofLine.objects.none()
    form = ProofForm(request.POST or None)
    formset = ProofLineFormset(
        request.POST or None, instance=form.instance, queryset=query_set)
    response = None

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)

            if 'check_proof' in request.POST:
                proof = ProofObj(lines=[])  #
                proof.rules = str(parent.rules)
                proof.premises = get_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset.ordered_forms:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        proofline = ProofLineObj()
                        child = line.save(commit=False)
                        child.proof = parent
                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)
                        proof.lines.append(proofline)

                # Determine which parser to user based on selected rules
                if ((proof.rules == 'fol_basic') or (proof.rules == 'fol_derived')):
                    parser = folparser.parser
                else:
                    parser = tflparser.parser

                response = verify_proof(proof, parser)

            elif 'submit' in request.POST:
                if len(formset.forms) > 0:
                    parent.created_by = request.user
                    parent.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('all_proofs'))

    context = {
        "object": form,
        "form": form,
        "formset": formset,
        "response": response
    }
    return render(request, 'proofchecker/proof_add_edit.html', context)


@login_required
def proof_update_view(request, pk=None):
    obj = get_object_or_404(Proof, pk=pk)
    ProofLineFormset = inlineformset_factory(
        Proof, ProofLine, form=ProofLineForm, extra=0, can_order=True)
    form = ProofForm(request.POST or None, instance=obj)
    formset = ProofLineFormset(
        request.POST or None, instance=obj, queryset=obj.proofline_set.order_by("ORDER"))
    response = None
    validation_failure = False

    if request.POST:
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            if 'check_proof' in request.POST:
                proof = ProofObj(lines=[])
                proof.rules = str(parent.rules)
                proof.premises = get_premises(parent.premises)
                proof.conclusion = str(parent.conclusion)

                for line in formset.ordered_forms:
                    if len(line.cleaned_data) > 0 and not line.cleaned_data['DELETE']:
                        proofline = ProofLineObj()
                        child = line.save(commit=False)
                        child.proof = parent
                        proofline.line_no = str(child.line_no)
                        proofline.expression = str(child.formula)
                        proofline.rule = str(child.rule)
                        proof.lines.append(proofline)

                # Determine which parser to user based on selected rules
                if ((proof.rules == 'fol_basic') or (proof.rules == 'fol_derived')):
                    parser = folparser.parser
                else:
                    parser = tflparser.parser

                response = verify_proof(proof, parser)

            elif 'submit' in request.POST:
                if len(formset.forms) > 0:
                    parent.created_by = request.user
                    parent.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('all_proofs'))

    context = {
        "object": obj,
        "form": form,
        "formset": formset,
        "response": response

    }
    return render(request, 'proofchecker/proof_add_edit.html', context)


class ProofView(LoginRequiredMixin, ListView):
    model = Proof
    template_name = "proofchecker/allproofs.html"
    paginate_by = 6

    def get_queryset(self):
        return Proof.objects.filter(created_by=self.request.user)


class ProofDetailView(DetailView):
    model = Proof


class ProofDeleteView(DeleteView):
    model = Proof
    template_name = "proofchecker/delete_proof.html"
    success_url = "/proofs/"


class ProblemView(ListView):
    model = Problem
    template_name = "proofchecker/problems.html"

def feedback_form(request):
    if request.POST:
        form = FeedbackForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            details = form.cleaned_data.get('details')
            subject = form.cleaned_data.get('subject')
            attach = request.FILES['attach']
            # attach = request.FILES.getlist('attach')
            domain = get_current_site(request).domain
            mail_subject = 'Bug/Feedback - ' + subject

            email_body = details+"\n\nReported By - "+name+"\nEmail - "+email

            to_email = 'proofchecker.pwreset@gmail.com'
            email = EmailMessage(
                mail_subject, email_body, to=[to_email])
            email.attach(attach.name, attach.read(), attach.content_type)
            email.send()
            messages.success(
                request, f'Your Feedback/Bug has been recorded. Thank you')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'proofchecker/feedback_form.html', {'form': form})
@instructor_required
def student_proofs_view(request, pk=None):
    courses = Course.objects.filter(instructor__user=request.user)

    students = []
    for course in courses:
        for student in course.students.all():
            students.append(student)

    students = list(set(students))

    student = None
    proofs = None

    if pk is not None:
        student = Student.objects.get(user__pk=pk)
        proofs = Proof.objects.filter(created_by=pk)

    context = {
        "students": students,
        "student": student,
        "proofs": proofs
    }
    return render(request, 'proofchecker/student_proofs.html', context)



@instructor_required
def course_student_proofs_view(request, course_id=None, student_id=None):

    students = []
    students.append(Course.objects.get(id=course_id).students.all())

    student = None
    proofs = None

    if student_id is not None:
        student = Student.objects.get(user__pk=student_id)
        proofs = Proof.objects.filter(created_by=student_id)

    context = {
        "students": students,
        "student": student,
        "proofs": proofs
    }
    return render(request, 'proofchecker/course_student_proofs.html', context)

