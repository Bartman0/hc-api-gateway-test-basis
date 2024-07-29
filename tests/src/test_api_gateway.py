import pytest

from base_test_data import (
    transform_request_amsterdam_landelijk,
    transform_request_filters,
    is_zoekvraag_authorised,
    is_amsterdam_authorised,
    is_landelijk_authorised,
    is_inclusief_overledenen_authorised,
    has_amsterdam_query_parameter,
    has_gemeente_van_inschrijving_query_parameter,
    has_bevragen_authorisation,
    has_inclusief_overledenen_query_parameter,
    FUNCTIONALITY_ZOEKVRAGEN,
    FIELDS_PERSOON_BASIS,
    FIELDS_KINDEREN,
    FIELDS_ADRES,
    TOKEN_USER_A,
    TOKEN_USER_B,
    TOKEN_USER_C,
)


def make_fields_uniform(request):
    request["fields"] = sorted(request["fields"])


@pytest.mark.parametrize(
    "hc_ams_request, hc_api_request, token, status_code",
    [
        (
            {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": "Verhuis*",
                "geboortedatum": "2002-07-01",
                "inclusiefOverledenPersonen": True,
            },
            {
                "type": "ZoekMetGeslachtsnaamEnGeboortedatum",
                "geslachtsnaam": "Verhuis*",
                "geboortedatum": "2002-07-01",
                "gemeenteVanInschrijving": "0363",
                "inclusiefOverledenPersonen": True,
                "fields": list(set(FIELDS_PERSOON_BASIS)),
            },
            TOKEN_USER_A,
            200,
        ),
        (
            {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"]["gob_brp_raadplegen_bsn"],
                "burgerservicenummer": ["999993653"],
            },
            {
                "type": "RaadpleegMetBurgerservicenummer",
                "burgerservicenummer": ["999993653"],
                "gemeenteVanInschrijving": "0363",
                "fields": list(set(FIELDS_PERSOON_BASIS + FIELDS_KINDEREN)),
            },
            TOKEN_USER_B,
            200,
        ),
        (
            {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_postcode_huisnummer"
                ],
                "postcode": "2593 BL",
                "huisnummer": "101",
            },
            {
                "type": "ZoekMetPostcodeEnHuisnummer",
                "postcode": "2593 BL",
                "huisnummer": "101",
                "fields": list(
                    set(FIELDS_PERSOON_BASIS + FIELDS_KINDEREN + FIELDS_ADRES)
                ),
            },
            TOKEN_USER_C,
            200,
        ),
    ],
)
class TestClass:
    """
    Test of de aanroeper gebruik mag maken van de Bevragen functionaliteit
    """

    def test_bevragen_authorisation(
        self, hc_ams_request, hc_api_request, token, status_code
    ):
        assert has_bevragen_authorisation(hc_ams_request, token)

    """
    Test of de aanroeper de aangeduide zoekvraag mag uitvoeren
    """

    def test_zoekvraag_authorisation(
        self, hc_ams_request, hc_api_request, token, status_code
    ):
        assert is_zoekvraag_authorised(hc_ams_request, token)

    """
    Test of de aanroeper voldoet aan de scope waar ie recht op heeft: landelijk of amsterdam
    """

    def test_amsterdam_landelijk_validation(
        self, hc_ams_request, hc_api_request, token, status_code
    ):
        request_result = transform_request_amsterdam_landelijk(hc_ams_request, token)
        if is_amsterdam_authorised(token):
            assert has_amsterdam_query_parameter(request_result)
        if is_landelijk_authorised(token):
            assert not (has_gemeente_van_inschrijving_query_parameter(request_result))

    """
    Test of de aanroeper de query parameter 'inclusiefOverledenPersonen' mag toepassen of niet
    """

    def test_inclusief_overledenen_validation(
        self, hc_ams_request, hc_api_request, token, status_code
    ):
        request_result = transform_request_amsterdam_landelijk(hc_ams_request, token)
        if has_inclusief_overledenen_query_parameter(request_result):
            assert is_inclusief_overledenen_authorised(token)

    """
    Test of de filters goed worden gezet in het HC request op basis van de verleende data scopes 
    """

    def test_request_filters(self, hc_ams_request, hc_api_request, token, status_code):
        request_result = transform_request_filters(hc_ams_request, token)
        request_result = make_fields_uniform(request_result)
        hc_api_request = make_fields_uniform(hc_api_request)
        assert request_result == hc_api_request
