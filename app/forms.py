from flask_wtf import FlaskForm
from wtforms import validators, StringField, BooleanField, IntegerField, SelectMultipleField, DecimalField, widgets
from wtforms.validators import DataRequired

choices = (('Ethical', 'Ethical Investing'),
            ('Growth', 'Growth Investing'),
           ('Index', 'Index Investing'),
           ('Quality', 'Quality Investing'),
           ('Value', 'Value Investing')
)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class InvestForm(FlaskForm):
    strategies = MultiCheckboxField(u'Strategy', choices=choices)
    amount = DecimalField(u'amount', [validators.required("Please Enter your birthdate"),
                                     validators.NumberRange(message="It mush be at least 5000", min=5000, max=1.7976931348623157e+308)])
