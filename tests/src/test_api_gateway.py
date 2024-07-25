import pytest

from base_token import TOKEN
from functions import transform_to_hc_api_request


def scope_groups():
    scope_to_id = {
        "scope_A": "54321-A",
        "scope_B": "54321-B",
        "scope_C": "54321-C",
    }
    id_to_scope = {v: k for k, v in scope_to_id.items()}
    return {"from_scope": scope_to_id, "from_id": id_to_scope}


def functionality_groups():
    name_to_group_id = {
        "gob_brp_algemeen": "12345-001",
        "gob_brp_algemeen_amsterdam": "12345-002",
        "gob_brp_algemeen_landelijk": "12345-003",
        "gob_brp_raadplegen": "12345-004",
        "gob_brp_bevragen": "12345-005",
        "gob_brp_kennisgevingen": "12345-006",
        "gob_brp_raadplegen_bsn": "12345-007",
        "gob_brp_raadplegen_geslachtsnaam_geboortedatum": "12345-008",
        "gob_brp_raadplegen_geslachtsnaam_gemeente": "12345-009",
        "gob_brp_raadplegen_postcode_huisnummer": "12345-00a",
        "gob_brp_raadplegen_straat_gemeente": "12345-00b",
        "gob_brp_raadplegen_nummer_identificatie": "12345-00c",
        "gob_brp_raadplegen_adresseerbaarobject": "12345-00d",
        "gob_brp_indicator_inclusief_overledenen": "12345-00e",
    }
    group_id_to_name = {v: k for k, v in name_to_group_id.items()}
    return {"from_name": name_to_group_id, "from_id": group_id_to_name}


def functionality_zoekvragen():
    functionality_to_zoekvraag = {
        "gob_brp_raadplegen_bsn": "RaadpleegMetBurgerservicenummer",
        "gob_brp_raadplegen_geslachtsnaam_geboortedatum": "ZoekMetGeslachtsnaamEnGeboortedatum",
        "gob_brp_raadplegen_postcode_huisnummer": "ZoekMetPostcodeEnHuisnummer",
    }
    zoekvraag_to_functionality = {v: k for k, v in functionality_to_zoekvraag.items()}
    return {
        "from_functionality": functionality_to_zoekvraag,
        "from_zoekvraag": zoekvraag_to_functionality,
    }


# profiel A: scope_A, scope_C, gob_brp_raadplegen_geslachtsnaam_geboortedatum, gob_brp_indicator_inclusief_overledenen, gob_brp_algemeen_amsterdam
def profile_A():
    return [
        scope_groups()["from_scope"]["scope_A"],
        scope_groups()["from_scope"]["scope_C"],
        functionality_groups()["from_name"][
            "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
        ],
        functionality_groups()["from_name"]["gob_brp_indicator_inclusief_overledenen"],
        functionality_groups()["from_name"]["gob_brp_algemeen_amsterdam"],
    ]


# profiel B: scope_A, scope_B, scope_C, scope_D, gob_brp_raadplegen_bsn, gob_brp_algemeen_landelijk
def profile_B():
    return [
        scope_groups()["from_scope"]["scope_A"],
        scope_groups()["from_scope"]["scope_B"],
        scope_groups()["from_scope"]["scope_C"],
        functionality_groups()["from_name"]["gob_brp_raadplegen_bsn"],
        functionality_groups()["from_name"]["gob_brp_algemeen_landelijk"],
    ]


# profiel C: scope_B, scope_C, scope_E, gob_brp_raadplegen_postcode_huisnummer, gb_brp_algemeen_amsterdam
def profile_C():
    return [
        scope_groups()["from_scope"]["scope_B"],
        scope_groups()["from_scope"]["scope_C"],
        functionality_groups()["from_name"]["gob_brp_raadplegen_postcode_huisnummer"],
        functionality_groups()["from_name"]["gob_brp_algemeen_amsterdam"],
    ]


def token_user_A():
    token = TOKEN
    token["groups"].extend(profile_A())
    return token


def token_user_B():
    token = TOKEN
    token["groups"].extend(profile_B())
    return token


def token_user_C():
    token = TOKEN
    token["groups"].extend(profile_C())
    return token


def fields_persoon_basis():
    return ["burgerservicenummer", "geboorte", "naam", "leeftijd"]


def fields_kinderen():
    return ["burgerservicenummer", "kinderen"]


def fields_adres():
    return ["burgerservicenummer", "adressering"]


@pytest.mark.parametrize(
    "hc_ams_request, hc_api_request, token, status_code",
    [
        (
            {
                "type": functionality_zoekvragen()["from_functionality"][
                    "gob_brp_raadplegen_bsn"
                ],
                "burgerservicenummer": ["999993653"],
            },
            {
                "type": "RaadpleegMetBurgerservicenummer",
                "burgerservicenummer": ["999993653"],
                "fields": list(set(fields_persoon_basis() + fields_kinderen())),
            },
            token_user_B(),
            200,
        ),
        (
            {
                "type": functionality_zoekvragen()["from_functionality"][
                    "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
                ],
                "geslachtsnaam": ["999993653"],
                "geboortedatum": ["1985-12-01"],
            },
            {
                "type": "ZoekMetGeslachtsnaamEnGeboortedatum",
                "geslachtsnaam": ["999993653"],
                "geboortedatum": ["1985-12-01"],
                "fields": list(set(fields_persoon_basis())),
            },
            token_user_A(),
            200,
        ),
        (
            {
                "type": functionality_zoekvragen()["from_functionality"][
                    "gob_brp_raadplegen_postcode_huisnummer"
                ],
                "postcode": ["999993653"],
                "huisnummer": ["1985-12-01"],
            },
            {
                "type": "ZoekMetPostcodeEnHuisnummer",
                "postcode": ["999993653"],
                "huisnummer": ["1985-12-01"],
                "fields": list(set(fields_persoon_basis() + fields_adres())),
            },
            token_user_C(),
            200,
        ),
    ],
)
def test_transform_to_hc_api_request(
    hc_ams_request, hc_api_request, token, status_code
):
    assert zoevraag_authorised(hc_ams_request, token)

    request_result = transform_to_hc_api_request(hc_ams_request, token)
    assert request_result == hc_api_request
