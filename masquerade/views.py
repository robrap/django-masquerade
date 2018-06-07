from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from masquerade.forms import MaskForm
from django.contrib.auth.models import User
from masquerade.signals import start_masquerading, stop_masquerading

START_MASQUERADE_REDIRECT_VIEW = getattr(settings, 'START_MASQUERADE_REDIRECT_VIEW', None)
STOP_MASQUERADE_REDIRECT_VIEW = getattr(settings, 'STOP_MASQUERADE_REDIRECT_VIEW', None)

MASQUERADE_REQUIRE_SUPERUSER = getattr(settings,
  'MASQUERADE_REQUIRE_SUPERUSER', False)

def get_start_redirect_url():
    if START_MASQUERADE_REDIRECT_VIEW:
        return reverse(START_MASQUERADE_REDIRECT_VIEW)
    else: return '/'

def get_stop_redirect_url():
    if STOP_MASQUERADE_REDIRECT_VIEW:
        return reverse(STOP_MASQUERADE_REDIRECT_VIEW)
    else: return '/'

def mask(request, template_name='masquerade/mask_form.html'):
    if not request.user.is_masked and not request.user.is_staff:
        return HttpResponseForbidden()
    elif not request.user.is_superuser and MASQUERADE_REQUIRE_SUPERUSER:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MaskForm(request.POST)
        if form.is_valid():
            # turn on masquerading
            request.session['mask_user'] = form.cleaned_data['mask_user']
            start_masquerading.send(sender='Masquerade', request=request)
            return HttpResponseRedirect(get_start_redirect_url())
    else:
        form = MaskForm()

    #return render_to_response(template_name, {'form': form},
    #   context_instance=RequestContext(request))
    return render_to_response(template_name, {'form': form, 'csrf_token': csrf(request)["csrf_token"]})

def unmask(request):
    # Turn off masquerading. Don't bother checking permissions.
    try:
        stop_masquerading.send(sender='Masquerade', request=request)
        del(request.session['mask_user']) 
    except KeyError:
        pass

    return HttpResponseRedirect(get_stop_redirect_url())
