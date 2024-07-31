import json
import pytest

from base_test_data import (
    make_fields_uniform,
    transform_request_amsterdam_landelijk,
    transform_request,
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
    FIELDS_NAAM,
    TOKEN_USER_A,
    TOKEN_USER_B,
    TOKEN_USER_C,
)
from hc_request import BrpRequest


@pytest.mark.parametrize(
    "hc_ams_request, hc_api_request, token, expected_response",
    [
        (
            {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": "Braber*",
                "geboortedatum": "1968-03-18",
                "inclusiefOverledenPersonen": True,
            },
            {
                "type": "ZoekMetGeslachtsnaamEnGeboortedatum",
                "geslachtsnaam": "Braber*",
                "geboortedatum": "1968-03-18",
                "gemeenteVanInschrijving": "0363",
                "inclusiefOverledenPersonen": True,
                "fields": list(set(FIELDS_PERSOON_BASIS)),
            },
            TOKEN_USER_A,
            {
                "personen": [
                    {
                        "burgerservicenummer": "999994542",
                        "geboorte": {
                            "datum": {
                                "datum": "1968-03-18",
                                "langFormaat": "18 maart 1968",
                                "type": "Datum"
                            }
                        },
                        "leeftijd": 56,
                    }
                ],
                "type": "ZoekMetGeslachtsnaamEnGeboortedatum"
            }
        ),
        (
            {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"]["gob_brp_raadplegen_bsn"],
                "burgerservicenummer": ["999994542"],
            },
            {
                "type": "RaadpleegMetBurgerservicenummer",
                "burgerservicenummer": ["999994542"],
                "gemeenteVanInschrijving": "0363",
                "fields": list(set(FIELDS_PERSOON_BASIS + FIELDS_KINDEREN)),
            },
            TOKEN_USER_B,
            {
                "type": "RaadpleegMetBurgerservicenummer",
                "personen": [
                    {
                        "burgerservicenummer": "999994542",
                        "leeftijd": 56,
                        "geboorte": {
                            "land": {
                                "code": "6030",
                                "omschrijving": "Nederland"
                            },
                            "plaats": {
                                "code": "0518",
                                "omschrijving": "'s-Gravenhage"
                            },
                            "datum": {
                                "type": "Datum",
                                "datum": "1968-03-18",
                                "langFormaat": "18 maart 1968"
                            }
                        },
                        "kinderen": [
                            {
                                "burgerservicenummer": "999995807",
                                "naam": {
                                    "voornamen": "Zoey",
                                    "voorvoegsel": "den",
                                    "geslachtsnaam": "Braber",
                                    "voorletters": "Z."
                                },
                                "geboorte": {
                                    "land": {
                                        "code": "6030",
                                        "omschrijving": "Nederland"
                                    },
                                    "plaats": {
                                        "code": "0363",
                                        "omschrijving": "Amsterdam"
                                    },
                                    "datum": {
                                        "type": "Datum",
                                        "datum": "2018-11-14",
                                        "langFormaat": "14 november 2018"
                                    }
                                }
                            },
                            {
                                "burgerservicenummer": "999995832",
                                "naam": {
                                    "voornamen": "Alexander",
                                    "voorvoegsel": "den",
                                    "geslachtsnaam": "Braber",
                                    "voorletters": "A."
                                },
                                "geboorte": {
                                    "land": {
                                        "code": "6030",
                                        "omschrijving": "Nederland"
                                    },
                                    "plaats": {
                                        "code": "0363",
                                        "omschrijving": "Amsterdam"
                                    },
                                    "datum": {
                                        "type": "Datum",
                                        "datum": "2009-05-29",
                                        "langFormaat": "29 mei 2009"
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        ),
        (
            {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_postcode_huisnummer"
                ],
                "postcode": "3078CE",
                "huisnummer": "1",
            },
            {
                "type": "ZoekMetPostcodeEnHuisnummer",
                "postcode": "3078CE",
                "huisnummer": "1",
                "fields": list(
                    set(FIELDS_PERSOON_BASIS + FIELDS_NAAM)
                ),
            },
            TOKEN_USER_C,
            {
                "type": "ZoekMetPostcodeEnHuisnummer",
                "personen": [
                    {
                        "burgerservicenummer": "999993021",
                        "geboorte": {
                            "datum": {
                                "type": "Datum",
                                "datum": "1926-05-05",
                                "langFormaat": "5 mei 1926"
                            }
                        },
                        "leeftijd": 98,
                        "naam": {
                            "voornamen": "Leonardus Fredericus",
                            "geslachtsnaam": "Kierkegaard",
                            "voorletters": "L.F.",
                            "volledigeNaam": "Leonardus Fredericus Kierkegaard"
                        }
                    },
                    {
                        "burgerservicenummer": "999995078",
                        "geboorte": {
                            "datum": {
                                "type": "Datum",
                                "datum": "1928-09-05",
                                "langFormaat": "5 september 1928"
                            }
                        },
                        "leeftijd": 95,
                        "naam": {
                            "voornamen": "Christina Maria",
                            "geslachtsnaam": "Maassen",
                            "voorletters": "C.M.",
                            "volledigeNaam": "Christina Maria Maassen"
                        }
                    }
                ]
            }
        ),
    ],
)
class TestPositives:
    """
    Test of de aanroeper gebruik mag maken van de Bevragen functionaliteit
    """
    def test_bevragen_authorisation(self, hc_ams_request, hc_api_request, token, expected_response):
        assert has_bevragen_authorisation(hc_ams_request, token)

    """
    Test of de aanroeper de aangeduide zoekvraag mag uitvoeren
    """
    def test_zoekvraag_authorisation(self, hc_ams_request, hc_api_request, token, expected_response):
        assert is_zoekvraag_authorised(hc_ams_request, token)

    """
    Test of de aanroeper voldoet aan de scope waar ie recht op heeft: landelijk of amsterdam
    """
    def test_amsterdam_landelijk_validation(self, hc_ams_request, hc_api_request, token, expected_response):
        request_result = transform_request_amsterdam_landelijk(hc_ams_request, token)
        if is_amsterdam_authorised(token):
            assert has_amsterdam_query_parameter(request_result)
        if is_landelijk_authorised(token):
            assert not (has_gemeente_van_inschrijving_query_parameter(request_result))

    """
    Test of de aanroeper de query parameter 'inclusiefOverledenPersonen' mag toepassen of niet
    """
    def test_inclusief_overledenen_validation(self, hc_ams_request, hc_api_request, token, expected_response):
        request_result = transform_request_amsterdam_landelijk(hc_ams_request, token)
        if has_inclusief_overledenen_query_parameter(request_result):
            assert is_inclusief_overledenen_authorised(token)

    """
    Test of de filters goed worden gezet in het HC request op basis van de verleende data scopes 
    """
    def test_request_filters(self, hc_ams_request, hc_api_request, token, expected_response):
        request_result = transform_request(hc_ams_request, token)
        request_result = make_fields_uniform(request_result)
        hc_api_request = make_fields_uniform(hc_api_request)
        assert request_result == hc_api_request

    def test_request_real_endpoint(self, hc_ams_request, hc_api_request, token, expected_response):
        endpoint = BrpRequest()
        request_result = transform_request(hc_ams_request, token)
        real_response = endpoint.request(request_result)
        assert real_response.status_code == 200
        assert (json.dumps(real_response.json(), indent=4, sort_keys=True)
                == json.dumps(expected_response, indent=4, sort_keys=True))
