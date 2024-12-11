import re


def clean_company_url(url):
    if not url:
        return ""

    text_and_links = re.sub(r'<[^>]+>', ' ', url).strip()

    urls = re.findall(r'https?://[^\s<>"\']+', text_and_links)
    if urls:
        base_url = urls[0]
        base_url = re.sub(r'\?(utm_source|ref|gh_jid).*', '', base_url)
        base_url = re.sub(r'&(utm_source|ref|gh_jid).*', '', base_url)
        return base_url

    return ""


def extract_company_name(text):
    company = re.sub(r'at\s*$', '', text)  
    company = re.sub(r'https.*$', '', company)  
    company = re.sub(r'Company:\s*', '', company) 
    company = re.sub(r'[^\w\s-]', '', company)  
    company = re.sub(r'\s+', ' ', company)  
    return company.strip()


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\-.,!?]', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()
