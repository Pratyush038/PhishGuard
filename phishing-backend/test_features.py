from feature_extractor import extract_features_from_url

def test_url(url):
    print(f"\nTesting URL: {url}")
    features = extract_features_from_url(url)
    print(f"Number of features: {len(features)}")
    print("First 10 features:", features[:10])
    print("Last 10 features:", features[-10:])

if __name__ == "__main__":
    safe_url = "https://www.google.com"
    phishing_url = "http://192.168.1.1/login@evil.com"  # suspicious IP + '@'
    short_url = "http://bit.ly/abcd1234"
    old_domain = "https://www.amazon.com"
    new_domain = "http://test-new-domain-xyz123.com"

    for url in [safe_url, phishing_url, short_url, old_domain, new_domain]:
        test_url(url)
