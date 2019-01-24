from django.http import HttpResponse
from django.shortcuts import render

from pnapp.api import ApiGetView
from .service import DirectoryService

class SearchDirectory(ApiGetView):
    """Search the certified coach directory by country, postal_code, or
    coach_name. Return json data in the shape:
        {
            "objects": [
                {
                    "id": <int>,
                    "name": <string>,
                    "certification_level": <string>,
                    "tagline": <string>,
                    "business_name": <string>,
                    "location": <string>,
                    "mobile": <string>,
                    "website": <string>,
                    "email": <string>
                }, ...
            ]
        }
    """
    MAX_RESULTS = 50

    @staticmethod
    def _apply_coach_directory_shape(coach):
        return dict(
            id=coach.id,
            name=coach.fullname,
            certification_level=coach.certification_level,
            tagline=coach.specialty,
            business_name=coach.business_name,
            location=coach.location,
            mobile=coach.mobile_phone,
            website=coach.url,
            email=coach.email
        )

    def api_get(self, request, *args, **kwargs):
        country = request.GET.get('country', '').strip()
        postal_code = request.GET.get('postal_code', '').strip()
        coach_name = request.GET.get('name', '').strip()
        coaches = None

        if country:
            coaches = DirectoryService.find_by_country(country)
        elif postal_code:
            coaches = DirectoryService.find_by_postal_code(postal_code)
        elif coach_name:
            coaches = DirectoryService.find_by_coach_name(coach_name)

        if coaches:
            return dict(
                objects=[SearchDirectory._apply_coach_directory_shape(coach) \
                    for coach in coaches[:self.MAX_RESULTS]]
            )

        return None
