from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddForm
from .models import Contact

def show(request):
    """ 
    This function gets all the members in your Database through your Model
    Any further usage please refer to: https://docs.djangoproject.com/el/1.10/ref/models/querysets/
    """
    contact_list = Contact.objects.all()
    return render(request, 'mycontacts/show.html',{'contacts': contact_list})

def editar(request, id):
    if request.method == 'POST':
        contact_list = get_object_or_404(Contact, id = id)
        django_form = AddForm(request.POST, instance = contact_list)

        if django_form.is_valid():
            django_form.save()
            contact_list.save()
            return redirect(show)
    
    else:
        contact_list = Contact.objects.get(id = id)
        return render(request, 'mycontacts/editar.html', {'contact': contact_list})

def delete(request, id):
    contact_list = get_object_or_404(Contact, id = id)

    if request.method == 'POST':
        contact_list.delete()
        return redirect(show)
    
    else:
        return render(request, 'mycontacts/delete.html', {'contact': contact_list})
    
def add(request):
    """ This function is called to add one contact member to your contact list in your Database """
    if request.method == 'POST':
        
        django_form = AddForm(request.POST)
        if django_form.is_valid():
           
            """ Assign data in Django Form to local variables """
            new_member_name = django_form.data.get("name")
            new_member_relation = django_form.data.get("relation")
            new_member_phone = django_form.data.get('phone')
            new_member_email = django_form.data.get('email')
            
            """ This is how your model connects to database and create a new member """
            Contact.objects.create(
                name =  new_member_name, 
                relation = new_member_relation,
                phone = new_member_phone,
                email = new_member_email, 
                )
                 
            contact_list = Contact.objects.all()
            return redirect(show)
        
        else:
            """ redirect to the same page if django_form goes wrong """
            return render(request, 'mycontacts/add.html')
    else:
        return render(request, 'mycontacts/add.html')

    