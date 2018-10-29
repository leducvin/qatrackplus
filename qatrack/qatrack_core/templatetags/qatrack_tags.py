import re

from django.core.cache import cache
from django.db.models import ObjectDoesNotExist
from django import template
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext as _

from qatrack.service_log import models as sl_models

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='addplaceholder')
def addplaceholder(field, placeholder=None):
    if placeholder is None:
        if hasattr(field, 'verbose_name'):
            return field.as_widget(attrs={'placeholder': field.verbose_name})
        v_name = field.name.replace('_', ' ').title()
        return field.as_widget(attrs={'placeholder': v_name})
    else:
        return field.as_widget(attrs={'placeholder': placeholder})


@register.filter(name='addcss_addplaceholder')
def addcss_addplaceholder(field, css):
    if hasattr(field, 'verbose_name'):
        return field.as_widget(attrs={'placeholder': field.verbose_name, 'class': css})
    v_name = re.sub(r'\d', '', field.name.replace('_', ' ').title())
    return field.as_widget(attrs={'placeholder': v_name, 'class': css})


@register.filter(name='hideinput')
def hideinput(field):
    return field.as_widget(attrs={'type': 'hidden'})


@register.filter(name='disableinput')
def disableinput(field):
    return field.as_widget(attrs={'disabled': 'disabled'})


@register.filter
def lookup(d, key):
    return d.get(key)


@register.simple_tag(name='render_status_tag')
def render_status_tag(status_name):
    status = sl_models.ServiceEventStatus.objects.get(name=status_name)
    return '<span class="label smooth-border" style="border-color: %s;">%s</span>' % (
        status.colour, status_name
    )


@register.filter(name='get_user_name')
def get_user_name(user):
    if user is not None:
        return user.username if not user.first_name or not user.last_name else user.first_name + ' ' + user.last_name
    else:
        return ''


@register.simple_tag(name='render_log')
def render_log(service_log, user):
    today = timezone.now().date()
    if service_log.datetime.date() == today:
        if timezone.now() - service_log.datetime < timezone.timedelta(hours=1):
            datetime_display = '%s %s' % (int((timezone.now() - service_log.datetime).total_seconds() / 60), _('minutes ago'))
        else:
            datetime_display = timezone.localtime(service_log.datetime).strftime('%I:%M %p')
    elif service_log.datetime.date() == today - timezone.timedelta(days=1):
        datetime_display = '%s %s' % (_('Yesterday'), timezone.localtime(service_log.datetime).strftime('%I:%M %p'))
    else:
        datetime_display = timezone.localtime(service_log.datetime).strftime('%b %d, %I:%M %p')

    context = {
        'instance': service_log,
        'datetime_display': datetime_display,
        'user': get_user_name(service_log.user),
        'can_view': user.has_perm('service_log.view_serviceevent') and service_log.service_event.is_active
    }
    if service_log.log_type == sl_models.NEW_SERVICE_EVENT:

        return get_template('service_log/log_service_event_new.html').render(context)

    elif service_log.log_type == sl_models.MODIFIED_SERVICE_EVENT:

        context['extra_info'] = service_log.extra_info
        return get_template('service_log/log_service_event_modified.html').render(context)

    elif service_log.log_type == sl_models.STATUS_SERVICE_EVENT:

        context['extra_info'] = service_log.extra_info
        status_old_colour = cache.get('service-status-colours').get(service_log.extra_info['status_change']['old'])
        context['old_status_tag'] = '<span class="label smooth-border" style="border-color: %s;">%s</span>' % (
            status_old_colour, service_log.extra_info['status_change']['old']
        ) if status_old_colour is not None else service_log.extra_info['status_change']['old']

        status_new_colour = cache.get('service-status-colours').get(service_log.extra_info['status_change']['new'])
        context['new_status_tag'] = '<span class="label smooth-border" style="border-color: %s;">%s</span>' % (
            status_new_colour, service_log.extra_info['status_change']['new']
        ) if status_new_colour is not None else service_log.extra_info['status_change']['new']
        context['new_status_colour'] = status_new_colour

        return get_template('service_log/log_service_event_status.html').render(context)

    elif service_log.log_type == sl_models.CHANGED_RTSQA:

        context['extra_info'] = service_log.extra_info
        return get_template('service_log/log_rtsqa.html').render(context)

    elif service_log.log_type == sl_models.DELETED_SERVICE_EVENT:

        context['extra_info'] = service_log.extra_info
        return get_template('service_log/log_service_event_deleted.html').render(context)
