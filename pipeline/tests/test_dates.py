from pipeline.dates import parse_spanish_date


def test_fecha_exacta_iso():
    result = parse_spanish_date("1994-06-14")
    assert result.date == "1994-06-14"
    assert result.date_precision == "exact"
    assert result.date_display is None


def test_fecha_exacta_prosa():
    result = parse_spanish_date("14 de junio de 1994")
    assert result.date == "1994-06-14"
    assert result.date_precision == "exact"


def test_fecha_aproximada_decada():
    result = parse_spanish_date("c. años 80")
    assert result.date == "1980-01-01"
    assert result.date_precision == "decade"
    assert result.date_display == "c. años 80"


def test_fecha_solo_anio():
    result = parse_spanish_date("en 1994 el club ascendió")
    assert result.date == "1994-01-01"
    assert result.date_precision == "year"


def test_fecha_rota_devuelve_none():
    assert parse_spanish_date("no hay fecha acá") is None


def test_mes_setiembre_variante():
    result = parse_spanish_date("3 de setiembre de 2001")
    assert result.date == "2001-09-03"
