from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        form = self.make_validated_form(name='LUCAS rangel cEZIMBRA')
        self.assertEqual('Lucas Rangel Cezimbra', form.cleaned_data['name'])

    def test_email_is_optional(self):
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))
        self.assertFormErrorMessage(form, '__all__', 'Informe seu e-mail ou telefone.')

    def test_error_when_email_invalid_and_phone_empty(self):
        form = self.make_validated_form(email='asdfsdf', phone='')
        self.assertFormErrorMessage(form, '__all__', 'Informe seu e-mail ou telefone.')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Lucas Rangel Cezimbra', cpf='12345678901',
                   email='lucas.cezimbra@gmail.com', phone='(51)82100596')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertEqual([msg], errors_list)
