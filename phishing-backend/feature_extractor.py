import re
from urllib.parse import urlparse
import requests
import whois
import dns.resolver
from datetime import datetime

def extract_features_from_url(url: str) -> list[float]:
    """
    Extract phishing detection features from a URL.
    Returns a list of 30 float features as required by your model.
    1.0 = suspicious, -1.0 = safe (following your training data scheme).
    """

    features = []

    # Parse URL components
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    scheme = parsed.scheme.lower()

    # 1. UsingIP: URL contains IP address instead of domain
    ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
    using_ip = 1.0 if re.match(ip_pattern, domain) else -1.0
    features.append(using_ip)

    # 2. LongURL: Length of URL > 75 suspicious
    long_url = 1.0 if len(url) > 75 else -1.0
    features.append(long_url)

    # 3. ShortURL: Uses URL shortening service
    shorteners = ['bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co', 'is.gd', 'buff.ly', 'adf.ly']
    short_url = 1.0 if any(shortener in domain for shortener in shorteners) else -1.0
    features.append(short_url)

    # 4. Symbol@: '@' in URL suspicious
    symbol_at = 1.0 if '@' in url else -1.0
    features.append(symbol_at)

    # 5. Redirecting//: multiple '//' after protocol suspicious
    redirecting = 1.0 if url.count('//') > 1 else -1.0
    features.append(redirecting)

    # 6. PrefixSuffix-: '-' in domain suspicious
    prefix_suffix = 1.0 if '-' in domain else -1.0
    features.append(prefix_suffix)

    # 7. SubDomains: More than 2 subdomains suspicious
    subdomains_count = domain.count('.') - 1 if domain.count('.') > 1 else 0
    subdomains = 1.0 if subdomains_count > 2 else -1.0
    features.append(subdomains)

    # 8. HTTPS: uses HTTPS (good)
    https = -1.0 if scheme == 'https' else 1.0  # safe if HTTPS, suspicious if not
    features.append(https)

    # 9. DomainRegLen: domain age in months <= 12 suspicious, else safe
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_months = (datetime.now() - creation_date).days / 30
            domain_reg_len = -1.0 if age_months > 12 else 1.0
        else:
            domain_reg_len = 1.0  # unknown treated suspicious
    except Exception:
        domain_reg_len = 1.0  # unable to get data - suspicious
    features.append(domain_reg_len)

    # 10. Favicon: favicon from different domain suspicious
    # Simple check: favicon URL contains domain name or not
    try:
        res = requests.get(url, timeout=3)
        favicon_suspicious = 1.0
        if res.status_code == 200:
            html = res.text.lower()
            favicons = re.findall(r'<link[^>]+rel=["\']shortcut icon["\'][^>]+href=["\']([^"\']+)["\']', html)
            if not favicons:
                favicons = re.findall(r'<link[^>]+rel=["\']icon["\'][^>]+href=["\']([^"\']+)["\']', html)
            for fav in favicons:
                if domain in fav:
                    favicon_suspicious = -1.0
                    break
        features.append(favicon_suspicious)
    except Exception:
        features.append(1.0)  # can't fetch page -> suspicious

    # 11. NonStdPort: uses non-standard port suspicious
    port = parsed.port
    non_std_port = 1.0 if port and port not in [80, 443, 8080] else -1.0
    features.append(non_std_port)

    # 12. HTTPSDomainURL: 'https' token in domain suspicious
    https_domain_url = 1.0 if 'https' in domain else -1.0
    features.append(https_domain_url)

    # 13. RequestURL: embedded objects from different domain suspicious
    # Basic: check if URL contains too many external resource references (stub with simple heuristic)
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            html = res.text.lower()
            external_refs = len(re.findall(r'src=["\']https?://', html))  # count external scripts/images
            request_url = 1.0 if external_refs > 5 else -1.0
        else:
            request_url = 1.0
    except Exception:
        request_url = 1.0
    features.append(request_url)

    # 14. AnchorURL: anchors href different domain suspicious
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            html = res.text.lower()
            anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', html)
            suspicious_count = 0
            total = len(anchors)
            for a in anchors:
                if a.startswith('http') and domain not in a:
                    suspicious_count += 1
            anchor_url = 1.0 if total > 0 and (suspicious_count / total) > 0.5 else -1.0
        else:
            anchor_url = 1.0
    except Exception:
        anchor_url = 1.0
    features.append(anchor_url)

    # 15. LinksInScriptTags: number of script links suspicious
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            html = res.text.lower()
            scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
            script_external = sum(1 for s in scripts if domain not in s)
            links_in_script_tags = 1.0 if script_external > 3 else -1.0
        else:
            links_in_script_tags = 1.0
    except Exception:
        links_in_script_tags = 1.0
    features.append(links_in_script_tags)

    # 16. ServerFormHandler: form action empty or external domain suspicious
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            html = res.text.lower()
            forms = re.findall(r'<form[^>]+action=["\']([^"\']*)["\']', html)
            suspicious = 0
            total = len(forms)
            for f in forms:
                if not f or (f.startswith('http') and domain not in f):
                    suspicious += 1
            server_form_handler = 1.0 if total > 0 and (suspicious / total) > 0.5 else -1.0
        else:
            server_form_handler = 1.0
    except Exception:
        server_form_handler = 1.0
    features.append(server_form_handler)

    # 17. InfoEmail: mailto present suspicious
    try:
        res = requests.get(url, timeout=3)
        info_email = 1.0 if res.status_code == 200 and 'mailto:' in res.text.lower() else -1.0
    except Exception:
        info_email = 1.0
    features.append(info_email)

    # 18. AbnormalURL: URL not matching WHOIS domain suspicious
    try:
        w = whois.whois(domain)
        whois_domain = w.domain_name
        if isinstance(whois_domain, list):
            whois_domain = whois_domain[0]
        abnormal_url = 1.0 if whois_domain is None or whois_domain.lower() not in domain else -1.0
    except Exception:
        abnormal_url = 1.0
    features.append(abnormal_url)

    # 19. WebsiteForwarding: more than one forwarding suspicious
    # Count redirects using requests
    try:
        res = requests.get(url, timeout=5)
        website_forwarding = 1.0 if len(res.history) > 1 else -1.0
    except Exception:
        website_forwarding = 1.0
    features.append(website_forwarding)

    # 20. StatusBarCust: can't detect from backend - assume safe
    status_bar_cust = -1.0
    features.append(status_bar_cust)

    # 21. DisableRightClick: can't detect from backend - assume safe
    disable_right_click = -1.0
    features.append(disable_right_click)

    # 22. UsingPopupWindow: can't detect from backend - assume safe
    using_popup_window = -1.0
    features.append(using_popup_window)

    # 23. IframeRedirection: iframe src external suspicious
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            html = res.text.lower()
            iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', html)
            suspicious_iframes = sum(1 for i in iframes if domain not in i)
            iframe_redirection = 1.0 if suspicious_iframes > 0 else -1.0
        else:
            iframe_redirection = 1.0
    except Exception:
        iframe_redirection = 1.0
    features.append(iframe_redirection)

    # 24. AgeofDomain: domain age < 6 months suspicious
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            ageofdomain = 1.0 if age_days < 180 else -1.0
        else:
            ageofdomain = 1.0
    except Exception:
        ageofdomain = 1.0
    features.append(ageofdomain)

    # 25. DNSRecording: DNS record found safe, none suspicious
    try:
        dns.resolver.resolve(domain)
        dns_recording = -1.0
    except Exception:
        dns_recording = 1.0
    features.append(dns_recording)

    # 26. WebsiteTraffic: Alexa rank > threshold suspicious (stub, assume safe)
    website_traffic = -1.0
    features.append(website_traffic)

    # 27. PageRank: Google PageRank low suspicious (stub, assume safe)
    page_rank = -1.0
    features.append(page_rank)

    # 28. GoogleIndex: indexed in Google safe (stub, assume safe)
    google_index = -1.0
    features.append(google_index)

    # 29. LinksPointingToPage: number of backlinks low suspicious (stub, assume safe)
    links_pointing_to_page = -1.0
    features.append(links_pointing_to_page)

    # 30. StatsReport: website stats report suspicious (stub, assume safe)
    stats_report = -1.0
    features.append(stats_report)

    return features
