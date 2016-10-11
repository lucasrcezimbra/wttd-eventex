from django.test import TestCase
from django.core.exceptions import ValidationError
from eventex.core.models import Speaker, Contact

class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Lucas Rangel Cezimbra',
            slug='lucas-rangel-cezimbra',
            photo='http://hbn.link/hb-pic',
        )

    def test_email(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='lucas.cezimbra@gmail.com',
        )

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.PHONE,
            value='(51) 8210.0596',
        )

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='X', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL,
            value='lucas.cezimbra@gmail.com')

        self.assertEqual('lucas.cezimbra@gmail.com', str(contact))

class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Lucas Rangel Cezimbra',
            slug='lucas-rangel-cezimbra',
            photo='http://lalala.com.br/x.png'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='lucas.cezimbra@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='51 8210.0596')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['lucas.cezimbra@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['51 8210.0596']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
