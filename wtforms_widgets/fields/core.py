import re
import typing as t
from datetime import datetime
from itertools import chain

import wtforms

from ..widgets import decorate_field, BootstrapFormControlDecorator, \
    BootstrapStandardDecorator, \
    BootstrapRadioDecorator, BootstrapCheckboxDecorator, \
    BootstrapFieldListWidget, BootstrapFormFieldWidget, \
    BootstrapDatepickerWidget, MoneyFieldDecorator, decorate, \
    BootstrapFormSelectDecorator


class SelectField(wtforms.fields.SelectField):
    widget = decorate_field(
        wtforms.fields.SelectField,
        BootstrapFormControlDecorator,
        BootstrapFormSelectDecorator,
        BootstrapStandardDecorator,
    )


class SelectMultipleField(wtforms.fields.SelectMultipleField):
    widget = decorate_field(
        wtforms.fields.SelectMultipleField,
        BootstrapFormControlDecorator,
        BootstrapFormSelectDecorator,
        BootstrapStandardDecorator,
    )


class RadioField(wtforms.fields.RadioField):
    widget = BootstrapFieldListWidget()
    option_widget = decorate(
        wtforms.widgets.RadioInput(),
        BootstrapRadioDecorator,
    )


class StringField(wtforms.fields.StringField):
    widget = decorate_field(
        wtforms.fields.StringField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class TextField(StringField):
    pass


class IntegerField(wtforms.fields.IntegerField):
    widget = decorate_field(
        wtforms.fields.IntegerField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class DecimalField(wtforms.fields.DecimalField):
    widget = decorate_field(
        wtforms.fields.DecimalField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class MoneyField(wtforms.fields.DecimalField):
    widget = decorate_field(
        wtforms.fields.DecimalField,
        MoneyFieldDecorator,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(MoneyField, self).process_formdata(valuelist)


class FloatField(wtforms.fields.FloatField):
    widget = decorate_field(
        wtforms.fields.FloatField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class BooleanField(wtforms.fields.BooleanField):
    widget = decorate_field(
        wtforms.fields.BooleanField,
        BootstrapCheckboxDecorator,
    )


class DateTimeField(wtforms.fields.DateTimeField):
    widget = decorate(
        BootstrapDatepickerWidget(),
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class TimeField(wtforms.fields.TimeField):
    widget = decorate_field(
        wtforms.fields.TimeField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class DateField(wtforms.fields.DateField):
    widget = decorate(
        BootstrapDatepickerWidget(),
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )
    supported_directives = {
        'd': 'dd',
        'm': 'mm',
        'a': 'D',
        'A': 'DD',
        'b': 'M',
        'B': 'MM',
        'y': 'yy',
        'Y': 'yyyy',
    }
    unsupported_directives = set(iter("wHIPMSfzZjUWcxX"))
    format_string_pattern = re.compile(r"(%+)([^%]|$)", re.M)
    # Set literals are only supported in Python 2.7 or higher
    available_datepicker_options = {
        "autoclose", "before_show_day", "calendar_weeks", "clear_btn",
        "days_of_week_disabled", "end_date", "force_parse", "format",
        "keyboard_navigation", "language", "min_view_mode", "multidate",
        "multidate_separator", "orientation", "start_date", "start_view",
        "today_btn", "today_highlight", "week_start"
    }

    def __init__(self, label=None, validators=None, format='%Y-%m-%d',
                 **kwargs):
        # Move Bootstrap datepicker specific options to its own dict
        self.datepicker_options = dict((
            (option, value) for (option, value) in kwargs.items()
            if option in self.available_datepicker_options
        ))
        for option in self.datepicker_options.keys():
            kwargs.pop(option)
        defaults = {'default': datetime.utcnow(), 'language': 'de',
                    'today_highlight': 'true', 'today_btn': 'linked'}
        self.datepicker_options = dict(chain(defaults.items(),
                                             self.datepicker_options.items()))
        # The format option is used by both DateField and Bootstrap datepicker,
        # albeit with a different format string syntax.
        self.datepicker_options['format'] = self.convert_format_string(format)
        super(DateField, self).__init__(label, validators, format, **kwargs)

    @classmethod
    def _replacement_function(cls, match):
        percentage_signs = match.group(1)
        percentage_sign_count = len(percentage_signs)
        directive = match.group(2)
        # Even number of percentage signs => all percentages are escaped
        if percentage_sign_count % 2 == 0:
            replacement = directive
        elif directive in cls.supported_directives:
            replacement = cls.supported_directives[directive]
        elif directive in cls.unsupported_directives:
            message = "Format directive %{} not supported by " \
                      "Bootstrap datepicker.".format(directive)
            raise ValueError(message)
        else:
            message = "Unknown format directive: %{}".format(directive)
            raise ValueError(message)
        return percentage_signs[0:percentage_sign_count // 2] + replacement

    @classmethod
    def convert_format_string(cls, format):
        """
        Convert a datetime strftime/strptime to a Bootstrap datepicker format
        string.
        """
        return cls.format_string_pattern.sub(cls._replacement_function, format)


class TextAreaField(wtforms.fields.TextAreaField):
    widget = decorate_field(
        wtforms.fields.TextAreaField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class PasswordField(wtforms.fields.PasswordField):
    widget = decorate_field(
        wtforms.fields.PasswordField,
        BootstrapFormControlDecorator,
        BootstrapStandardDecorator,
    )


class FileField(wtforms.fields.FileField):
    widget = decorate_field(
        wtforms.fields.FileField,
        BootstrapStandardDecorator,
    )


# No need to decorate wtforms.fields.HiddenField
HiddenField = wtforms.fields.HiddenField


class SubmitField(wtforms.fields.SubmitField):
    widget = decorate_field(
        wtforms.fields.SubmitField,
    )


try:
    import wtforms_sqlalchemy.fields
except ImportError:
    def __getattr__(name: str) -> t.Any:
        if name in ("QuerySelectField", "QuerySelectmultipleField"):
            raise AttributeError(
                f"To use the {name!r}, install `wtforms_sqalalchemy`"
                " via the `[sql]` optional dependency group"
                " (`pip install wtforms-widgets[sql]`)"
            )
        raise AttributeError(f"module {__name__!r} has on attribute {name!r}!")
else:
    class QuerySelectField(
        wtforms_sqlalchemy.fields.QuerySelectField
    ):
        widget = decorate_field(
            wtforms_sqlalchemy.fields.QuerySelectField,
            BootstrapFormControlDecorator,
            BootstrapFormSelectDecorator,
            BootstrapStandardDecorator,
        )


    class QuerySelectMultipleField(
        wtforms_sqlalchemy.fields.QuerySelectMultipleField
    ):
        widget = decorate_field(
            wtforms_sqlalchemy.fields.QuerySelectMultipleField,
            BootstrapFormControlDecorator,
            BootstrapFormSelectDecorator,
            BootstrapStandardDecorator,
        )


class FieldList(wtforms.fields.FieldList):
    widget = BootstrapFieldListWidget()


class FormField(wtforms.fields.FormField):
    widget = BootstrapFormFieldWidget()
