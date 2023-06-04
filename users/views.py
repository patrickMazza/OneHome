
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .form import *
from .models import ClientProfile, Profile
from django.urls import reverse
from django.template.defaultfilters import slugify
from secrets import token_urlsafe
from django.core.files.storage import FileSystemStorage


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save user to Database
            # Show sucess message when account is created
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')  # Redirect user to Login page
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def user_home(request):
    cur_user_id = request.user.id
    client_entries = ClientProfile.objects.filter(
        caseworker=cur_user_id).order_by('-created_at')
    if request.method == 'GET':
        form = Sort(request.GET)
        if form.is_valid():
            selection = form['field'].value()
            if selection == "Highest Priority":
                client_entries = ClientProfile.objects.filter(
                    caseworker=cur_user_id).orderby('client_Intake_Date')
            elif selection == "Most Progress":
                client_entries = ClientProfile.objects.filter(
                    caseworker=cur_user_id).orderby('-progress')
            elif selection == "Oldest to Newest":
                client_entries = ClientProfile.objects.filter(
                    caseworker=cur_user_id).order_by('created_at')

    else:
        form = Sort()
        client_entries = ClientProfile.objects.filter(
            caseworker=cur_user_id).order_by('-created_at')

    context = {
        'form': form,
        'client_entries':  client_entries,
    }
    return render(request, "users/user_home.html", context)


@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientRegisterForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            request_image = request.FILES.get('image', 'default.jpg')
            obj = ClientProfile.objects.create(first_Name=form['first_Name'].value(), last_Name=form['last_Name'].value(), birthdate=form['birthdate'].value(),
                                               client_Intake_Date=form['client_Intake_Date'].value(), image=request_image,
                                               slug=slugify(form['first_Name'].value(
                                               ) + form['last_Name'].value() + token_urlsafe(16)),
                                               caseworker=request.user)
            obj.save()
            messages.success(
                request, f'Client has been added to your homepage.')

            return redirect('user_home')

    else:
        cur_user = request.user
        # if we have a user that has already selected info, it will pass in this info
        form = ClientRegisterForm(instance=cur_user)

    args = {}
    args['form'] = form

    return render(request, 'users/add_client.html', args)


def addform(request, slug):
    cur_user_id = request.user
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            if form['application_type'].value() == "2010e Supportive Housing Application":
                part1 = Application2010e_part1.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="Application Summary", progress=0, updated_at=datetime.now(), done=False, consent=False)
                part2 = Application2010e_part2.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="Assessment Survey", progress=0, updated_at=datetime.now(), done=False)
                part3 = Application2010e_part3.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="PsychoSocial Evaluation", progress=0, updated_at=datetime.now(), done=False)
                part4 = Application2010e_part4.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC Housing and Homeless History Report", progress=0, updated_at=datetime.now(), done=False)
                part5 = Application2010e_part5.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC Standardized Vulnerability Assessment", progress=0, updated_at=datetime.now(), done=False)
                part6 = Application2010e_part6.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC HRA Consent Form", progress=0, updated_at=datetime.now(), done=False)
                part7 = Application2010e_part7.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC Supportive Housing Determination Letter", progress=0, updated_at=datetime.now(), done=False)
                part1.save()
                part2.save()
                part3.save()
                part4.save()
                part5.save()
                part6.save()
                part7.save()
                obj = ClientApplication.objects.create(caseworker=cur_user_id, client=cur_client, part1_id=part1, part2_id=part2, part3_id=part3, part4_id=part4, part5_id=part5, part6_id=part6, part7_id=part7,
                                                       application_Name=form['application_type'].value(), progress=0, slug=slugify(form['application_type'].value() + token_urlsafe(16)), created_at=datetime.now(), updated_at=datetime.now())
                obj.save()
    else:
        form = AddForm()
    client_entry = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug).values()
    formlist = ClientApplication.objects.filter(
        caseworker=cur_user_id, client=cur_client).values()

    context = {
        'form': form,
        'formlist': formlist,
        'client_entry':  client_entry,
    }
    return render(request, 'users/client_page.html', context)


def deleteform(request, slug):
    cur_user_id = request.user
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            if form['application_type'].value() == "2010e Supportive Housing Application":
                part1 = Application2010e_part1.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="Application Summary", progress=0, updated_at=datetime.now(), done=False, consent=False)
                part2 = Application2010e_part2.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="Assessment Survey", progress=0, updated_at=datetime.now(), done=False)
                part3 = Application2010e_part3.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="PsychoSocial Evaluation", progress=0, updated_at=datetime.now(), done=False)
                part4 = Application2010e_part4.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC Housing and Homeless History Report", progress=0, updated_at=datetime.now(), done=False)
                part5 = Application2010e_part5.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC Standardized Vulnerability Assessment", progress=0, updated_at=datetime.now(), done=False)
                part6 = Application2010e_part6.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC HRA Consent Form", progress=0, updated_at=datetime.now(), done=False)
                part7 = Application2010e_part7.objects.create(
                    caseworker=cur_user_id, client=cur_client, application_Name="NYC Supportive Housing Determination Letter", progress=0, updated_at=datetime.now(), done=False)
                part1.save()
                part2.save()
                part3.save()
                part4.save()
                part5.save()
                part6.save()
                part7.save()
                obj = ClientApplication.objects.create(caseworker=cur_user_id, client=cur_client, part1_id=part1, part2_id=part2, part3_id=part3, part4_id=part4, part5_id=part5, part6_id=part6, part7_id=part7,
                                                       application_Name=form['application_type'].value(), progress=0, slug=slugify(form['application_type'].value() + token_urlsafe(16)), created_at=datetime.now(), updated_at=datetime.now())
                obj.save()
    else:
        form = AddForm()
    client_entry = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug).values()
    formlist = ClientApplication.objects.filter(
        caseworker=cur_user_id, client=cur_client).values()

    context = {
        'form': form,
        'formlist': formlist,
        'client_entry':  client_entry,
    }
    return render(request, 'users/client_page.html', context)


