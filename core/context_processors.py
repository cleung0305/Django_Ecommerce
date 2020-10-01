from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

def contact_form(request):
    request_context = RequestContext(request)
    if request.method == 'GET':
        contact_form = ContactForm()
        context = {'contact_form': contact_form}
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data['subject']
            from_email = contact_form.cleaned_data['from_email']
            message = contact_form.cleaned_data['message']
        try:
            send_mail(subject, message, from_email, ['loklok12614@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid Header Found.')
        context = {
            'contact_form': contact_form,
            'subject': subject,
            'from_email': from_email,
            'message': message
        }
    return context
