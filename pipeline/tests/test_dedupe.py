from pipeline.dedupe import possible_duplicate, stable_id


def test_id_estable_por_url():
    id1 = stable_id("https://blog.com/post1", "Titulo", "1994-01-01")
    id2 = stable_id("https://blog.com/post1", "Titulo distinto", "2000-01-01")
    assert id1 == id2  # misma url -> mismo id, sin importar el resto


def test_id_distinto_por_url_distinta():
    id1 = stable_id("https://blog.com/post1", "Titulo", "1994-01-01")
    id2 = stable_id("https://blog.com/post2", "Titulo", "1994-01-01")
    assert id1 != id2


def test_dedup_idempotente_recorrer_no_duplica():
    # Simula correr el scraper dos veces sobre la misma fuente.
    first_run = stable_id("https://blog.com/post1", "Nota", "1994-01-01")
    second_run = stable_id("https://blog.com/post1", "Nota", "1994-01-01")
    assert first_run == second_run


def test_flag_similitud_detecta_republicacion():
    existing = [("existing-id-1", "Defensores vuelve a Primera", "1994-06-14")]
    dup = possible_duplicate("Defensores Vuelve a Primera", "1994-06-14", existing)
    assert dup == "existing-id-1"


def test_flag_similitud_no_falso_positivo():
    existing = [("existing-id-1", "Defensores vuelve a Primera", "1994-06-14")]
    dup = possible_duplicate("Un partido totalmente distinto", "2001-01-01", existing)
    assert dup is None
