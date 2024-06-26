from functools import reduce
from itertools import chain

import wtforms.fields
from flask import url_for
from markupsafe import escape, Markup as HTMLString
from wtforms.widgets.core import html_params


class WidgetDecorator(object):
    """Decorate widgets."""

    def __init__(self, widget):
        """
        :param widget: Original widget to be decorated.
        """
        if widget is None:
            raise ValueError('Parameter widget may not be None.')
        self.widget = widget


class BootstrapFormControlDecorator(WidgetDecorator):
    """Adds the Bootstrap form-control class to a widget."""

    def __call__(self, field, **kwargs):
        if 'class_' in kwargs:
            kwargs['class_'] = u'form-control ' + kwargs['class_']
        else:
            kwargs['class_'] = u'form-control'

        if field.errors:
            kwargs['class_'] += ' is-invalid'

        return self.widget(field, **kwargs)


class BootstrapStandardDecorator(WidgetDecorator):
    """
    Renders a field in horizontal layout.

    Horizontal layout is a two column layout, where the label is placed in the
    left column and the field is placed right next to it.
    """

    def render_horizontal(self, field, **kwargs):
        error_html = [
            Markup('<div class="invalid-feedback">{0}</div>').format(e)
            for e in field.errors
        ]
        desc_html = []
        if field.description:
            desc_html.append(
                Markup('<div class="col-sm-12"><span class="form-text">{0}</span></div>')
                    .format(field.description)
            )
        label_classes = ['col-form-label']
        if field.errors:
            label_classes.append('text-danger')
        html = [f'<div class="row" id="form-group-{field.name}">',
                '<div class="col-sm-4">',
                field.label(class_=' '.join(label_classes)),
                *desc_html,
                '</div>',
                '<div class="col-sm-4">',
                self.widget(field, **kwargs),
                *error_html,
                '</div>',
                '</div>']
        return HTMLString(u''.join(html))

    def render_inline(self, field, **kwargs):
        return HTMLString(u''.join([
            field.label(class_=u'sr-only'),
            self.widget(field, placeholder=field.label.text, **kwargs),
        ]))

    def render_basic(self, field, **kwargs):
        html = [field.label(),
                '<br/>',
                self.widget(field, **kwargs)]
        help_block = Markup(u'<span class="form-text">{0}</span>')
        if field.description:
            html.append(help_block.format(field.description))
        html.extend(help_block.format(e) for e in field.errors)
        return HTMLString(u''.join(html))

    def __call__(self, field, **kwargs):
        render_mode = kwargs.pop("render_mode", "basic")
        if render_mode == "basic":
            return self.render_basic(field, **kwargs)
        elif render_mode == "horizontal":
            return self.render_horizontal(field, **kwargs)
        elif render_mode == "inline":
            return self.render_inline(field, **kwargs)
        else:
            raise ValueError("Unknown render mode: {0}".format(render_mode))


class BootstrapRadioCheckboxDecorator(WidgetDecorator):
    """
    Renders a field in horizontal layout.

    Horizontal layout is a two column layout, where the label is placed in the
    left column and the field is placed right next to it.
    """
    wrapper_class = None

    def _render(self, field, **kwargs):

        # we need:
        input_classes = kwargs.get('class_', '').split()
        kwargs['class_'] = ' '.join(input_classes + ['form-check-input'])
        return HTMLString(u''.join([
            u'<div class="form-check">',
            self.widget(field, **kwargs),
            field.label(escape(field.label.text), class_='form-check-label'),
            u'</div>',
        ]))

    def render_basic(self, field, **kwargs):
        return self._render(field, **kwargs)

    def render_horizontal(self, field, **kwargs):
        return HTMLString(u''.join([
            f'<div class="row" id="form-group-{field.name}"><div class="offset-sm-4 col-sm-4">',
            self._render(field, **kwargs),
            u'</div></div>',
        ]))

    def render_inline(self, field, **kwargs):
        return field.label(u"{0} {1}".format(
            self.widget(field, **kwargs),
            escape(field.label.text)
        ), class_=self.wrapper_class + "-inline")

    def __call__(self, field, **kwargs):
        render_mode = kwargs.pop("render_mode", "horizontal")
        if render_mode == "basic":
            return self.render_basic(field, **kwargs)
        if render_mode == "horizontal":
            return self.render_horizontal(field, **kwargs)
        if render_mode == "inline":
            return self.render_inline(field, **kwargs)
        raise ValueError(f"Unknown render mode: {render_mode}")


class BootstrapRadioDecorator(BootstrapRadioCheckboxDecorator):
    wrapper_class = u"radio"


class BootstrapCheckboxDecorator(BootstrapRadioCheckboxDecorator):
    wrapper_class = u"checkbox"


