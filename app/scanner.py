import hashlib
import io
import re
from PIL import Image, ExifTags
import fitz

EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
PHONE = re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)")
PAN = re.compile(r"(?<![A-Z0-9])[A-Z]{5}\d{4}[A-Z](?![A-Z0-9])")
IPV4 = re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)")

def inspect(name, content):
    ext = name.rsplit(".",1)[-1].lower() if "." in name else ""
    if ext not in {"pdf","txt","png","jpg","jpeg"}:
        raise ValueError("Only PDF, TXT, JPG, JPEG and PNG are supported.")
    if len(content)>25*1024*1024:
        raise ValueError("File exceeds 25 MB.")
    sha = hashlib.sha256(content).hexdigest()
    findings = []
    extracted = ""
    metadata = {}
    if ext == "pdf":
        try:
            doc=fitz.open(stream=content,filetype="pdf")
            if doc.needs_pass:
                raise ValueError("Password-protected PDFs are not supported.")
            if len(doc)>150:
                raise ValueError("PDF exceeds the 150-page analysis limit.")
            extracted="\n".join(page.get_text() for page in doc)
            metadata={k:str(v) for k,v in doc.metadata.items() if v and k in {"author","creator","producer","creationDate","modDate"}}
            doc.close()
            if metadata:
                findings.append({"type":"Document metadata","severity":"Low","detail":"Embedded author, software or timestamp metadata found","count":len(metadata)})
        except ValueError:
            raise
        except Exception as e:
            raise ValueError("Could not parse this PDF.") from e
    elif ext == "txt":
        extracted=content.decode("utf-8",errors="replace")
    else:
        try:
            with Image.open(io.BytesIO(content)) as img:
                exif=img.getexif()
                metadata={str(ExifTags.TAGS.get(k,k)):str(v)[:150] for k,v in exif.items()}
                if metadata:
                    findings.append({"type":"Image EXIF metadata","severity":"Medium","detail":"Embedded photo metadata detected (may reveal device or time)","count":len(metadata)})
                if any(k in metadata for k in ("GPSInfo","GPSLatitude","GPSLongitude")) or 34853 in exif:
                    findings.append({"type":"GPS metadata","severity":"High","detail":"GPS-related EXIF data found; location may be exposed","count":1})
        except Exception as e:
            raise ValueError("Could not decode this image.") from e
    patterns=[
        ("Email address",EMAIL,"Medium"),
        ("Indian phone number",PHONE,"Medium"),
        ("PAN-like identifier",PAN,"High"),
        ("IPv4 address",IPV4,"Low")
    ]
    for label,pattern,severity in patterns:
        matches=pattern.findall(extracted)
        if matches:
            findings.append({"type":label,"severity":severity,"detail":"Potentially sensitive pattern found (review for false positives)","count":len(matches)})
    weights={"Low":10,"Medium":25,"High":40,"Critical":60}
    score=min(100,sum(weights[f["severity"]] for f in findings))
    risk="Critical" if score>=80 else "High" if score>=50 else "Medium" if score>=20 else "Low"
    return {"filename":name,"filetype":ext.upper(),"sha256":sha,"score":score,"risk":risk,"findings":findings,"metadata":metadata,"text_chars":len(extracted)}
