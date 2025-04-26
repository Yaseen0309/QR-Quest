import re
import tldextract

def extract_features(url):
    features = {}
    features["url_length"] = len(url)
    features["num_dots"] = url.count('.')
    features["has_ip"] = bool(re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", url))  # ✅ Corrected regex
    features["has_https"] = "https" in url
    features["has_at_symbol"] = "@" in url
    features["has_shortener"] = any(x in url for x in ["bit.ly", "tinyurl", "t.co"])
    ext = tldextract.extract(url)
    features["subdomain_length"] = len(ext.subdomain)
    features["is_brand_mismatch"] = not (ext.domain in url.lower())
    return features
