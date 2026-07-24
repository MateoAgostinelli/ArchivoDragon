from pipeline.normalize import html_to_clean_markdown, sanitize_html


def test_sanitize_elimina_script():
    dirty = '<p>Hola</p><script>alert("xss")</script>'
    clean = sanitize_html(dirty)
    assert "<script" not in clean
    assert "alert" not in clean


def test_sanitize_elimina_atributos_de_evento():
    dirty = '<img src="x.jpg" onerror="alert(1)">'
    clean = sanitize_html(dirty)
    assert "onerror" not in clean


def test_html_a_markdown_conserva_texto():
    html = "<h2>Título</h2><p>Cuerpo del <b>post</b>.</p>"
    md = html_to_clean_markdown(html)
    assert "Título" in md
    assert "Cuerpo del" in md


def test_html_a_markdown_no_deja_html_crudo():
    dirty = "<p>Texto</p><script>document.cookie</script>"
    md = html_to_clean_markdown(dirty)
    assert "<script" not in md
    assert "document.cookie" not in md
