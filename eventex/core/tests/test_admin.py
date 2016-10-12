from django.contrib import admin
from django.test import TestCase
from eventex.core.admin import TalkModelAdmin, SpeakerModelAdmin, ContactInline
from eventex.core.models import Contact, Course, Speaker, Talk
from eventex.core.models import Talk, Course
from unittest.mock import Mock

class ContactAdminTest(TestCase):
    def test_verbose_name(self):
        verbose_name = Contact._meta.verbose_name
        self.assertEqual(verbose_name, 'contato')

    def test_verbose_name_plural(self):
        verbose_name_plural = Contact._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'contatos')

    def test_verbose_name_attrs(self):
        attrs = [('speaker', 'palestrante'),
                 ('kind', 'tipo'),
                 ('value', 'valor')]

        for attr, expected in attrs:
            with self.subTest():
                verbose_name = Contact._meta.get_field(attr).verbose_name
                self.assertEqual(verbose_name, expected)


class ContactInlineAdminTest(TestCase):
    def setUp(self):
        self.contact_inline = ContactInline(Mock(), admin.site)

    def test_model(self):
        self.assertEqual(Contact, self.contact_inline.model)

    def test_extra(self):
        self.assertEqual(1, self.contact_inline.extra)

class SpeakerAdminTest(TestCase):
    def setUp(self):
        self.model_admin = SpeakerModelAdmin(Speaker, admin.site)

    def test_verbose_name(self):
        verbose_name = Speaker._meta.verbose_name
        self.assertEqual(verbose_name, 'palestrante')

    def test_verbose_name_plural(self):
        verbose_name_plural = Speaker._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'palestrantes')

    def test_verbose_name_attrs(self):
        attrs = [('name', 'nome'),
                 ('slug', 'slug'),
                 ('photo', 'foto'),
                 ('website', 'website'),
                 ('description', 'descrição')]

        for attr, expected in attrs:
            with self.subTest():
                verbose_name = Speaker._meta.get_field(attr).verbose_name
                self.assertEqual(verbose_name, expected)

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Speaker))

    def test_model_admin_is_registered(self):
        self.assertTrue(isinstance(self.model_admin, SpeakerModelAdmin))

    def test_inlines(self):
        self.assertEqual([ContactInline], self.model_admin.inlines)

    def test_prepopulated_fields(self):
        self.assertEqual({'slug': ('name', )}, self.model_admin.prepopulated_fields)

    def test_list_display(self):
        expected = ['name', 'photo_img', 'website_link', 'email', 'phone']
        self.assertEqual(expected, self.model_admin.list_display)

    def test_website_link(self):
        website = 'http://lrcezimbra.com.br'
        website_link = self.model_admin.website_link(Speaker(website=website))
        expected = '<a href="{0}">{0}</a>'.format(website)
        self.assertEqual(expected, website_link)

    def test_website_link_attrs(self):
        self.assertTrue(self.model_admin.website_link.allow_tags)
        self.assertEqual('website', self.model_admin.website_link.short_description)

    def test_photo_img(self):
        photo = '/www1.png'
        photo_img = self.model_admin.photo_img(Speaker(photo=photo))
        expected = '<img width="32px" src="{}" />'.format(photo)
        self.assertEqual(expected, photo_img)

    def test_photo_img_attrs(self):
        self.assertTrue(self.model_admin.photo_img.allow_tags)
        self.assertEqual('foto', self.model_admin.photo_img.short_description)

    def test_email_attrs(self):
        self.assertEqual('e-mail', self.model_admin.email.short_description)

    def test_phone_attrs(self):
        self.assertEqual('telefone', self.model_admin.phone.short_description)


class TalkAdminTest(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(
            title='Titulo da Palestra',
        )
        self.course = Course.objects.create(
            title='Título do Curso',
            start='09:00',
            description='Descrição do Curso',
            slots=20
        )

    def test_verbose_name(self):
        verbose_name = Talk._meta.verbose_name
        self.assertEqual('palestra', verbose_name)

    def test_verbose_name_plural(self):
        verbose_name_plural = Talk._meta.verbose_name_plural
        self.assertEqual('palestras', verbose_name_plural)

    def test_ordering(self):
        self.assertListEqual(['start'], Course._meta.ordering)

    def test_verbose_name_attrs(self):
        attrs = [('title', 'título'),
                 ('start', 'início'),
                 ('description', 'descrição'),
                 ('speakers', 'palestrantes')]

        for attr, expected in attrs:
            with self.subTest():
                verbose_name = Talk._meta.get_field(attr).verbose_name
                self.assertEqual(verbose_name, expected)

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Talk))

    def test_queryset_dont_get_courses(self):
        talk_model_admin = TalkModelAdmin(Talk, admin.site)
        talks = talk_model_admin.get_queryset(Mock())
        self.assertEqual(1, talks.count())

    def test_model_admin_is_registered(self):
        model_admin = admin.site._registry.get(Talk)
        self.assertTrue(isinstance(model_admin, TalkModelAdmin))


class CourseAdminTest(TestCase):
    def test_verbose_name(self):
        verbose_name = Course._meta.verbose_name
        self.assertEqual('curso', verbose_name)

    def test_verbose_name_plural(self):
        verbose_name_plural = Course._meta.verbose_name_plural
        self.assertEqual('cursos', verbose_name_plural)

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Course))
