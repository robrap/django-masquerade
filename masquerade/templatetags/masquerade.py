from django import template
from django.core.urlresolvers import reverse

from ..views import mask, unmask

register = template.Library()

@register.tag
def masquerade_link(parser, token):
    return MasqueradeLinkNode()

class MasqueradeLinkNode(template.Node):
    def __init__(self):
        self.request = template.Variable('request')
    
    def render(self, context):
        request = self.request.resolve(context)

        link = '<a href="%s">%s</a>'

        try:
            if request.user.is_masked:
                link = link % (reverse(unmask),
                  'Be yourself!')
            else:
                link = link % (reverse(mask),
                  'Impersonate a user.')

        except AttributeError:
            return ''

        return link
        
@register.tag
def masquerade_status(parser, token):
    return MasqueradeStatusNode()

class MasqueradeStatusNode(template.Node):
    def __init__(self):
        self.request = template.Variable('request')
    
    def render(self, context):
        request = self.request.resolve(context)

        status = "You are not currently impersonating anyone."

        try:
            if request.user.is_masked:
                status = "You are impersonating the user <b>%s</b>." % (
                  request.user.username,
#                  request.user.first_name,
#                  request.user.last_name,
                )

        except AttributeError:
            pass

        return status

