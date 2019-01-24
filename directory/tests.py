from django.test import TestCase

from .models import CertifiedCoach
from .service import DirectoryService

class DirectoryServiceTests(TestCase):
    def _create_country_coaches(self, show_in_directory=1):
        country_coaches = [
            ('Bill Gates', 'United States'),
            ('Frederick Banting', 'Canada'),
            ('Steven Hawking', 'United Kingdom'),
            ('Carl Freidrich Gauss', 'Germany'),
            ('Plato', 'Greece'),
        ]
        for name,country in country_coaches:
            CertifiedCoach.objects.create(fullname=name, country=country,
                show_in_directory=show_in_directory)

    def _create_90210_coaches(self, show_in_directory=1):
        beverly_hills_coaches = [
            ('Kelly', '90211'),
            ('Dylan', '90210'),
            ('Brandon', '90210')
        ]
        for name,postal_code in beverly_hills_coaches:
            CertifiedCoach.objects.create(fullname=name, postal_code=postal_code,
                show_in_directory=show_in_directory)

    def _create_coaches_named_jon(self, show_in_directory=1):
        famous_jons = ['Jon Hamm', 'Jon Bon Jovi', 'Jon Stewart', 'Jon Voight',
            'Lil Jon', 'Jon Lovitz', 'Jon Favreau']
        for jon in famous_jons:
            CertifiedCoach.objects.create(fullname=jon,
                show_in_directory=show_in_directory)

    def test_search_by_country_handles_blank(self):
        self.assertEqual(DirectoryService.find_by_country('').count(), 0)

    def test_search_by_country_with_valid_country(self):
        self._create_country_coaches()
        canadian_coaches = DirectoryService.find_by_country('canada')
        self.assertEqual(canadian_coaches.count(), 1)
        self.assertEqual(canadian_coaches[0].fullname, 'Frederick Banting')

    def test_search_by_country_ignores_partial_country(self):
        self._create_country_coaches(show_in_directory=1)
        canadian_coaches = DirectoryService.find_by_country('can')
        self.assertEqual(canadian_coaches.count(), 0)

    def test_search_by_country_does_not_return_hidden_records(self):
        self._create_country_coaches(show_in_directory=0)
        canadian_coaches = DirectoryService.find_by_country('canada')
        self.assertEqual(canadian_coaches.count(), 0)

    def test_search_by_postal_code_handles_blank(self):
        self.assertEqual(DirectoryService.find_by_postal_code('').count(), 0)

    def test_search_by_postal_code_with_valid_code(self):
        self._create_90210_coaches()
        beverly_hills_coaches = DirectoryService.find_by_postal_code('90210')
        self.assertEqual(beverly_hills_coaches.count(), 2)
        self.assertEqual(sorted([c.fullname for c in beverly_hills_coaches]),
            ['Brandon', 'Dylan'])

    def test_search_by_postal_code_does_fuzzy_match(self):
        self._create_90210_coaches()
        beverly_hills_coaches = DirectoryService.find_by_postal_code('902')
        self.assertEqual(beverly_hills_coaches.count(), 3)
        self.assertEqual(sorted([c.fullname for c in beverly_hills_coaches]),
            ['Brandon', 'Dylan', 'Kelly'])

    def test_search_by_postal_code_does_not_return_hidden_records(self):
        self._create_90210_coaches(show_in_directory=0)
        beverly_hills_coaches = DirectoryService.find_by_postal_code('90210')
        self.assertEqual(beverly_hills_coaches.count(), 0)

    def test_search_by_coach_name_handles_blank(self):
        self.assertEqual(DirectoryService.find_by_coach_name('').count(), 0)

    def test_search_by_coach_name_does_valid_partial_search(self):
        self._create_coaches_named_jon()
        coaches_named_jon = DirectoryService.find_by_coach_name('Lil')
        self.assertEqual(coaches_named_jon.count(), 1)
        self.assertEqual(coaches_named_jon[0].fullname, 'Lil Jon')

    def test_search_by_coach_name_does_fuzzy_search(self):
        self._create_coaches_named_jon()
        coaches_named_jon = DirectoryService.find_by_coach_name('jon')
        self.assertEqual(coaches_named_jon.count(), 7)

    def test_search_by_coach_does_not_return_hidden_records(self):
        self._create_coaches_named_jon(show_in_directory=0)
        coaches_named_jon = DirectoryService.find_by_coach_name('Jon')
        self.assertEqual(coaches_named_jon.count(), 0)


class CertifiedCoachModelTests(TestCase):
    def test_location_property_has_all_address_fields(self):
        addr = CertifiedCoach.objects.create(address1='317 Dundas St W', address2='Suite 1',
            city='Toronto', province='ON', postal_code='M5T 1G4', country='Canada')
        self.assertEqual(addr.location, '317 Dundas St W, Suite 1, Toronto, ON M5T 1G4, Canada')

    def test_location_property_excludes_address2(self):
        addr = CertifiedCoach.objects.create(address1='317 Dundas St W', address2='',
            city='Toronto', province='ON', postal_code='M5T 1G4', country='Canada')
        self.assertEqual(addr.location, '317 Dundas St W, Toronto, ON M5T 1G4, Canada')

    def test_location_property_handles_missing_fields(self):
        addr = CertifiedCoach.objects.create(address1='', address2='',
            city='Toronto', province='ON', postal_code='', country='Canada')
        self.assertEqual(addr.location, 'Toronto, ON, Canada')

    def test_certification_level_is_blank(self):
        no_certs = CertifiedCoach.objects.create(level1_status=0, level2_status=0,
            procoach_status=0)
        self.assertEqual(no_certs.certification_level, '')

    def test_certification_level_is_level1(self):
        certs = CertifiedCoach.objects.create(level1_status=1, level2_status=0,
            procoach_status=0)
        self.assertEqual(certs.certification_level, 'Level 1')

    def test_certification_level_is_level1_and_2(self):
        certs = CertifiedCoach.objects.create(level1_status=1, level2_status=1,
            procoach_status=0)
        self.assertEqual(certs.certification_level, 'Level 1,Level 2')

    def test_certification_level_is_all(self):
        certs = CertifiedCoach.objects.create(level1_status=1, level2_status=1,
            procoach_status=1)
        self.assertEqual(certs.certification_level, 'Level 1,Level 2,Procoach')

    def test_certification_level_is_procoach(self):
        certs = CertifiedCoach.objects.create(level1_status=0, level2_status=0,
            procoach_status=1)
        self.assertEqual(certs.certification_level, 'Procoach')
