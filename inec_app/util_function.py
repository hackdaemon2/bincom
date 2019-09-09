from django.utils import timezone
from django.conf import settings

def extra_context ( context, title ):
    context['current_year'] = timezone.now().year
    context['app_name'] = settings.APP_NAME
    context['support_email'] = settings.SUPPORT_EMAIL
    context['support_phone'] = settings.SUPPORT_PHONE
    context['developer_name'] = settings.DEVELOPER_NAME
    context['twitter'] = settings.TWITTER
    context['linkedin'] = settings.LINKEDIN
    context['github'] = settings.GITHUB
    context['repo'] = settings.REPO
    context['title'] = title
    
    return context