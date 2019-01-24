
from  .models import CertifiedCoach

class DirectoryService():
    @classmethod
    def find_by_country(cls, country):
        """Get a list of certified coaches by country, matched against `country`
        in a case-insensitive exact text lookup."""
        return CertifiedCoach.objects.filter(country__iexact=country,
            show_in_directory=1)

    @classmethod
    def find_by_postal_code(cls, postal_code):
        """Get a list of certified coaches by postal code, matched against
        `postal_code`, including partial matches."""
        return CertifiedCoach.objects.filter(postal_code__icontains=postal_code,
            show_in_directory=1)

    @classmethod
    def find_by_coach_name(cls, coach_name):
        """Get a list of certified coaches by name, performing a fulltext search
        against `coach_name`."""
        return CertifiedCoach.objects.filter(fullname__search=coach_name,
            show_in_directory=1)
