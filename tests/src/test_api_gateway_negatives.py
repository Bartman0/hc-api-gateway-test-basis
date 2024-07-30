import pytest

from base_test_data import (
    make_fields_uniform,
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
    TOKEN_USER_geen_brp_bevragen, TOKEN_USER_geen_landelijk_permissie,
)


class TestNegatives:
    """
    Test of de aanroeper zonder permissie voor Bevragen wordt afgekeurd
    """
    def test_bevragen_authorisation(self):
        hc_ams_request = {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": "Verhuis*",
                "geboortedatum": "2002-07-01",
                "inclusiefOverledenPersonen": True,
            }
        assert not has_bevragen_authorisation(hc_ams_request, TOKEN_USER_geen_brp_bevragen)

    def test_zoekvraag_authorisation(self):
        hc_ams_request_geslachtsnaam = {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": "Verhuis*",
                "geboortedatum": "2002-07-01",
                "inclusiefOverledenPersonen": True,
            }
        assert not is_zoekvraag_authorised(hc_ams_request_geslachtsnaam, TOKEN_USER_B)
        assert not is_zoekvraag_authorised(hc_ams_request_geslachtsnaam, TOKEN_USER_C)

        hc_ams_request_bsn = {
            "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                "gob_brp_raadplegen_bsn"
            ],
            "geslachtsnaam": "Verhuis*",
            "geboortedatum": "2002-07-01",
            "inclusiefOverledenPersonen": True,
        }
        assert not is_zoekvraag_authorised(hc_ams_request_bsn, TOKEN_USER_A)
        assert not is_zoekvraag_authorised(hc_ams_request_bsn, TOKEN_USER_C)


    def test_amsterdam_landelijk_validation(self):
        hc_ams_request = {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": "Verhuis*",
                "geboortedatum": "2002-07-01",
                "inclusiefOverledenPersonen": True,
            }
        request_result = transform_request_amsterdam_landelijk(hc_ams_request, TOKEN_USER_geen_landelijk_permissie)
        if is_amsterdam_authorised(TOKEN_USER_geen_landelijk_permissie):
            assert has_amsterdam_query_parameter(request_result)
            assert has_gemeente_van_inschrijving_query_parameter(hc_ams_request)
            assert not is_landelijk_authorised(TOKEN_USER_geen_landelijk_permissie)

    def test_inclusief_overledenen_validation(self):
        hc_ams_request = {
                "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": "Verhuis*",
                "geboortedatum": "2002-07-01",
                "inclusiefOverledenPersonen": True,
            }
        token = TOKEN_USER_B
        request_result = transform_request_amsterdam_landelijk(hc_ams_request, token)
        if has_inclusief_overledenen_query_parameter(request_result):
            assert not is_inclusief_overledenen_authorised(token)

    """
    Test of de filters goed worden gezet in het HC request op basis van de verleende data scopes 
    """
    def test_request_filters(self):
        hc_ams_request = {
            "type": FUNCTIONALITY_ZOEKVRAGEN["from_name"][
                "gob_brp_raadplegen_bsn"
            ],
            "gob_brp_raadplegen_bsn": "1234567",
        }
        token = TOKEN_USER_A
        request_result = transform_request_filters(hc_ams_request, token)
        assert "kinderen" not in request_result["fields"]
        assert "adressering" not in request_result["fields"]
        for field in request_result["fields"]:
            assert "kinderen" not in field
            assert "addressering" not in field