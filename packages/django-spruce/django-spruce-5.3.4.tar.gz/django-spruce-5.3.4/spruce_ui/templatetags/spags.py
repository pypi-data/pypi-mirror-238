import datetime
import os
import types
from django.conf import settings
from django import template
from django.contrib.admin.templatetags.admin_list import _coerce_field_name
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import label_for_field, display_for_field, lookup_field, display_for_value
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.db import models
from django.urls import NoReverseMatch
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import mark_safe
from pathlib import Path

# 获取当前文件所在的绝对路径
current_file = Path(__file__).resolve()

# 获取当前文件所在目录的父目录的父目录，即项目的根目录
BASE_DIR = current_file.parent.parent

# 指定应用程序 "myapp" 的路径
APP_DIR = BASE_DIR

register = template.Library()


@register.simple_tag()
def website_config():
    data = {
        'title': 'DjangoSpruceUi',
        'logo': '/static/assets/images/logo.png',
        'loginImage': '/static/assets/images/account-logo.png',
        'loginDesc': 'Spruce Ui 中后台前端/设计解决方案',
    }
    name = 'WEBSITE_CONFIG'
    return os.environ.get(name, getattr(settings, name, None)) if os.environ.get(name, getattr(settings, name,
                                                                                               None)) is not None else data


@register.simple_tag()
def menus():
    name = 'SPRUCE_MENU'
    if os.environ.get(name, getattr(settings, name, None)):
        return os.environ.get(name, getattr(settings, name, None))
    else:
        return 'false'


@register.simple_tag()
def first():
    name = 'SPRUCE_MENU_FIRST'
    if os.environ.get(name, getattr(settings, name, None)):
        return 'true'
    else:
        return 'false'


@register.simple_tag()
def menus_icon():
    name = 'SPRUCE_MENU_ICON'
    if os.environ.get(name, getattr(settings, name, None)) is True:
        return 'true'
    return 'false'


@register.filter(is_safe=True)
def filter_app_list(value):
    if getattr(settings, 'SPRUCE_SYS', True) is False:
        return 'false'

    def mk(i):
        if i.get('name'):
            i['label'] = i['name']
        i['path'] = i['app_url'] if i.get('app_url') else (i['admin_url'] if i.get('admin_url') else '')
        if i.get('app_label'):
            i['name'] = i['app_label']
        elif i.get('object_name'):
            i['name'] = i['object_name']
        if i.get('models'):
            i['children'] = list(map(mk, i['models']))
            del i['models']
        if i.get('model'):
            del i['model']
        if i.get('models'):
            del i['models']

        def convert_true_to_string(i):
            for key, value in i.items():
                if isinstance(value, dict):
                    # 如果值是字典，则递归处理子字典
                    convert_true_to_string(value)
                elif value is True:
                    # 如果值是True，将其转换为字符串
                    i[key] = 'true'
                elif value is False:
                    i[key] = 'false'
                elif value is None:
                    i[key] = ''

        convert_true_to_string(i)
        return i

    value = list(map(mk, value))
    return value


