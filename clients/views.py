# -*- coding: utf-8 -*-
from django.utils.encoding import smart_text
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.forms.util import ErrorList
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from forms import ClientFindForm
from models import Client

# Create your views here.
class ClientsView(ListView):
    '''
    view list of clients and take link for download report
    get from GET array string for filter and atributte name for sort
    use form (from forms.py) for find
    '''
    model = Client

    _ORDER_LIST_FIELD = ['name', '-name', 'sername', '-sername', 'birthday', '-birthday']
    @property
    def order_list_field(self):
        return self._ORDER_LIST_FIELD

    def get(self, request, *args, **kwargs):
        self.find_text = self.request.GET.get('find_text', None)
        if self.find_text is not None:
            self.find_text = smart_text(self.find_text)
        self.find_form = ClientFindForm(request.GET)

        self.order_field = None
        if not 'find' in request.GET:
            for field_name in self.order_list_field:
                if field_name in request.GET:
                    self.order_field = field_name
                    break
        return super(ClientsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)
        context['find_form'] = self.find_form if self.find_form is not None else ClientFindForm()
        return context

    def get_queryset(self):
        my_queryset = None
        if self.find_text is None:
            my_queryset = Client.objects.all()
        else:
            keys = filter(lambda x: len(x) > 0, self.find_text.split(' '))
            if keys is None or len(keys) == 0:
                my_queryset = Client.objects.all()
            elif len(keys) == 1:
                my_queryset = Client.objects.filter(Q(name__contains=keys[0]) | Q(sername__contains=keys[0]))
            else:
                my_queryset = Client.objects.filter(Q(name=keys[0]) & Q(sername=keys[1]) | Q(name=keys[1]) & Q(sername=keys[0]))
        if self.order_field is not None:
            my_queryset = my_queryset.order_by(self.order_field)
        return my_queryset

def create_report():
    from tasks import report
    report.delay()

def test_in_image(form):
    '''
    test image size (<10Mb)
    :param form: form
    :return: test ok -> None, test bad -> form with error
    '''
    if 'photo' in form.cleaned_data:
        if form.cleaned_data['photo'].size > 1 * 1024 * 1024:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                _(u'Photo have big size')
            ])
            return form
    return None

class ClientCreate(CreateView):
    '''
    View form for create of new client
    '''
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('clients:view')
    model = Client
    fields = ['name', 'sername', 'birthday', 'photo']

    def form_valid(self, form):
        '''
        bild report (task to celery)
        '''
        result_test_image = test_in_image(form)
        if result_test_image is None:
            create_report()
            return super(ClientCreate, self).form_valid(form)
        return self.form_invalid(result_test_image)

class ClientUpdate(UpdateView):
    '''
    View form for change of client
    '''
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('clients:view')
    model = Client
    fields = ['name', 'sername', 'birthday', 'photo']

    def form_valid(self, form):
        result_test_image = test_in_image(form)
        if result_test_image is None:
            create_report()
            return super(ClientUpdate, self).form_valid(form)
        return self.form_invalid(result_test_image)

class ClientDetail(DetailView):
    '''
    Detail view of client
    '''
    model = Client

class ClientDelete(DeleteView):
    '''
    Remove view of client
    '''
    model = Client
    success_url = reverse_lazy('clients:view')

    def get(self, request, *args, **kwargs):
        from tasks import report
        report.delay()
        return super(ClientDelete, self).get(request, *args, **kwargs)

class ClientLikes(ListView):
    '''
    Form for view photos of clients, and set likes photos
    Set like with help post query
    '''
    model = Client
    template_name = 'clients/client_likes_list.html'

    def post(self, request, *args, **kwargs):
        if "like_id" in request.POST:
            client = Client.objects.get(pk = request.POST['like_id'])
            client.likes += 1
            client.save()
        return super(ClientLikes, self).get(request, *args, **kwargs)