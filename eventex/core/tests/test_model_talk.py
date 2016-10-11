from django.test import TestCase
from eventex.core.models import Talk
from eventex.core.managers import PeriodManager

class  TalkModelTest(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(
            title='Titulo da Palestra',
        )

    def test_create(self):
        self.assertTrue(Talk.objects.exists())

    def test_has_speakers(self):
        self.talk.speakers.create(
            name='Lucas Rangel Cezimbra',
            slug='lucas-rangel-cezimbra',
            website='lrcezimbra.com.br'
        )

        self.assertEqual(1, self.talk.speakers.count())

    def test_description_blank(self):
        field = Talk._meta.get_field('description')
        self.assertTrue(field.blank)

    def test_speaker_blank(self):
        field = Talk._meta.get_field('speakers')
        self.assertTrue(field.blank)

    def test_start_blank(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.blank)

    def test_start_null(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.null)

    def test_str(self):
        self.assertEqual('Titulo da Palestra', str(self.talk))

class PeriodManagerTest(TestCase):
    def setUp(self):
        Talk.objects.create(title='Morning Talk', start='11:59')
        Talk.objects.create(title='Afternoon Talk', start='12:00')

    def test_manager(self):
        self.assertIsInstance(Talk.objects, PeriodManager)

    def test_at_morning(self):
        qs = Talk.objects.at_morning()
        expected = ['Morning Talk']
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)

    def test_at_afternoon(self):
        qs = Talk.objects.at_afternoon()
        expected = ['Afternoon Talk']
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)