def items_for_result(cl, result, form):
    """
    Generate the actual list of data.
    """

    def link_in_col(is_first, field_name, cl):
        if cl.list_display_links is None:
            return False
        if is_first and not cl.list_display_links:
            return True
        return field_name in cl.list_display_links

    first = True
    pk = cl.lookup_opts.pk.attname

    for field_index, field_name in enumerate(cl.list_display):
        empty_value_display = cl.model_admin.get_empty_value_display()
        row_classes = ["field-%s" % _coerce_field_name(field_name, field_index)]
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(
                attr, "empty_value_display", empty_value_display
            )
            if f is None or f.auto_created:
                if field_name == "action_checkbox":
                    row_classes = ["action-checkbox"]
                boolean = getattr(attr, "boolean", False)
                result_repr = display_for_value(value, empty_value_display, boolean)
                if isinstance(value, (datetime.date, datetime.time)):
                    row_classes.append("nowrap")
            else:
                if isinstance(f.remote_field, models.ManyToOneRel):
                    field_val = getattr(result, f.name)
                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        result_repr = field_val
                else:
                    result_repr = display_for_field(value, f, empty_value_display)
                if isinstance(
                        f, (models.DateField, models.TimeField, models.ForeignKey)
                ):
                    row_classes.append("nowrap")
        row_class = mark_safe(' class="%s"' % " ".join(row_classes))
        # If list_display_links not defined, add the link tag to the first field
        if link_in_col(first, field_name, cl):
            table_tag = "th" if first else "td"
            first = False

            # Display link to the result's change_view if the url exists, else
            # display just the result's representation.
            try:
                url = cl.url_for_result(result)
            except NoReverseMatch:
                link_or_text = result_repr
            else:
                url = add_preserved_filters(
                    {"preserved_filters": cl.preserved_filters, "opts": cl.opts}, url
                )
                # Convert the pk to something that can be used in JavaScript.
                # Problem cases are non-ASCII strings.
                if cl.to_field:
                    attr = str(cl.to_field)
                else:
                    attr = pk
                value = result.serializable_value(attr)
                link_or_text = format_html(
                    '<a style="color: #2d8cf0;" href="{}">{}</a>',
                    url,
                    result_repr,
                )
            spruce_ui = result_repr if result_repr is not None else ''
            yield {field_name: format_html(
                "{}", link_or_text
            ), 'spruce_ui': spruce_ui}
        else:
            # By default the fields come from ModelAdmin.list_editable, but if we pull
            # the fields out of the form instead of list_editable custom admins
            # can provide fields on a per request basis
            if (
                    form
                    and field_name in form.fields
                    and not (
                    field_name == cl.model._meta.pk.name
                    and form[cl.model._meta.pk.name].is_hidden
            )
            ):
                bf = form[field_name]
                result_repr = mark_safe(str(bf.errors) + str(bf))
            yield {field_name: mark_safe(result_repr)}
    if form and not form[cl.model._meta.pk.name].is_hidden:
        yield format_html("{}", form[cl.model._meta.pk.name])


@register.filter(is_safe=False)
def filter_results(cl):
    data = {}
    columns = []
    for i, field_name in enumerate(cl.list_display):
        text, attr = label_for_field(
            field_name, cl.model, model_admin=cl.model_admin, return_attr=True
        )
        if attr:
            field_name = _coerce_field_name(field_name, i)
            # Potentially not sortable

            # if the field is the action checkbox: no sorting and special class
            if field_name == "action_checkbox":
                columns.append({'type': "selection", "width": 'auto', })
                continue
        columns.append({'title': text, 'key': field_name, "width": 'auto', })
    data['columns'] = columns
    result = []
    for res in cl.result_list:
        packed_dict = {}
        for item in items_for_result(cl, res, None):
            packed_dict.update(item)
        result.append(packed_dict)
    data['data'] = result
    return data


@register.simple_tag()
def random_color():
    import random
    my_list = ["default", "success", "info", "warning", "error"]
    random_string = random.choice(my_list)
    return random_string


