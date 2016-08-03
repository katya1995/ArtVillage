from models import Art, Agent, UserProfile, Artist, Image, Orders
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

from django.db import transaction
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
    AdminPasswordChangeForm)
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.pdfgen import canvas
from django.http import HttpResponse


csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

#Delete when deployed
#admin.site.unregister(Group)

"""
Adds action to User table where super users can make certain users volunteers and members of staff
"""
def make_volunteer(modeladmin, request, queryset):
    g = Group.objects.get(name='Volunteers')
    for qs in queryset:
        try:
            g.user_set.add(qs)
        except:
            pass

    queryset.update(is_staff = "True")

"""
Action to create labels for up to 5 pieces of art at a time (all of which should be by the same artist) and returns a pdf
"""
def make_labels(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="labels.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    y = 700
    count = 0

    #Original way of creating labels, kept in case these turn out to be more suitable.
    '''
    for qs in queryset:

        name = str(qs.name)
        by = "By: " + str(qs.artist)
        s =  u"\xA3" + str(qs.price)

        p.setFont("Helvetica",16,leading=None)
        p.drawCentredString(290,y,name)
        y = y - 20
        p.drawCentredString(290,y,by)
        y = y - 20
        p.drawCentredString(290,y,s)
        y = y - 20
        p.drawCentredString(290,y,str(qs.identification))
        p.drawImage('static/images/logo.jpg', 75, y, width=120, height=80)
        y = y - 15
        p.roundRect(50,y,width=500,height=105,radius=4)


        count += 1

        # Close the PDF object cleanly, and we're done.
        if count % 3 == 0:
            p.showPage()
            y = 700

        else:
            y = y - 200
    p.save()
    '''

    if len(queryset) > 5:
        p.drawCentredString(290,y,'Please select 5 or less pieces of art')
        p.showPage()

    else:
        name = queryset[0].artist

        p.rect(290-(283.442/2),y-425.163,283.442,425.163)
        p.rect(290-(283.442/2)+5,y-425.163+5,283.442-10,425.163-10)

        p.setFont("Times-Bold",24,leading=None)
        y = y - 30
        p.drawCentredString(290, y, name)
        y = y - 35
        for qs in queryset:
            p.setFont("Times-Roman",14,leading=None)
            p.drawCentredString(290,y,qs.name)
            y = y -15
            p.setFont("Times-Italic",14,leading=None)
            p.drawCentredString(290,y,qs.sub_category)
            y = y - 15
            p.setFont("Times-Bold",14,leading=None)
            s =  u"\xA3" + str(qs.price)
            p.drawCentredString(290,y,s)
            y = y - 30

        p.drawImage('static/images/logo.jpg',290-(283.442/2)+15 , 700-425.163+15, width=50, height=40)
        p.drawImage('static/images/UnLtd.png',290-(283.442/2)+75 , 700-425.163+25, width=80, height=20)
        p.drawImage('static/images/shawlands.jpg',290-(283.442/2)+160 , 700-425.163+20, width=50, height=30)
        p.drawImage('static/images/glasgow.png',290-(283.442/2)+220 , 700-425.163+20, width=50, height=30)

        p.showPage()

    p.save()
    return response

"""
Action to change art status to approved, approved pieces will be displayed to users
"""
def approve_art(modeladmin, request, queryset):
    queryset.update(authenticate = "approved")

"""
Action to reject pieces of art. Used if information is wrong or if it should be hidden from the main page
"""
def reject_art(modeladmin, request, queryset):
    queryset.update(authenticate = "rejected")

class AgentResource(resources.ModelResource):

    class Meta:
        model = Agent
        fields = ( 'id', 'surname', 'firstname', 'phone', 'postcode', )
        exclude = ('fullname', )

class ArtResource(resources.ModelResource):

    class Meta:
        model = Art
        import_id_fields = ('identification',)
        fields = ( 'identification', 'name', 'price', 'artist_id', 'artist', 'category', \
                   'sub_category', 'quantity', 'weight', 'size', 'agent_id', 'agent',)
        export_order = ( 'identification', 'name', 'price', 'artist_id', 'artist', 'category', 'sub_category', \
                         'quantity', 'weight', 'size', 'agent_id', 'agent', )
        exclude = ('id', 'authenticate', 'description', )

class PictureAdmin(admin.ModelAdmin):
    list_display = ['id','art']
    search_fields = ('art', )
    raw_id_fields = ("art",)


# Add in this class to customized the Admin Interface
class ArtAdmin(ImportExportModelAdmin):
    raw_id_fields = ("agent_id","artist_id",)
    resource_class = ArtResource
    list_display = ['id', 'identification', 'name', 'artist', 'category', 'sub_category', 'agent', 'authenticate', ]
    list_display_links = ('id', 'identification', 'name', 'artist', 'category', 'sub_category', 'agent', 'authenticate')
    search_fields = ('name', 'category', 'artist', 'identification', 'authenticate', )
    list_filter = ["authenticate","category"]
    actions = [approve_art, reject_art, make_labels]


    def get_actions(self, request):
        actions = super(ArtAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
        else:
            for a in actions:
                if a != 'make_labels':
                    del actions[a]
        return actions

class ArtistResource(resources.ModelResource):
    class Meta:
        model = Artist
        fields = ( 'id', 'surname', 'firstname')
        exclude = ('description', 'fullname', )


class AgentAdmin(ImportExportModelAdmin):
    resource_class = AgentResource
    list_display = ['id', 'surname', 'firstname', 'phone', 'postcode', ]
    list_display_links = ('id', 'surname', 'firstname', 'phone', 'postcode')
    search_fields = ['surname', 'firstname', 'fullname', 'id', 'phone', 'postcode', 'fullname',]

    def get_actions(self, request):
        actions = super(AgentAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
        else:
            actions = []
        return actions

class ArtistAdmin(ImportExportModelAdmin):
    resource_class = ArtistResource
    list_display = ['surname','firstname',]
    search_fields = ['surname','firstname','id', 'fullname',]
    list_display_links = ('surname', 'firstname')

    def get_actions(self, request):
        actions = super(ArtistAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
        else:
            actions = []
        return actions

class OrderAdmin(ImportExportModelAdmin):
    list_display = ['payer_email','payment_date','buyer','payment_gross','payment_status']
    search_fields = ['payer_email','buyer','id']
    list_display_links = ('payer_email','payment_date','buyer','payment_gross','payment_status', )
    list_filter = ["payment_status"]

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
        else:
            actions = []
        return actions

class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    actions = [make_volunteer]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls import patterns
        return patterns('',
            (r'^(\d+)/password/$',
             self.admin_site.admin_view(self.user_change_password))
        ) + super(UserAdmin, self).get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url,
                                               extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.get_queryset(request), pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(admin.site.each_context())
        return TemplateResponse(request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context, current_app=self.admin_site.name)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST['_continue'] = 1
        return super(UserAdmin, self).response_add(request, obj,
                                                   post_url_continue)



# Update the registeration to include this customised interface
admin.site.unregister(User)
admin.site.register(Art, ArtAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Image, PictureAdmin)
admin.site.register(Orders,OrderAdmin)
