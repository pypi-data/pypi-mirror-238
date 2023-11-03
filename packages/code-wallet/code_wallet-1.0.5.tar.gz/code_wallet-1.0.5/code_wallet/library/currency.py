from enum import Enum
from code_wallet.library.errors import ErrInvalidCurrency

# Represents a currency code.
class CurrencyCode(Enum):
    KIN = "kin"
    AED = "aed"
    AFN = "afn"
    ALL = "all"
    AMD = "amd"
    ANG = "ang"
    AOA = "aoa"
    ARS = "ars"
    AUD = "aud"
    AWG = "awg"
    AZN = "azn"
    BAM = "bam"
    BBD = "bbd"
    BDT = "bdt"
    BGN = "bgn"
    BHD = "bhd"
    BIF = "bif"
    BMD = "bmd"
    BND = "bnd"
    BOB = "bob"
    BRL = "brl"
    BSD = "bsd"
    BTN = "btn"
    BWP = "bwp"
    BYN = "byn"
    BZD = "bzd"
    CAD = "cad"
    CDF = "cdf"
    CHF = "chf"
    CLP = "clp"
    CNY = "cny"
    COP = "cop"
    CRC = "crc"
    CUP = "cup"
    CVE = "cve"
    CZK = "czk"
    DJF = "djf"
    DKK = "dkk"
    DOP = "dop"
    DZD = "dzd"
    EGP = "egp"
    ERN = "ern"
    ETB = "etb"
    EUR = "eur"
    FJD = "fjd"
    FKP = "fkp"
    GBP = "gbp"
    GEL = "gel"
    GHS = "ghs"
    GIP = "gip"
    GMD = "gmd"
    GNF = "gnf"
    GTQ = "gtq"
    GYD = "gyd"
    HKD = "hkd"
    HNL = "hnl"
    HRK = "hrk"
    HTG = "htg"
    HUF = "huf"
    IDR = "idr"
    ILS = "ils"
    INR = "inr"
    IQD = "iqd"
    IRR = "irr"
    ISK = "isk"
    JMD = "jmd"
    JOD = "jod"
    JPY = "jpy"
    KES = "kes"
    KGS = "kgs"
    KHR = "khr"
    KMF = "kmf"
    KPW = "kpw"
    KRW = "krw"
    KWD = "kwd"
    KYD = "kyd"
    KZT = "kzt"
    LAK = "lak"
    LBP = "lbp"
    LKR = "lkr"
    LRD = "lrd"
    LYD = "lyd"
    MAD = "mad"
    MDL = "mdl"
    MGA = "mga"
    MKD = "mkd"
    MMK = "mmk"
    MNT = "mnt"
    MOP = "mop"
    MRU = "mru"
    MUR = "mur"
    MVR = "mvr"
    MWK = "mwk"
    MXN = "mxn"
    MYR = "myr"
    MZN = "mzn"
    NAD = "nad"
    NGN = "ngn"
    NIO = "nio"
    NOK = "nok"
    NPR = "npr"
    NZD = "nzd"
    OMR = "omr"
    PAB = "pab"
    PEN = "pen"
    PGK = "pgk"
    PHP = "php"
    PKR = "pkr"
    PLN = "pln"
    PYG = "pyg"
    QAR = "qar"
    RON = "ron"
    RSD = "rsd"
    RUB = "rub"
    RWF = "rwf"
    SAR = "sar"
    SBD = "sbd"
    SCR = "scr"
    SDG = "sdg"
    SEK = "sek"
    SGD = "sgd"
    SHP = "shp"
    SLL = "sll"
    SOS = "sos"
    SRD = "srd"
    SSP = "ssp"
    STN = "stn"
    SYP = "syp"
    SZL = "szl"
    THB = "thb"
    TJS = "tjs"
    TMT = "tmt"
    TND = "tnd"
    TOP = "top"
    TRY = "try"
    TTD = "ttd"
    TWD = "twd"
    TZS = "tzs"
    UAH = "uah"
    UGX = "ugx"
    USD = "usd"
    UYU = "uyu"
    UZS = "uzs"
    VES = "ves"
    VND = "vnd"
    VUV = "vuv"
    WST = "wst"
    XAF = "xaf"
    XCD = "xcd"
    XOF = "xof"
    XPF = "xpf"
    YER = "yer"
    ZAR = "zar"
    ZMW = "zmw"

# Index of currency codes in the lookup table.
lookup_table = [code.value for code in CurrencyCode]


def currency_code_to_index(currency: str) -> int:
    """
    Converts a currency code to its index in the lookup table.
    """
    if currency not in lookup_table:
        raise ErrInvalidCurrency()

    return lookup_table.index(currency)


def index_to_currency_code(index: int) -> str:
    """
    Converts an index in the lookup table to a currency code.
    """
    if index < 0 or index >= len(lookup_table):
        raise ErrInvalidCurrency()

    return lookup_table[index]


