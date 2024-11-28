import multiprocessing
from langchain_community.chat_models import ChatLlamaCpp
from typing import List, Tuple
from pydantic import BaseModel, Field

class SkillGrading(BaseModel):
    skill: str = Field(description="The name of the skill")
    grading: str = Field(description="The proficiency level of the skill as Grundkenntnisse, Fortgeschritten or Experte ")

class Skillset(BaseModel):
    skills: List[SkillGrading] = Field(description="A list of skills and their grading")

# Path to your model weights
local_model = "Mistral-Nemo-Instruct-2407-IQ4_XS.gguf"

llm = ChatLlamaCpp(
    temperature=0.5,
    model_path=local_model,
    n_ctx=10000,
    #n_gpu_layers=0,
    n_batch=512,  # Adjust based on your system resources
    max_tokens=2048,
    n_threads=multiprocessing.cpu_count() - 1,
    repeat_penalty=1.5,
    top_p=0.5,
    verbose=False,
    seed=42
)
structured_llm = llm.with_structured_output(Skillset)

def extract_skills(job_description):
    system_prompt = (
        "You are an AI assistant that extracts a list of hard skills from a given job description. "
        "For each skill, provide only the skill name and the required proficiency level in parentheses "
        "(Grundkenntnisse, Fortgeschritten, Experte). List the skills in bullet points."
    )
    messages = [
        ("system", system_prompt),
        ("human", "Abgeschlossenes Studium (BWL) oder vergleichbare kaufmännische Ausbildung\nMindestens 3 Jahre Berufserfahrung im Einkauf oder in kaufmännischen Positionen\nFundierte Kenntnisse und Erfahrungen im Vertragsrecht und im Bereich Einkauf von Software\nErfahrung in der Erstellung und Prüfung von Leistungsbeschreibungen im IT-Umfeld\nErfahrung in der Durchführung von europaweiten Vergabeverfahren wünschenswert\nGute Kenntnisse in Microsoft Office, SAP, MM und SRM, Anwenderkenntnisse in SharePoint erwünscht\nÜberdurchschnittliches Engagement und ein ausgeprägtes Qualitäts- und Verantwortungsbewusstsein\nProzessorientierte, eigenständige, flexible und sehr strukturierte Arbeitsweise\nTeamfähigkeit, Offenheit und Kooperationsfähigkeit sowie hohe Flexibilität und proaktives Handeln\nVerbindliche, respektvolle und lösungsorientierte Kommunikation\nVerhandlungssichere Deutschkenntnisse in Wort und Schrift"),
        ("ai", "skills = [\n['Procurement Management', 'Experte'],\n['Contract Law', 'Experte'],\n['Software Procurement', 'Experte'],\n['IT Performance Specifications Creation', 'Fortgeschritten'],\n['European Tendering Procedures', 'Fortgeschritten'],\n['Microsoft Office', 'Experte'],\n['SAP MM', 'Fortgeschritten'],\n['SAP SRM', 'Fortgeschritten'],\n['SharePoint', 'Grundkenntnisse'],\n['Process-Oriented Workflows', 'Experte'],\n['Structured Work Methodologies', 'Experte'],\n['German Language Proficiency', 'Experte']\n]"),
        ("human", "Abgeschlossenes Studium im IT-Umfeld oder vergleichbare Ausbildung\nMindestens vier Jahre Berufserfahrung in den genannten Aufgabengebieten\nSehr gute Erfahrung in der Planung und Konzeption von komplexen IT-Architekturen\nExpertise im Bereich von Netzwerkarchitekturen, GBit- und TBit-Technologien, Gateways und IT-Sicherheit\nSolides Know-how in der strategischen Produktentwicklung\nSehr gute Deutschkenntnisse"),
        ("ai", "skills = [\n['IT-Architekturplanung', 'Experte'],\n['IT-Architekturkonzeption', 'Experte'],\n['Netzwerkarchitektur', 'Experte'],\n['GBit-Technologien', 'Fortgeschritten'],\n['TBit-Technologien', 'Fortgeschritten'],\n['Gateways', 'Fortgeschritten'],\n['IT-Sicherheit', 'Experte'],\n['Strategische Produktentwicklung', 'Experte'],\n['Deutschkenntnisse', 'Experte']\n]"),
        ("human", "Sehr guter Hochschulabschluss im Bereich Netzwerktechnik (LAN) wünschenswert\nMindestens fünf Jahre Berufserfahrung und sehr gute Kenntnisse im Bereich DDI\nGute Kenntnisse in der Planung und Design von IT-Netzwerken\nMehrj��hrige Erfahrung in Projektarbeit\nGute Kenntnisse im Umgang mit Funktions- und Konfigurationstests zur Entwicklung von Software- & Hardware-Releases von DDI-Komponenten\nAnalytisches Denkvermögen, hohe Leistungsbereitschaft und Reisebereitschaft (innerhalb Deutschlands)\nITIL-Zertifizierung wünschenswert\nSehr gute Präsentations- und Kommunikationsfähigkeiten auf Deutsch und Englisch\nIdealerweise Erfahrungen im Bundeswehr- bzw. Behördenumfeld"),
        ("ai", "skills = [\n['Network Technology (LAN)', 'Experte'],\n['DDI (DNS, DHCP, IPAM) Management', 'Experte'],\n['IT Network Planning', 'Experte'],\n['IT Network Design', 'Experte'],\n['Software Release Testing', 'Fortgeschritten'],\n['Hardware Release Testing', 'Fortgeschritten'],\n['Project Management', 'Fortgeschritten'],\n['Analytical Thinking', 'Experte'],\n['ITIL Framework', 'Fortgeschritten'],\n['German Language Proficiency', 'Experte'],\n['English Language Proficiency', 'Experte'],\n['Federal or Government Environment Experience', 'Grundkenntnisse']\n]"),
        ("human", job_description)
    ]
    return structured_llm.invoke(messages)

# Example usage
job_description = """
    
    Abgeschlossenes Studium (z. B. VWL, BWL) oder vergleichbare kaufmännische Ausbildung
    Mindestens 3 Jahre Berufserfahrung im Einkauf oder in kaufmännischen Positionen
    Kenntnisse und Erfahrungen im Vertragsrecht und im Bereich Einkauf von IT und Allgemeinen Bedarfen
    Erfahrung in der Erstellung und Prüfung von Leistungsbeschreibungen wünschenswert
    Erfahrung im Vergaberecht (ober- und unterschwellige Vergaben) von Vorteil
    Sehr gute Kenntnisse in Microsoft Office, SAP, MM und SRM, Anwenderkenntnisse in SharePoint erwünscht
    Überdurchschnittliches Engagement und ein ausgeprägtes Qualitäts- und Verantwortungsbewusstsein
    Organisationstalent, prozessorientierte, eigenständige, flexible und sehr strukturierte Arbeitsweise
    Teamfähigkeit, Offenheit und Kooperationsfähigkeit sowie hohe Flexibilität und proaktives Handeln
    Verbindliche, respektvolle und lösungsorientierte Kommunikation
    Verhandlungssichere Deutschkenntnisse in Wort und Schrift

"""

skset = extract_skills(job_description)
print(skset)