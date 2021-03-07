# wtforms-widgets
Decorator driven wtforms extension with Bootstrap 4 support for Flask

Copyright (c) The Pycroft Authors. See the [AUTHORS](https://github.com/agdsn/pycroft/blob/develop/AUTHORS) file.

Install with
```
pip install wtforms-widgets
```

Initialize your form with `wtforms_widgets.base_form.BaseForm` instead of `flask_wtf.FlaskForm` or `wtforms.Form`.

Import the `StringField` and `PasswordField` from `wtforms_widgets.fields.core`.
```
from wtforms import validators

from wtforms.validators import Email
from wtforms_widgets.base_form import BaseForm
from wtforms_widgets.fields.core import StringField, PasswordField

class RegisterForm(BaseForm):
    email = StringField('Email Address', [Email(), validators.DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [validators.DataRequired(message='Must provide a password. ;-)')])
```

Displaying the form in jinja is much simpler and looks great.
```
<form method="POST" action="{{ url_for('auth.register') }}" accept-charset="UTF-8" role="form">
    {% for field in form %}
        {{ field(render_mode='horizontal', autocomplete='off') }}
    {% endfor %}
    <input type="submit" value="submit">
</form>
```

# Available field types

- SelectField
- SelectMultipleField
- RadioField
- StringField / TextField
- IntegerField
- DecimalField
- MoneyField
- FloatField
- BooleanField
- DateTimeField
- DateField (with [bootstrap-datepicker](https://www.npmjs.com/package/bootstrap-datepicker))
- TextAreaField
- PasswordField
- FileField
- HiddenField
- SubmitField
- QuerySelectField
- QuerySelectMultipleField
- FieldList
- FormField
- TypeaheadField
- ReadonlyTextField
- MacField