def deleteform(request, slug):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]

    client_entry = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug).values()
    formlist = ClientApplication.objects.filter(
        caseworker=cur_user_id, client=cur_client).values()

    context = {
        'form': "",
        'formlist': formlist,
        'client_entry':  client_entry,
    }
    return render(request, 'users/deleteform.html', context)


def deleteformdone(request, slug1, slug2):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug1)[0]

    client_entry = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug1).values()

    ClientApplication.objects.filter(slug=slug2).delete()

    formlist = ClientApplication.objects.filter(
        caseworker=cur_user_id, client=cur_client).values()

    context = {
        'form': "",
        'formlist': formlist,
        'client_entry':  client_entry,
    }
    return render(request, 'users/client_page.html', context)


@ login_required
def client_page(request, slug):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]

    client_entry = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug).values()
    formlist = ClientApplication.objects.filter(
        caseworker=cur_user_id, client=cur_client).values()

    context = {
        'form': "",
        'formlist': formlist,
        'client_entry':  client_entry,
    }
    return render(request, 'users/client_page.html', context)


@ login_required
def application_home(request, slug1, slug2):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug1)[0]

    client_entry = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug1).values()
    app = ClientApplication.objects.filter(slug=slug2)[0]
    formlist = ClientApplication.objects.filter(
        caseworker=cur_user_id, client=cur_client).values()
    part1 = Application2010e_part1.objects.filter(pk=app.part1_id.id).values()
    part2 = Application2010e_part2.objects.filter(pk=app.part2_id.id).values()
    part3 = Application2010e_part3.objects.filter(pk=app.part3_id.id).values()
    part4 = Application2010e_part4.objects.filter(pk=app.part4_id.id).values()
    part5 = Application2010e_part5.objects.filter(pk=app.part5_id.id).values()
    part6 = Application2010e_part6.objects.filter(pk=app.part6_id.id).values()
    part7 = Application2010e_part7.objects.filter(pk=app.part7_id.id).values()

    context = {
        'app': app,
        'slug1':  slug1,
        'slug2':  slug2,
        'part1': part1,
        'part2': part2,
        'part3': part3,
        'part4': part4,
        'part5': part5,
        'part6': part6,
        'part7': part7,
        'client_entry':  client_entry,
        'formlist': formlist
    }
    return render(request, 'users/application_home.html', context)


@ login_required
def app_part(request, slug1, slug2, app_name, id):

    app = Application2010e_part1.objects.get(pk=id)
    if request.method == 'POST':
        form = Application2010e_P1(request.POST, instance=app)
        if form.is_valid():
            form.save()
            redirect('application_home', slug1, slug2)
    else:
        form = Application2010e_P1(instance=app)

    context = {
        'slug1':  slug1,
        'slug2': slug2,
        'form': form,
        'app': app
    }
    return render(request, 'users/app_part.html', context)


@ login_required
def upload_document(request, slug):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]
    if request.method == 'POST':
        form = DocsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  # saving model instance
            messages.success(
                request, f'Documents Uploaded')
            myfile = request.FILES['file_field']
            fs = FileSystemStorage(
                location='media/client_docs/', base_url='media/client_docs/')
            filename = fs.save(myfile.name, myfile)
            file_url = fs.url(filename)
            doc_obj = Docs.objects.create(document_Name=form['document_Name'].value(
            ), client=cur_client, application=form['application_type'].value(), file_field=file_url)
            doc_obj.save()
    else:
        form = DocsForm()

    all_docs = Docs.objects.filter(client=cur_client).values()

    context = {
        'documents': all_docs,
        'slug':  slug,
        'form': form
    }
    return render(request, 'users/upload_document.html', context)


def allDocs(request, slug):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]
    docs = Docs.objects.filter(client=cur_client).values()
    if request.method == 'POST':
        doc_id = request.POST['selected_doc']
        return delete_document_done(request, slug, doc_id)
    context = {
        'documents': docs,
        'slug':  slug,
    }
    return render(request, 'users/delete_document.html', context)


def delete_document_done(request, slug, doc_id):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]
    Docs.objects.filter(pk=doc_id).delete()
    messages.success(
        request, f'Document Deleted')
    docs = Docs.objects.filter(client=cur_client).values()
    context = {
        'documents': docs,
        'slug':  slug,

    }
    return render(request, 'users/delete_document_done.html', context)


def getChecks(request, slug):
    cur_user_id = request.user.id
    cur_client = ClientProfile.objects.filter(
        caseworker=cur_user_id, slug=slug)[0]
    docs = Docs.objects.filter(client=cur_client).values()
    if request.method == 'POST':
        doc_id = request.POST['selected_doc']
        return delete_document_done(request, slug, doc_id)
    context = {
        'documents': docs,
        'slug':  slug,
    }
    return render(request, 'users/delete_document.html', context)
