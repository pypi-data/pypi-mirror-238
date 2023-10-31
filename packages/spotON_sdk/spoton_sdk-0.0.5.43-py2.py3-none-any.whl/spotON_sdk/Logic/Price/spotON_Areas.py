from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel


class Currency_unit(BaseModel):
    name: str
    symbol: str 

class Currency(BaseModel):
    majorUnit: Currency_unit
    minorUnit: Currency_unit
    iso_code_4217: str 

class Currencies:
    euro = Currency(
        majorUnit=Currency_unit(name="Euro", symbol="€"),
        minorUnit=Currency_unit(name="cent", symbol="cent"),
        iso_code_4217 = "EUR"
    )


    bulgarian_lev = Currency(
        majorUnit=Currency_unit(name="Bulgarian Lev", symbol="лв"),
        minorUnit=Currency_unit(name="stotinki", symbol="st."),
        iso_code_4217="BGN"
    )

    croatian_kuna = Currency(
        majorUnit=Currency_unit(name="Croatian Kuna", symbol="kn"),
        minorUnit=Currency_unit(name="lipa", symbol="lp"),
        iso_code_4217="HRK"
    )

    czech_koruna = Currency(
        majorUnit=Currency_unit(name="Czech Koruna", symbol="Kč"),
        minorUnit=Currency_unit(name="haléř", symbol="h"),
        iso_code_4217="CZK"
    )

    danish_krone = Currency(
        majorUnit=Currency_unit(name="Danish Krone", symbol="kr"),
        minorUnit=Currency_unit(name="øre", symbol="øre"),
        iso_code_4217="DKK"
    )

    hungarian_forint = Currency(
        majorUnit=Currency_unit(name="Hungarian Forint", symbol="Ft"),
        minorUnit=Currency_unit(name="fillér", symbol="f"),
        iso_code_4217="HUF"
    )


    polish_zloty = Currency(
        majorUnit=Currency_unit(name="Polish Złoty", symbol="zł"),
        minorUnit=Currency_unit(name="grosz", symbol="gr"),
        iso_code_4217="PLN"
    )


    romanian_leu = Currency(
        majorUnit=Currency_unit(name="Romanian Leu", symbol="lei"),
        minorUnit=Currency_unit(name="bani", symbol="b"),
        iso_code_4217="RON"
    )


    swedish_krona = Currency(
        majorUnit=Currency_unit(name="Swedish Krona", symbol="kr"),
        minorUnit=Currency_unit(name="öre", symbol="öre"),
        iso_code_4217="SEK"
    )

class Area_details(BaseModel):
    name: str
    code: str
    tz: str
    currency: Currency = Currencies.euro