@register.filter(is_safe=True, needs_autoescape=True)
def spruce_ui_unordered_list(value, autoescape=True):
    """
    Recursively take a self-nested list and return an HTML unordered list --
    WITHOUT opening and closing <ul> tags.

    Assume the list is in the proper format. For example, if ``var`` contains:
    ``['States', ['Kansas', ['Lawrence', 'Topeka'], 'Illinois']]``, then
    ``{{ var|unordered_list }}`` returns::

        <li>States
        <ul>
                <li>Kansas
                <ul>
                        <li>Lawrence</li>
                        <li>Topeka</li>
                </ul>
                </li>
                <li>Illinois</li>
        </ul>
        </li>
    """
    if autoescape:
        escaper = conditional_escape
    else:

        def escaper(x):
            return x

    def walk_items(item_list):
        item_iterator = iter(item_list)
        try:
            item = next(item_iterator)
            while True:
                try:
                    next_item = next(item_iterator)
                except StopIteration:
                    yield item, None
                    break
                if isinstance(next_item, (list, tuple, types.GeneratorType)):
                    try:
                        iter(next_item)
                    except TypeError:
                        pass
                    else:
                        yield item, next_item
                        item = next(item_iterator)
                        continue
                yield item, None
                item = next_item
        except StopIteration:
            pass

    def list_formatter(item_list, tabs=1):
        indent = "\t" * tabs
        output = []
        for item, children in walk_items(item_list):
            sublist = ""
            if children:
                sublist = "\n%s<n-list>\n%s\n%s</n-list>\n%s" % (
                    indent,
                    list_formatter(children, tabs + 1),
                    indent,
                    indent,
                )
            output.append("%s <n-list-item> %s%s </n-list-item>" % (indent, escaper(item), sublist))
        return "\n".join(output)

    return mark_safe(list_formatter(value))


@register.filter(is_safe=True)
def spruce_ui_list_filter(cl):
    data = []
    for i in cl.filter_specs:
        title = i.title
        options = []
        value = False
        field_generic = False
        if i.__dict__.get('lookup_val') is not None:
            value = i.__dict__['lookup_val']
        # 列表选择
        if i.__dict__.get('lookup_kwarg'):
            if i.__dict__.get('lookup_choices'):
                options.append({'value': '?', 'label': '全部'})
                for lookup_choice in i.__dict__['lookup_choices']:
                    options.append({'value': lookup_choice, 'label': lookup_choice})
            if not i.__dict__.get('lookup_choices'):
                options.append({'value': '?', 'label': '全部'})
                options.append({'value': '1', 'label': '是'})
                options.append({'value': '0', 'label': '否'})
            key = i.__dict__['lookup_kwarg']
        # 时间选择
        else:
            key = i.__dict__['field_generic']
            if len(i.__dict__['date_params']) > 0:
                datetime_object1 = datetime.datetime.strptime(
                    i.__dict__['used_parameters'][f'{i.__dict__["field_path"]}' + '__gte'], "%Y-%m-%d %H:%M:%S")
                datetime_object2 = datetime.datetime.strptime(
                    i.__dict__['used_parameters'][f'{i.__dict__["field_path"]}' + '__lt'], "%Y-%m-%d %H:%M:%S")
                value = [datetime_object1.timestamp() * 1000, datetime_object2.timestamp() * 1000]
            else:
                value = []
            field_generic = i.__dict__['field_generic']

        if value:
            data.append(
                {'title': title, 'options': options, 'key': key, 'value': value,
                 'field_generic': field_generic if field_generic else '',
                 'placeholder': '请选择要搜索的%s' % title})
        else:
            data.append(
                {'title': title, 'options': options, 'key': key, 'placeholder': '请选择要搜索的%s' % title,
                 'field_generic': field_generic if field_generic else '', })
    return data


@register.filter(is_safe=True)
def spruce_ui_field_name(cl):
    texts = ''
    for i in cl.search_fields:
        text, attr = label_for_field(
            i, cl.model, model_admin=cl.model_admin, return_attr=True
        )
        if text == 'Pk':
            texts += 'ID' + ' '
            continue
        texts += text + ' '
    return texts


@register.filter(is_safe=True)
def spruce_ui_file_format(file_format):
    return [{'label': value, 'value': key} for key, value in file_format]


@register.simple_tag()
def icon_list():
    name = 'SPRUCE_ICON'
    data = os.environ.get(name, getattr(settings, name, None))
    return data


@register.filter(is_safe=True)
def filter_icon(icon, request):
    try:
        return getattr(request.resolver_match.func.model_admin, icon).icon
    except:
        return ''


@register.filter(is_safe=True)
def filter_type(icon, request):
    try:
        return getattr(request.resolver_match.func.model_admin, icon).type
    except:
        return ''
