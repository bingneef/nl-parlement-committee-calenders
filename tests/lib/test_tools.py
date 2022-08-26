from lib.tools import generate_safe_filename, text_from_html_string


def test_generate_safe_file_name():
    """Replaces unsafe chars to dashes"""

    unsafe_str = "a b/c&d,e.f"
    extension = '.png'
    expected = "a-b-c-d-e-f.png"

    assert generate_safe_filename(unsafe_str, extension) == expected


def test_text_from_html_string():
    """Fetches the text from the html string"""

    html_str = "<b>A</b>"
    expected = "A"

    assert text_from_html_string(html_str) == expected


def test_text_from_html_string_with_line_breaks():
    """Replaces the linebreaks with \n"""

    html_str = "<p>A</p>B<br />C<p>D</p>"
    expected = "A\nB\nC\nD"

    assert text_from_html_string(html_str) == expected


def test_text_from_html_string_with_line_breaks_and_custom_separator():
    """Replaces the linebreaks with \t"""

    html_str = "<p>A</p>B<br />C<p>D</p>"
    expected = "A\tB\tC\tD"

    assert text_from_html_string(html_str, separator='\t') == expected
