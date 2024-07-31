from copy import deepcopy
from base_token import TOKEN

GEMEENTE_AMSTERDAM_CODE = "0363"

PARAMETER_GEMEENTE_VAN_INSCHRIJVING = "gemeenteVanInschrijving"
PARAMETER_INCLUSIEF_OVERLEDENEN = "inclusiefOverledenPersonen"

PERMISSION_SCOPE_AMSTERDAM = "gob_brp_algemeen_amsterdam"
PERMISSION_SCOPE_LANDELIJK = "gob_brp_algemeen_landelijk"
PERMISSION_SCOPE_INCLUSIEF_OVERLEDENEN = "gob_brp_indicator_inclusief_overledenen"


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
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_bevragen"],
    ]


# profiel B: scope_B, gob_brp_raadplegen_bsn, gob_brp_algemeen_amsterdam
def profile_B():
    return [
        SCOPE_GROUPS["from_name"]["scope_B"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_raadplegen_bsn"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_amsterdam"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_bevragen"],
    ]


# profiel C: scope_B, scope_C, gob_brp_raadplegen_postcode_huisnummer, gb_brp_algemeen_landelijk
def profile_C():
    return [
        SCOPE_GROUPS["from_name"]["scope_C"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_raadplegen_postcode_huisnummer"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_landelijk"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_bevragen"],
    ]


def profile_geen_brp_bevragen():
    return [
        SCOPE_GROUPS["from_name"]["scope_B"],
        SCOPE_GROUPS["from_name"]["scope_C"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_raadplegen_postcode_huisnummer"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_amsterdam"],
    ]


def profile_geen_landelijk_permissie():
    return [
        SCOPE_GROUPS["from_name"]["scope_B"],
        SCOPE_GROUPS["from_name"]["scope_C"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_raadplegen_postcode_huisnummer"],
        FUNCTIONALITY_GROUPS["from_name"]["gob_brp_algemeen_amsterdam"],
    ]


def profile(name):
    if name == "A":
        return profile_A()
    if name == "B":
        return profile_B()
    if name == "C":
        return profile_C()
    if name == "geen_brp_bevragen":
        return profile_geen_brp_bevragen()
    if name == "geen_landelijk_permissie":
        return profile_geen_landelijk_permissie()
    raise ValueError("unknown user specified for a profile")


def token_user(name):
    token = deepcopy(TOKEN)
    token["groups"].extend(profile(name))
    token["name"] = f"{name}, User"
    token["family_name"] = f"{name}"
    token["unique_name"] = f"user.{name}"
    token["upn"] = f"user.{name}@amsterdam.nl"
    return token


TOKEN_USER_A = token_user("A")
TOKEN_USER_B = token_user("B")
TOKEN_USER_C = token_user("C")
TOKEN_USER_geen_brp_bevragen = token_user("geen_brp_bevragen")
TOKEN_USER_geen_landelijk_permissie = token_user("geen_landelijk_permissie")


def fields_persoon_basis():
    return ["burgerservicenummer", "geboorte", "leeftijd"]


FIELDS_PERSOON_BASIS = fields_persoon_basis()


def fields_kinderen():
    return ["burgerservicenummer", "kinderen"]


FIELDS_KINDEREN = fields_kinderen()


def fields_naam():
    return ["burgerservicenummer", "naam"]


FIELDS_NAAM = fields_naam()


def scope_fields():
    scope_to_fields = {
        "scope_A": list(set(FIELDS_PERSOON_BASIS)),
        "scope_B": list(set(FIELDS_PERSOON_BASIS + FIELDS_KINDEREN)),
        "scope_C": list(set(FIELDS_PERSOON_BASIS + FIELDS_NAAM)),
    }
    return {"from_name": scope_to_fields}


SCOPE_FIELDS = scope_fields()


def has_bevragen_authorisation(hc_ams_request, token):
    return FUNCTIONALITY_GROUPS["from_name"]["gob_brp_bevragen"] in token["groups"]


def is_zoekvraag_authorised(hc_ams_request, token):
    zoekvraag = hc_ams_request["type"]
    return (
        FUNCTIONALITY_GROUPS["from_name"][
            FUNCTIONALITY_ZOEKVRAGEN["from_id"][zoekvraag]
        ]
        in token["groups"]
    )


def is_amsterdam_authorised(token):
    return (
        FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_AMSTERDAM] in token["groups"]
    )


def is_landelijk_authorised(token):
    return (
        FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_LANDELIJK] in token["groups"]
    )


def has_amsterdam_query_parameter(hc_api_request):
    return (
            PARAMETER_GEMEENTE_VAN_INSCHRIJVING in hc_api_request
            and hc_api_request[PARAMETER_GEMEENTE_VAN_INSCHRIJVING]
            == GEMEENTE_AMSTERDAM_CODE
    )


def has_gemeente_van_inschrijving_query_parameter(hc_api_request):
    return PARAMETER_GEMEENTE_VAN_INSCHRIJVING in hc_api_request


def is_inclusief_overledenen_authorised(token):
    return (
        FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_INCLUSIEF_OVERLEDENEN]
        in token["groups"]
    )


def has_inclusief_overledenen_query_parameter(hc_api_request):
    return PARAMETER_INCLUSIEF_OVERLEDENEN in hc_api_request


def transform_request_amsterdam_landelijk(hc_ams_request, jwt_token):
    if (
        FUNCTIONALITY_GROUPS["from_name"][PERMISSION_SCOPE_AMSTERDAM]
        in jwt_token["groups"]
    ):
        hc_ams_request[PARAMETER_GEMEENTE_VAN_INSCHRIJVING] = GEMEENTE_AMSTERDAM_CODE
    return hc_ams_request


def transform_request(hc_ams_request, jwt_token):
    hc_ams_request = transform_request_amsterdam_landelijk(hc_ams_request, jwt_token)
    fields = []
    for scope, group_id in SCOPE_GROUPS["from_name"].items():
        if group_id in jwt_token["groups"]:
            fields.extend(SCOPE_FIELDS["from_name"][scope])
    hc_ams_request["fields"] = list(set(fields))
    return hc_ams_request


def make_fields_uniform(request):
    request["fields"] = sorted(request["fields"])
