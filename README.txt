## Zoekfuncties

1. ZoekMetGeslachtsnaamEnGeboortedatum
2. RaadpleegMetBurgerservicenummer
3. ZoekMetPostcodeEnHuisnummer


## Testcontext

- gebruikersgroep A, deze groep mag gebruik maken van Zoekfunctie 1
- gebruikersgroep B, deze groep mag gebruik maken van Zoekfunctie 2
- gebruikersgroep C, deze groep mag gebruik maken van Zoekfunctie 3
- gebruikersgroep A, deze groep mag gebruik maken van Scope A (bv Persoon basis)
- gebruikersgroep B/C, deze groep mag gebruik maken van Scope B (bv Persoon basis+Kinderen)
- gebruikersgroep C, deze groep mag gebruik maken van Scope C (bv Persoon basis+Adres)
- gebruikersgroep A, deze groep mag inclusief overleden personen gegevens bevragen
- gebruikersgroep B, deze groep mag Amsterdammers bevragen
- gebruikersgroep C, deze groep mag landelijke personen

- profiel A: scope_A, gob_brp_raadplegen_geslachtsnaam_geboortedatum, 
- profiel B: scope_B, gob_brp_raadplegen_bsn
- profiel C: scope_B, scope_C, gob_brp_raadplegen_postcode_huisnummer


## Testcases

- worden de HC API filters goed gedefinieerd voor de verschillende data scopes?
- worden de HC AMS API aanroepen omgezet naar de juiste filters?
- worden de zoekvragen goed gevalideerd voor de gebruikersgroepen?
- wordt de validatie van Amsterdam-ingezetenen goed uitgevoerd?
- wordt de selectie op overledenen goed toegepast?


## Autorisatie profielen
| functie                                                                   | application role                               |
| ------------------------------------------------------------------------- | ---------------------------------------------- |
| Algemeen GOB-BRP (nodig?<br>de volgende twee zou je ook kunnen gebruiken) | gob_brp_algemeen                               |
| GOB-BRP Amsterdam ingezetenen                                             | gob_brp_algemeen_amsterdam                     |
| GOB-BRP landelijke ingezetenen                                            | gob_brp_algemeen_landelijk                     |
| Indicator inclusief overledenen                                           | gob_brp_indicator_inclusief_overledenen        |
| Raadplegen applicatie                                                     | gob_brp_raadplegen                             |
| Bevragen applicatie                                                       | gob_brp_bevragen                               |
| Kennisgevingen applicatie                                                 | gob_brp_kennisgevingen                         |
| Zoekvraag Raadpleeg met burgerservicenummer                               | gob_brp_raadplegen_bsn                         |
| Zoek met geslachtsnaam en geboortedatum                                   | gob_brp_raadplegen_geslachtsnaam_geboortedatum |
| Zoek met geslachtsnaam, voornamen en gemeente van inschrijving            | gob_brp_raadplegen_geslachtsnaam_gemeente      |
| Zoek met postcode en huisnummer                                           | gob_brp_raadplegen_postcode_huisnummer         |
| Zoek met straat, huisnummer en gemeente van inschrijving                  | gob_brp_raadplegen_straat_gemeente             |
| Zoek met nummeraanduiding identificatie                                   | gob_brp_raadplegen_nummer_identificatie        |
| Zoek met adresseerbaarobject identificatie                                | gob_brp_raadplegen_adresseerbaarobject         |

In deze tests gebruiken we fictieve group id's voor deze groepen. In de echte API-gateway moeten deze groups en hun id's bepaald worden bij de start van het component, ofwel vanuit configuratie, ofwel vanuit Entra.

gob_brp_algemeen 12345-001
gob_brp_algemeen_amsterdam 12345-002
gob_brp_algemeen_landelijk 12345-003
gob_brp_raadplegen 12345-004
gob_brp_bevragen 12345-005
gob_brp_kennisgevingen 12345-006
gob_brp_raadplegen_bsn 12345-007
gob_brp_raadplegen_geslachtsnaam_geboortedatum 12345-008
gob_brp_raadplegen_geslachtsnaam_gemeente 12345-009
gob_brp_raadplegen_postcode_huisnummer 12345-00a
gob_brp_raadplegen_straat_gemeente 12345-00b
gob_brp_raadplegen_nummer_identificatie 12345-00c
gob_brp_raadplegen_adresseerbaarobject 12345-00d


## Data scopes
scope_A 54321-A
scope_B 54321-B
scope_C 54321-C
scope_D 54321-D
scope_E 54321-E
scope_A 54321-F


## definitie gemeente Amsterdam

gemeenteVanInschrijving == "0363"