class spotON_Area(Enum):
    AL = Area_details(name='AL',code='10YAL-KESH-----5',tz='Europe/Tirane',)
    AT = Area_details(name='AT',code='10YAT-APG------L',tz='Europe/Vienna',currency=Currencies.euro)
    BA = Area_details(name='BA',code='10YBA-JPCC-----D',tz='Europe/Sarajevo')
    BE = Area_details(name='BE',code='10YBE----------2',tz='Europe/Brussels')
    BG = Area_details(name='BG',code='10YCA-BULGARIA-R',tz='Europe/Sofia',currency=Currencies.bulgarian_lev)
    BY = Area_details(name='BY',code='10Y1001A1001A51S',tz='Europe/Minsk')
    CH = Area_details(name='CH',code='10YCH-SWISSGRIDZ',tz='Europe/Zurich')
    CWE = Area_details(name='CWE',code='10YDOM-REGION-1V',tz='Europe/Brussels')
    CY = Area_details(name='CY',code='10YCY-1001A0003J',tz='Asia/Nicosia')
    CZ = Area_details(name='CZ',code='10YCZ-CEPS-----N',tz='Europe/Prague',currency=Currencies.czech_koruna)
    CZ_DE_SK = Area_details(name='CZ_DE_SK',code='10YDOM-CZ-DE-SKK',tz='Europe/Prague',currency=Currencies.czech_koruna)
    DE = Area_details(name='DE',code='10Y1001A1001A83F',tz='Europe/Berlin')
    DE_50HZ = Area_details(name='DE_50HZ',code='10YDE-VE-------2',tz='Europe/Berlin')
    DE_AMPRION = Area_details(name='DE_AMPRION',code='10YDE-RWENET---I',tz='Europe/Berlin')
    DE_AT_LU = Area_details(name='DE_AT_LU',code='10Y1001A1001A63L',tz='Europe/Berlin')
    DE_LU = Area_details(name='DE_LU',code='10Y1001A1001A82H',tz='Europe/Berlin')
    DE_TENNET = Area_details(name='DE_TENNET',code='10YDE-EON------1',tz='Europe/Berlin')
    DE_TRANSNET = Area_details(name='DE_TRANSNET',code='10YDE-ENBW-----N',tz='Europe/Berlin')
    DK = Area_details(name='DK',code='10Y1001A1001A65H',tz='Europe/Copenhagen',currency=Currencies.danish_krone)
    DK_1 = Area_details(name='DK_1',code='10YDK-1--------W',tz='Europe/Copenhagen',currency=Currencies.danish_krone)
    DK_1_NO_1 = Area_details(name='DK_1_NO_1',code='46Y000000000007M',tz='Europe/Copenhagen',currency=Currencies.danish_krone)
    DK_2 = Area_details(name='DK_2',code='10YDK-2--------M',tz='Europe/Copenhagen',currency=Currencies.danish_krone)
    DK_CA = Area_details(name='DK_CA',code='10Y1001A1001A796',tz='Europe/Copenhagen',currency=Currencies.danish_krone)
    EE = Area_details(name='EE',code='10Y1001A1001A39I',tz='Europe/Tallinn')
    ES = Area_details(name='ES',code='10YES-REE------0',tz='Europe/Madrid')
    FI = Area_details(name='FI',code='10YFI-1--------U',tz='Europe/Helsinki')
    FR = Area_details(name='FR',code='10YFR-RTE------C',tz='Europe/Paris')
    GB = Area_details(name='GB',code='10YGB----------A',tz='Europe/London')
    GB_ELECLINK = Area_details(name='GB_ELECLINK',code='11Y0-0000-0265-K',tz='Europe/London')
    GB_IFA = Area_details(name='GB_IFA',code='10Y1001C--00098F',tz='Europe/London')
    GB_IFA2 = Area_details(name='GB_IFA2',code='17Y0000009369493',tz='Europe/London')
    GB_NIR = Area_details(name='GB_NIR',code='10Y1001A1001A016',tz='Europe/Belfast')
    GR = Area_details(name='GR',code='10YGR-HTSO-----Y',tz='Europe/Athens')
    HR = Area_details(name='HR',code='10YHR-HEP------M',tz='Europe/Zagreb',currency=Currencies.croatian_kuna)
    HU = Area_details(name='HU',code='10YHU-MAVIR----U',tz='Europe/Budapest',currency=Currencies.hungarian_forint)
    IE = Area_details(name='IE',code='10YIE-1001A00010',tz='Europe/Dublin')
    IE_SEM = Area_details(name='IE_SEM',code='10Y1001A1001A59C',tz='Europe/Dublin')
    IS = Area_details(name='IS',code='IS',tz='Atlantic/Reykjavik')
    IT = Area_details(name='IT',code='10YIT-GRTN-----B',tz='Europe/Rome')
    IT_BRNN = Area_details(name='IT_BRNN',code='10Y1001A1001A699',tz='Europe/Rome')
    IT_CALA = Area_details(name='IT_CALA',code='10Y1001C--00096J',tz='Europe/Rome')
    IT_CNOR = Area_details(name='IT_CNOR',code='10Y1001A1001A70O',tz='Europe/Rome')
    IT_CSUD = Area_details(name='IT_CSUD',code='10Y1001A1001A71M',tz='Europe/Rome')
    IT_FOGN = Area_details(name='IT_FOGN',code='10Y1001A1001A72K',tz='Europe/Rome')
    IT_GR = Area_details(name='IT_GR',code='10Y1001A1001A66F',tz='Europe/Rome')
    IT_MACRO_NORTH = Area_details(name='IT_MACRO_NORTH',code='10Y1001A1001A84D',tz='Europe/Rome')
    IT_MACRO_SOUTH = Area_details(name='IT_MACRO_SOUTH',code='10Y1001A1001A85B',tz='Europe/Rome')
    IT_MALTA = Area_details(name='IT_MALTA',code='10Y1001A1001A877',tz='Europe/Rome')
    IT_NORD = Area_details(name='IT_NORD',code='10Y1001A1001A73I',tz='Europe/Rome')
    IT_NORD_AT = Area_details(name='IT_NORD_AT',code='10Y1001A1001A80L',tz='Europe/Rome')
    IT_NORD_CH = Area_details(name='IT_NORD_CH',code='10Y1001A1001A68B',tz='Europe/Rome')
    IT_NORD_FR = Area_details(name='IT_NORD_FR',code='10Y1001A1001A81J',tz='Europe/Rome')
    IT_NORD_SI = Area_details(name='IT_NORD_SI',code='10Y1001A1001A67D',tz='Europe/Rome')
    IT_PRGP = Area_details(name='IT_PRGP',code='10Y1001A1001A76C',tz='Europe/Rome')
    IT_ROSN = Area_details(name='IT_ROSN',code='10Y1001A1001A77A',tz='Europe/Rome')
    IT_SACO_AC = Area_details(name='IT_SACO_AC',code='10Y1001A1001A885',tz='Europe/Rome')
    IT_SACO_DC = Area_details(name='IT_SACO_DC',code='10Y1001A1001A893',tz='Europe/Rome')
    IT_SARD = Area_details(name='IT_SARD',code='10Y1001A1001A74G',tz='Europe/Rome')
    IT_SICI = Area_details(name='IT_SICI',code='10Y1001A1001A75E',tz='Europe/Rome')
    IT_SUD = Area_details(name='IT_SUD',code='10Y1001A1001A788',tz='Europe/Rome')
    LT = Area_details(name='LT',code='10YLT-1001A0008Q',tz='Europe/Vilnius')
    LU = Area_details(name='LU',code='10YLU-CEGEDEL-NQ',tz='Europe/Luxembourg')
    LV = Area_details(name='LV',code='10YLV-1001A00074',tz='Europe/Riga')
    MD = Area_details(name='MD',code='10Y1001A1001A990',tz='Europe/Chisinau')
    ME = Area_details(name='ME',code='10YCS-CG-TSO---S',tz='Europe/Podgorica')
    MK = Area_details(name='MK',code='10YMK-MEPSO----8',tz='Europe/Skopje')
    MT = Area_details(name='MT',code='10Y1001A1001A93C',tz='Europe/Malta')
    NL = Area_details(name='NL',code='10YNL----------L',tz='Europe/Amsterdam')
    NO = Area_details(name='NO',code='10YNO-0--------C',tz='Europe/Oslo')
    NO_1 = Area_details(name='NO_1',code='10YNO-1--------2',tz='Europe/Oslo')
    NO_1A = Area_details(name='NO_1A',code='10Y1001A1001A64J',tz='Europe/Oslo')
    NO_2 = Area_details(name='NO_2',code='10YNO-2--------T',tz='Europe/Oslo')
    NO_2A = Area_details(name='NO_2A',code='10Y1001C--001219',tz='Europe/Oslo')
    NO_2_NSL = Area_details(name='NO_2_NSL',code='50Y0JVU59B4JWQCU',tz='Europe/Oslo')
    NO_3 = Area_details(name='NO_3',code='10YNO-3--------J',tz='Europe/Oslo')
    NO_4 = Area_details(name='NO_4',code='10YNO-4--------9',tz='Europe/Oslo')
    NO_5 = Area_details(name='NO_5',code='10Y1001A1001A48H',tz='Europe/Oslo')
    PL = Area_details(name='PL',code='10YPL-AREA-----S',tz='Europe/Warsaw',currency=Currencies.polish_zloty)
    PL_CZ = Area_details(name='PL_CZ',code='10YDOM-1001A082L',tz='Europe/Warsaw',currency=Currencies.polish_zloty)
    PT = Area_details(name='PT',code='10YPT-REN------W',tz='Europe/Lisbon')
    RO = Area_details(name='RO',code='10YRO-TEL------P',tz='Europe/Bucharest',currency=Currencies.romanian_leu)
    RS = Area_details(name='RS',code='10YCS-SERBIATSOV',tz='Europe/Belgrade')
    RU = Area_details(name='RU',code='10Y1001A1001A49F',tz='Europe/Moscow')
    RU_KGD = Area_details(name='RU_KGD',code='10Y1001A1001A50U',tz='Europe/Kaliningrad')
    SE = Area_details(name='SE',code='10YSE-1--------K',tz='Europe/Stockholm',currency=Currencies.swedish_krona)
    SE_1 = Area_details(name='SE_1',code='10Y1001A1001A44P',tz='Europe/Stockholm',currency=Currencies.swedish_krona)
    SE_2 = Area_details(name='SE_2',code='10Y1001A1001A45N',tz='Europe/Stockholm',currency=Currencies.swedish_krona)
    SE_3 = Area_details(name='SE_3',code='10Y1001A1001A46L',tz='Europe/Stockholm',currency=Currencies.swedish_krona)
    SE_4 = Area_details(name='SE_4',code='10Y1001A1001A47J',tz='Europe/Stockholm',currency=Currencies.swedish_krona)
    SI = Area_details(name='SI',code='10YSI-ELES-----O',tz='Europe/Ljubljana')
    SK = Area_details(name='SK',code='10YSK-SEPS-----K',tz='Europe/Bratislava')
    TR = Area_details(name='TR',code='10YTR-TEIAS----W',tz='Europe/Istanbul')
    UA = Area_details(name='UA',code='10Y1001C--00003F',tz='Europe/Kiev')
    UA_BEI = Area_details(name='UA_BEI',code='10YUA-WEPS-----0',tz='Europe/Kiev')
    UA_DOBTPP = Area_details(name='UA_DOBTPP',code='10Y1001A1001A869',tz='Europe/Kiev')
    UA_IPS = Area_details(name='UA_IPS',code='10Y1001C--000182',tz='Europe/Kiev')
    UK = Area_details(name='UK',code='10Y1001A1001A92E',tz='Europe/London')
    XK = Area_details(name='XK',code='10Y1001C--00100H',tz='Europe/Rome')