class BootstrapFieldListWidget(object):
    def __call__(self, field, **kwargs):
        return HTMLString(u''.join(chain(
            (Markup(u'<p class="form-text">{0}</p>').format(e) for e in field.errors),
            (f(**kwargs) for f in field)
        )))


class BootstrapFormFieldWidget(object):
    def __call__(self, field, **kwargs):
        return HTMLString(u"<div class=\"form-field\">" +
                          u''.join(f(**kwargs) for f in field) +
                          u"</div>")


class BootstrapStaticFieldWidget(object):
    """Render a static Bootstrap control."""

    def __call__(self, field, **kwargs):
        kwargs["class_"] = u"form-control-static"
        # Assume that the field provides access to its value.
        value = field._value()
        return HTMLString(u''.join([
            u'<p {}>'.format(html_params(**kwargs)),
            value,
            u'</p>',
        ]))


def decorators(widget):
    """
    Yields all decorators of a widget starting from the outermost.
    """
    while isinstance(widget, WidgetDecorator):
        yield type(widget)
        widget = widget.widget


def decorate(widget, *decorators):
    """
    Decorate a widget with a list of decorators.
    :param widget: a widget
    :param tuple[WidgetDecorator] decorators: some decorators
    :rtype: WidgetDecorator
    :returns: decorated widget
    """
    return reduce(lambda w, d: d(w), decorators, widget)


def decorate_field(field, *decorators):
    """
    Return a field's widget decorated with the given decorators..
    :param wtforms.fields.core.Field field: a WTForms field
    :param tuple[WidgetDecorator] decorators: some decorators
    :rtype: WidgetDecorator
    :returns: decorated widget
    """
    return decorate(field.widget, *decorators)


from markupsafe import Markup


class BootstrapDatepickerWidget(object):
    """Renders datetime fields using bootstrap-datepicker."""

    def __call__(self, field, **kwargs):
        kwargs["data-provide"] = u"datepicker"
        for (option, value) in field.datepicker_options.items():
            attribute = 'data-date-{0}'.format(option.replace('_', '-'))
            kwargs[attribute] = value
        options = dict(kwargs, name=field.name)
        if field.data:
            options["value"] = field.data
        return HTMLString(u"<input {0}>".format(html_params(**options)))


class CheckBoxWidget(wtforms.widgets.Select):
    """A simple multi selection widget rendered as Checkbox list.

    It uses the bootstrap markup.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'checkbox')
        field_id = kwargs.pop('id', field.id)
        html = []
        for value, label, checked in field.iter_choices():
            choice_id = u'{}-{}'.format(field_id, value)
            options = dict(kwargs, name=field.name, value=value, id=choice_id)
            html.append(u'<label class="checkbox" {}>'.format(html_params(id=field_id)))
            if checked:
                options['checked'] = 'checked'
            html.append(u'<input {}>'.format(html_params(**options)))
            html.append(label)
            html.append(u'</label>')
        return u''.join(html)


class BootstrapFormSelectDecorator(WidgetDecorator):
    def __call__(self, field, **kwargs):
        classes = kwargs.get('class_', '').split()
        kwargs['class_'] = ' '.join(classes + ['form-select'])
        return self.widget(field, **kwargs)


class LazyLoadSelectWidget(wtforms.widgets.Select):
    """This is the widget for the LazyLoadSelectField

    Please look at web.form.fields.LazyLoadSelectField for more information.
    """

    def __call__(self, field, **kwargs):
        conditions = getattr(field, "conditions", None)
        if conditions is not None:
            kwargs["data-fieldids"] = ",".join(conditions)
        kwargs['data-role'] = u'lazy-load-select'
        kwargs['data-url'] = url_for(field.data_endpoint)
        kwargs['value'] = str(field.data)

        return super(LazyLoadSelectWidget, self).__call__(field, **kwargs)


class Disabler(WidgetDecorator):
    def __call__(self, field, **kwargs):
        kwargs['disabled'] = True
        return self.widget(field, **kwargs)


class MoneyFieldDecorator(WidgetDecorator):
    """Adds the Bootstrap form-control class to a widget."""

    def __call__(self, field, **kwargs):
        kwargs['class_'] += ' money-amount'
        group_cls = 'input-group' + (' is-invalid' if field.errors else '')
        return Markup(
            '<div class="{}">{}<span class="input-group-text">€</span></div>'
        ).format(group_cls, self.widget(field, **kwargs))


class MacFieldDecorator(WidgetDecorator):
    """Adds an addon which shows the vendor."""

    def __call__(self, field, **kwargs):
        group_cls = 'input-group' + (' is-invalid' if field.errors else '')
        return Markup(
            '<div class="{}">{}<div class="input-group-text mac-manufacturer">?</div></div>'
        ).format(group_cls, self.widget(field, **kwargs))
