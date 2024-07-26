from copy import deepcopy
from base_token import TOKEN

GEMEENTE_AMSTERDAM_CODE = "0363"
GEMEENTE_VAN_INSCHRIJVING_PARAMETER = "gemeenteVanInschrijving"
PERMISSION_SCOPE_AMSTERDAM = "gob_brp_algemeen_amsterdam"
PERMISSION_SCOPE_LANDELIJK = "gob_brp_algemeen_landelijk"


def scope_groups():
    scope_to_id = {
        "scope_A": "S-54321-A",
        "scope_B": "S-54321-B",
        "scope_C": "S-54321-C",
    }
    id_to_scope = {v: k for k, v in scope_to_id.items()}
    return {"from_name": scope_to_id, "from_id": id_to_scope}


SCOPE_GROUPS = scope_groups()


def functionality_groups():
    name_to_group_id = {
        "gob_brp_algemeen": "F-12345-001",
        "gob_brp_algemeen_amsterdam": "F-12345-002",
        "gob_brp_algemeen_landelijk": "F-12345-003",
        "gob_brp_raadplegen": "F-12345-004",
        "gob_brp_bevragen": "F-12345-005",
        "gob_brp_kennisgevingen": "F-12345-006",
        "gob_brp_raadplegen_bsn": "F-12345-007",
        "gob_brp_raadplegen_geslachtsnaam_geboortedatum": "F-12345-008",
        "gob_brp_raadplegen_geslachtsnaam_gemeente": "F-12345-009",
        "gob_brp_raadplegen_postcode_huisnummer": "F-12345-00a",
        "gob_brp_raadplegen_straat_gemeente": "F-12345-00b",
        "gob_brp_raadplegen_nummer_identificatie": "F-12345-00c",
        "gob_brp_raadplegen_adresseerbaarobject": "F-12345-00d",
        "gob_brp_indicator_inclusief_overledenen": "F-12345-00e",
    }
    group_id_to_name = {v: k for k, v in name_to_group_id.items()}
    return {"from_name": name_to_group_id, "from_id": group_id_to_name}


FUNCTIONALITY_GROUPS = functionality_groups()


def functionality_zoekvragen():
    functionality_to_zoekvraag = {
        "gob_brp_raadplegen_bsn": "RaadpleegMetBurgerservicenummer",
        "gob_brp_raadplegen_geslachtsnaam_geboortedatum": "ZoekMetGeslachtsnaamEnGeboortedatum",
        "gob_brp_raadplegen_postcode_huisnummer": "ZoekMetPostcodeEnHuisnummer",
    }
    zoekvraag_to_functionality = {v: k for k, v in functionality_to_zoekvraag.items()}
    return {
        "from_name": functionality_to_zoekvraag,
        "from_id": zoekvraag_to_functionality,
    }


FUNCTIONALITY_ZOEKVRAGEN = functionality_zoekvragen()


# profiel A: scope_A, gob_brp_raadplegen_geslachtsnaam_geboortedatum, gob_brp_indicator_inclusief_overledenen, gob_brp_algemeen_amsterdam
def profile_A():
    return [
        SCOPE_GROUPS["from_name"]["scope_A"],
        FUNCTIONALITY_GROUPS["from_name"][
            "gob_brp_raadplegen_geslachtsnaam_geboortedatum"
        ],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_indicator_inclusief_overledenen"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_amsterdam"],
    ]


PROFILE_A = profile_A()


# profiel B: scope_B, gob_brp_raadplegen_bsn, gob_brp_algemeen_landelijk
def profile_B():
    return [
        SCOPE_GROUPS["from_name"]["scope_B"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_raadplegen_bsn"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_amsterdam"],
    ]


PROFILE_B = profile_B()


# profiel C: scope_B, scope_C, gob_brp_raadplegen_postcode_huisnummer, gb_brp_algemeen_amsterdam
def profile_C():
    return [
        SCOPE_GROUPS["from_name"]["scope_B"],
        SCOPE_GROUPS["from_name"]["scope_C"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_raadplegen_postcode_huisnummer"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_landelijk"],
    ]


PROFILE_C = profile_C()


def token_user_A():
    token = deepcopy(TOKEN)
    token["groups"].extend(profile_A())
    token["name"] = "A, User"
    token["family_name"] = "A"
    token["unique_name"] = "user.A"
    token["upn"] = "user.A@amsterdam.nl"
    return token


TOKEN_USER_A = token_user_A()


def token_user_B():
    token = deepcopy(TOKEN)
    token["groups"].extend(profile_B())
    token["name"] = "B, User"
    token["family_name"] = "B"
    token["unique_name"] = "user.B"
    token["upn"] = "user.B@amsterdam.nl"
    return token


TOKEN_USER_B = token_user_B()


def token_user_C():
    token = deepcopy(TOKEN)
    token["groups"].extend(profile_C())
    token["name"] = "C, User"
    token["family_name"] = "C"
    token["unique_name"] = "user.C"
    token["upn"] = "user.C@amsterdam.nl"
    return token


TOKEN_USER_C = token_user_C()


def fields_persoon_basis():
    return ["burgerservicenummer", "geboorte", "naam", "leeftijd"]


FIELDS_PERSOON_BASIS = fields_persoon_basis()


def fields_kinderen():
    return ["burgerservicenummer", "kinderen"]


FIELDS_KINDEREN = fields_kinderen()


def fields_adres():
    return ["burgerservicenummer", "adressering"]


FIELDS_ADRES = fields_adres()


def scope_fields():
    scope_to_fields = {
        "scope_A": list(set(FIELDS_PERSOON_BASIS)),
        "scope_B": list(set(FIELDS_PERSOON_BASIS + FIELDS_KINDEREN)),
        "scope_C": list(set(FIELDS_PERSOON_BASIS + FIELDS_KINDEREN + FIELDS_ADRES)),
    }
    return {"from_name": scope_to_fields}


SCOPE_FIELDS = scope_fields()


def is_zoekvraag_authorised(hc_ams_request, token):
    zoekvraag = hc_ams_request["type"]
    return FUNCTIONALITY_GROUPS["from_name"][FUNCTIONALITY_ZOEKVRAGEN["from_id"][zoekvraag]] in token["groups"]


def is_amsterdam_authorised(token):
    return (
            FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_AMSTERDAM]
            in token["groups"]
    )


def is_landelijk_authorised(token):
    return (
            FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_LANDELIJK]
            in token["groups"]
    )


def has_amsterdam_query_parameter(hc_api_request):
    return (GEMEENTE_VAN_INSCHRIJVING_PARAMETER in hc_api_request and
            hc_api_request[GEMEENTE_VAN_INSCHRIJVING_PARAMETER] == GEMEENTE_AMSTERDAM_CODE)


def transform_request_amsterdam_landelijk(hc_ams_request, jwt_token):
    if FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_AMSTERDAM] in jwt_token["groups"]:
        hc_ams_request[GEMEENTE_VAN_INSCHRIJVING_PARAMETER] = GEMEENTE_AMSTERDAM_CODE
    return hc_ams_request


def transform_request_filters(hc_ams_request, jwt_token):
    hc_ams_request = transform_request_amsterdam_landelijk(hc_ams_request, jwt_token)
    fields = []
    for scope, group_id in SCOPE_GROUPS["from_name"].items():
        if group_id in jwt_token["groups"]:
            fields.extend(SCOPE_FIELDS["from_name"][scope])
    hc_ams_request["fields"] = list(set(fields))
    return hc_ams_request
