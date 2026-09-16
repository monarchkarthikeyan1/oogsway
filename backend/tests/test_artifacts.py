import pytest
from app.core.artifact_generator import ArtifactGenerator
from app.utils.security import sanitize_html, prepare_iframe_document

def test_artifact_parsing():
    sample_response = """
Here is your requested product canvas dashboard:

<artifact title="Product Strategy Canvas" type="html">
<div class="card">
    <h1>Product Canvas</h1>
    <p>Strategic goals for PLG</p>
</div>
</artifact>
"""
    artifacts = ArtifactGenerator.parse_artifacts_from_response(sample_response)
    assert len(artifacts) == 1
    assert artifacts[0]["title"] == "Product Strategy Canvas"
    assert artifacts[0]["artifact_type"] == "html"
    assert "Product Canvas" in artifacts[0]["content"]

def test_html_sanitization_and_iframe_wrapper():
    raw_html = "<div class='test'><h1>Title</h1><script>alert('xss')</script></div>"
    sanitized = sanitize_html(raw_html)
    assert "<script>" not in sanitized
    assert "<h1>Title</h1>" in sanitized

    iframe_doc = prepare_iframe_document(sanitized, title="Test View")
    assert "Content-Security-Policy" in iframe_doc
    assert "<!DOCTYPE html>" in iframe_doc
