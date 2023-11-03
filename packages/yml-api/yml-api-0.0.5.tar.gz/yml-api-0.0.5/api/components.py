from django.template.loader import render_to_string


class Link(dict):
    def __init__(self, url, target='_blank', icon=None):
        self['type'] = 'link'
        self['url'] = url
        self['target'] = target
        self['icon'] = icon


class QrCode(dict):
    def __init__(self, text):
        self['type'] = 'qrcode'
        self['text'] = text


class Progress(dict):
    def __init__(self, value):
        self['type'] = 'progress'
        self['value'] = int(value or 0)


class Status(dict):
    def __init__(self, style, label):
        self['type'] = 'status'
        self['style'] = style
        self['label'] = label


class Indicators(dict):
    def __init__(self, title):
        self['type'] = 'indicators'
        self['title'] = title
        self['items'] = []
        self['actions'] = []

    def append(self, name, value):
        self['items'].append(dict(name=str(name), value=value))

    def action(self, label, url, modal=False):
        self['actions'].append(dict(label=str(label), url=url, modal=modal))


class Boxes(dict):
    def __init__(self, title):
        self['type'] = 'boxes'
        self['title'] = str(title)
        self['items'] = []

    def append(self, icon, label, url):
        self['items'].append(dict(icon=icon, label=label, url=url))

class Info(dict):
    def __init__(self, title, message):
        self['type'] = 'info'
        self['title'] = title
        self['message'] = message
        self['actions'] = []

    def action(self, label, url, modal=False, icon=None):
        self['actions'].append(dict(label=label, url=url, modal=modal, icon=icon))


class Warning(dict):
    def __init__(self, title, message):
        self['type'] = 'warning'
        self['title'] = title
        self['message'] = message
        self['actions'] = []

    def action(self, label, url, modal=False):
        self['actions'].append(dict(label=label, url=url, modal=modal))


class Table(dict):
    def __init__(self, actions=(), subsets=(), subset=None, filters=(), flags=(), rows=(), pagination=None):
        self['type'] = 'table'
        self['actions'] = actions
        self['subsets'] = subsets
        self['subset'] = subset
        self['filters'] = filters
        self['flags'] = flags
        self['rows'] = rows
        self['pagination'] = pagination


class TemplateContent(dict):
    def __init__(self, name, context):
        self['type'] = 'html'
        self['content'] = render_to_string(name, context)


