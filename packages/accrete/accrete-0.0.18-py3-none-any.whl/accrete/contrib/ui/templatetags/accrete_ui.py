import logging
from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

_logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(name='combine_templates')
def combine_templates(template_name, request=None):
    html = ''
    for app in settings.INSTALLED_APPS:
        try:
            html += render_to_string(
                f'{app.split(".")[-1]}/{template_name}', request=request
            )
        except template.TemplateDoesNotExist:
            continue
    return mark_safe(html)


@register.filter(name='get_attr')
def get_attr_from_string(param, value):
    try:
        attr = getattr(param, value)
    except AttributeError:
        _logger.exception(f'Object {param} has no attribute {value}')
        return ''
    if callable(attr):
        return attr()
    else:
        return attr


@register.filter(name='render_query_params')
def query_params_to_html(params):
    html = ''
    for param in params:
        html += build(param)
    return mark_safe(html)


def build(param):
    if not param.get('params'):
        return build_param(param)
    else:
        return build_params(param)


def get_value(param):
    if param.get('data_type', '') == 'bool':
        return f'data-value={param["value"]}'
    else:
        return f'data-value=""'


def build_params(param):
    start = f'<div class="query-param" tabindex="-1" data-param="{param["param"]}" ' \
            f'data-param-label="{param["label"]}">' \
            f'<p class="px-1 arrow">{param["label"]}</p>' \
            f'<div class="query-params is-hidden" data-param="{param["param"]}">'
    stop = '</div></div>'
    params = []
    for p in param.get('params'):
        params.append(build(p))
    return f'{start}{"".join(params)}{stop}'


def build_param(param):
    return f'<div class="query-param" tabindex="-1" data-type="{param["data_type"]}" ' \
           f'data-param-invert="{"true" if param.get("invert") else "false"}" ' \
           f'data-param="{param["param"]}" data-param-label="{param["label"]}" ' \
           f'{get_value(param)} data-step="{param.get("step", "1")}">' \
           f'<p class="px-1 arrowless">{param["label"]}</p>' \
           f'<div class="param-options is-hidden">{build_options(param)}</div></div>'


def build_options(param):
    options = ''
    for choice in param.get('choices', []):
        options += f'<option value="{choice[0]}">{choice[1]}</option>'
    return options
