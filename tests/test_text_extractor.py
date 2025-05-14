import pytest
from src.scraper.text_extractor import extract_text_from_urls

def test_extract_text_from_urls():
    # Test with a known good URL
    test_urls = ["https://example.com"]
    results = extract_text_from_urls(test_urls)
    
    assert len(results) == 1
    assert isinstance(results[0], str)
    assert len(results[0]) > 0

def test_extract_text_from_invalid_url():
    # Test with an invalid URL
    test_urls = ["https://thisisnotarealwebsite123456789.com"]
    results = extract_text_from_urls(test_urls)
    
    assert len(results) == 1
    assert results[0] == ""  # Should return empty string for failed extraction

def test_extract_text_from_multiple_urls():
    # Test with multiple URLs
    test_urls = [
        "https://example.com",
        "https://example.org"
    ]
    results = extract_text_from_urls(test_urls)
    
    assert len(results) == 2
    assert all(isinstance(text, str) for text in results) 