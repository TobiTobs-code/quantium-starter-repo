from app import app


def test_header_is_present():
    page_text = str(app.layout)
    assert "Soul Foods Pink Morsels Sales Visualiser" in page_text


def test_visualisation_is_present():
    page_text = str(app.layout)
    assert "sales-line-chart" in page_text


def test_region_picker_is_present():
    page_text = str(app.layout)
    assert "region-filter" in page_text