from PIL import Image
import os,json,time,random,re,fitz
from openai import RateLimitError, APIError,OpenAI
from lxml import etree
from bs4 import BeautifulSoup

def call_llm(prompt, api, config_list, llm_config):

    api_key = api
    client = OpenAI(api_key=api_key, base_url=config_list[0]['base_url'])
    model = config_list[0]['model']
    temp = llm_config.get('temperature', 0)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temp
    )
    return response

def get_XML_context(xml_path):
    with open(xml_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")    
    irrelevant_sections = {
        "supplementary materials", "declaration of interests",
        "declaration of competing interest",
        "credit authorship contribution statement",
        "author contributions", "data availability",
        "funding", "fundings", "acknowledgment",
        "acknowledgements", "reference", "references"
    }
    for div in soup.find_all("div"):
        head = div.find("head")
        if head and head.text.strip().lower() in irrelevant_sections:
            div.decompose()  
    full_text = soup.get_text(" ", strip=True)
    return full_text

def get_XML_titleabstract(xml_path):
    """
    Extract ONLY the title and abstract text from a TEI/XML file.
    Return as a single text string.
    """
    with open(xml_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    # -------- Extract Title ----------
    title = ""
    title_stmt = soup.find("titleStmt")
    if title_stmt and title_stmt.find("title"):
        title = title_stmt.find("title").get_text(" ", strip=True)
    else:
        # fallback: any <title>
        t = soup.find("title")
        if t:
            title = t.get_text(" ", strip=True)
    # -------- Extract Abstract ----------
    abstract = ""
    abstract_tag = soup.find("abstract")
    if abstract_tag:
        abstract = abstract_tag.get_text(" ", strip=True)
    # -------- Combine into text output ----------
    result = f"Title:\n{title}\nAbstract:\n{abstract}"
    return result

def extract_paper_basic_info(xml_path):
    """Extract DOI, title, authors, year, journal from GROBID XML."""
    if not os.path.exists(xml_path):
        return {}
    
    tree = etree.parse(xml_path)
    root = tree.getroot()

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    metadata = {
        "doi": None,
        "title": None,
        "authors": [],
        "journal": None,
        "year": None
    }
    #filename
    metadata["filename"] = xml_path.split('\\')[-1]
    # DOI
    doi_el = root.xpath("//tei:idno[@type='DOI']", namespaces=ns)
    if doi_el:
        metadata["doi"] = doi_el[0].text

    # Title
    title_el = root.xpath("//tei:titleStmt/tei:title", namespaces=ns)
    if title_el:
        metadata["title"] = title_el[0].text

    # Authors
    authors = root.xpath("//tei:author/tei:persName", namespaces=ns)
    for a in authors:
        name = " ".join(filter(None, [
            (a.find("tei:forename", namespaces=ns).text if a.find("tei:forename", namespaces=ns) is not None else None),
            (a.find("tei:surname", namespaces=ns).text if a.find("tei:surname", namespaces=ns) is not None else None)
        ]))
        metadata["authors"].append(name.strip())

    # Journal
    journal_el = root.xpath("//tei:monogr/tei:title[@level='j']", namespaces=ns)
    if journal_el:
        metadata["journal"] = journal_el[0].text

    # Year
    date_el = root.xpath("//tei:imprint/tei:date", namespaces=ns)
    if date_el and "when" in date_el[0].attrib:
        metadata["year"] = date_el[0].attrib["when"]

    return metadata