def is_valid_currency(currency: str) -> bool:
    """
    Checks if the given currency code is valid.
    """
    return currency in lookup_table


def currency_code_to_region(currency: str) -> str:
    """
    Converts a currency code to its region code. This is useful for displaying
    the currency code flag and formatting the currency number based on the
    region.
    """
    region_mapping = {
        'usd': 'us',
        'eur': 'eu',
        'chf': 'ch',
        'nzd': 'nz',
        'xcd': 'ag',
        'zar': 'za',
        'dkk': 'dk',
        'gbp': 'gb',
        'ang': 'cw',
        'xpf': 'pf',
        'mad': 'ma',
        'xaf': 'il',
        'aud': 'au',
        'nok': 'no',
        'ils': 'il',
        'xof': 'il',
        'bdt': 'bd',
        'gtq': 'gt',
        'gyd': 'gy',
        'afn': 'af',
        'kyd': 'ky',
        'bbd': 'bb',
        'kes': 'ke',
        'mvr': 'mv',
        'egp': 'eg',
        'crc': 'cr',
        'hrk': 'hr',
        'sgd': 'sg',
        'brl': 'br',
        'kgs': 'kg',
        'ssp': 'ss',
        'btn': 'bt',
        'pkr': 'pk',
        'mmk': 'mm',
        'mru': 'mr',
        'uzs': 'uz',
        'stn': 'st',
        'lyd': 'ly',
        'mzn': 'mz',
        'sll': 'sl',
        'tjs': 'tj',
        'hkd': 'hk',
        'shp': 'sh',
        'mxn': 'mx',
        'wst': 'ws',
        'bob': 'bo',
        'idr': 'id',
        'cdf': 'cd',
        'bsd': 'bs',
        'bmd': 'bm',
        'huf': 'hu',
        'azn': 'az',
        'pab': 'pa',
        'kzt': 'kz',
        'cop': 'co',
        'rub': 'ru',
        'qar': 'qa',
        'cup': 'cu',
        'amd': 'am',
        'top': 'to',
        'sar': 'sa',
        'kpw': 'kp',
        'nio': 'ni',
        'aoa': 'ao',
        'isk': 'is',
        'mnt': 'mn',
        'mga': 'mg',
        'thb': 'th',
        'byn': 'by',
        'bwp': 'bw',
        'rsd': 'rs',
        'clp': 'cl',
        'gmd': 'gm',
        'aed': 'ae',
        'tzs': 'tz',
        'all': 'al',
        'khr': 'kh',
        'irr': 'ir',
        'etb': 'et',
        'php': 'ph',
        'mdl': 'md',
        'sbd': 'sb',
        'sdg': 'sd',
        'vuv': 'vu',
        'mkd': 'mk',
        'htg': 'ht',
        'srd': 'sr',
        'bzd': 'bz',
        'bif': 'bi',
        'myr': 'my',
        'pen': 'pe',
        'bhd': 'bh',
        'ron': 'ro',
        'uah': 'ua',
        'pyg': 'py',
        'ttd': 'tt',
        'cad': 'ca',
        'scr': 'sc',
        'try': 'tr',
        'ves': 've',
        'fkp': 'fk',
        'hnl': 'hn',
        'gnf': 'gn',
        'ngn': 'ng',
        'mwk': 'mw',
        'ern': 'er',
        'szl': 'sz',
        'bgn': 'bg',
        'mop': 'mo',
        'sek': 'se',
        'bnd': 'bn',
        'fjd': 'fj',
        'kwd': 'kw',
        'czk': 'cz',
        'twd': 'tw',
        'dop': 'do',
        'djf': 'dj',
        'jpy': 'jp',
        'omr': 'om',
        'lrd': 'lr',
        'kmf': 'km',
        'mur': 'mu',
        'jmd': 'jm',
        'tnd': 'tn',
        'lbp': 'lb',
        'tmt': 'tm',
        'jod': 'jo',
        'lkr': 'lk',
        'ugx': 'ug',
        'sos': 'so',
        'nad': 'na',
        'pln': 'pl',
        'awg': 'aw',
        'rwf': 'rw',
        'lak': 'la',
        'dzd': 'dz',
        'yer': 'ye',
        'syp': 'sy',
        'uyu': 'uy',
        'cny': 'cn',
        'krw': 'kr',
        'ars': 'ar',
        'ghs': 'gh',
        'npr': 'np',
        'inr': 'in',
        'iqd': 'iq',
        'bam': 'ba',
        'cve': 'cv',
        'gel': 'ge',
        'zmw': 'zm',
        'gip': 'gi',
        'vnd': 'vn',
        'pgk': 'pg',
    }

    return region_mapping.get(currency)