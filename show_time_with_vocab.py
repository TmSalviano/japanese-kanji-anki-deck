import requests
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
import genanki


WANIKANI_API_KEY = "4efdd4b8-62d7-4e49-9fc1-4e99815fb3e9"
DECK_ID = 2059400110  
MODEL_ID = 1607392319  
REQUEST_DELAY = 60  


wanikani_model = genanki.Model(
    MODEL_ID,
    "WaniKani Kanji Detailed",
    fields=[
        {"name": "Subject_ID"},
        {"name": "Characters"},
        {"name": "Level"},
        {"name": "Meanings"},
        {"name": "Auxiliary_Meanings"},
        {"name": "Readings"},
        {"name": "Meaning_Mnemonic"},
        {"name": "Reading_Mnemonic"},
        {"name": "Meaning_Hint"},
        {"name": "Reading_Hint"},
        {"name": "Amalgamation_Subject_Ids"},
        {"name": "Component_Subject_Ids"},
        {"name": "Document_URL"},
        {"name": "Lesson_Position"},
        {"name": "Created_At"},
        {"name": "Data_Updated_At"},
        {"name": "Visually_Similar_Subject_Ids"},
        {"name": "Spaced_Repetition_System_ID"},
        {"name": "Hidden_At"},
        {"name": "Slug"},
    ],
    templates=[
        {
            "name": "Kanji Card",
            "qfmt": """<div class="kanji">{{Characters}}</div>
<div>Level {{Level}} • Lesson {{Lesson_Position}}</div>""",
            "afmt": """{{FrontSide}}
<hr>

<div class="section">
    <div class="section-title">Meanings</div>
    {{Meanings}}
</div>

<div class="section">
    <div class="section-title">Readings</div>
    {{Readings}}
</div>

<div class="section">
    <div class="section-title">Meaning Mnemonic</div>
    <div class="mnemonic-container">{{Meaning_Mnemonic}}</div>
</div>

<div class="section">
    <div class="section-title">Reading Mnemonic</div>
    <div class="mnemonic-container">{{Reading_Mnemonic}}</div>
</div>

<div class="button">
    <div class="section-title">Components & Relations</div>
    <div class="content">
        Components: {{Component_Subject_Ids}}<br>
        Used in: {{Amalgamation_Subject_Ids}}<br>
        Visually Similar: {{Visually_Similar_Subject_Ids}}
    </div>
</div>

<div class="button">
    <div class="section-title">Metadata</div>
    <div class="content">
        Subject ID: {{Subject_ID}}<br>
        Slug: {{Slug}}<br>
        Created: {{Created_At}}<br>
        Updated: {{Data_Updated_At}}<br>
        SRS System ID: {{Spaced_Repetition_System_ID}}<br>
        Document: <a href="{{Document_URL}}">WaniKani</a>
    </div>
</div>

<script>
    document.querySelectorAll('.button').forEach(button => {
        const title = button.querySelector('.section-title');
        const content = button.querySelector('.content');
        
        content.style.display = 'none';
        title.addEventListener('click', () => {
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        });
        title.style.cursor = 'pointer';
    });
</script>""",
        }
    ],
    css="""\
.card { 
    font-family: Arial; 
    font-size: 16px; 
    text-align: center; 
} 
.kanji { 
    font-size: 120px; 
    margin-bottom: 20px; 
} 
.section { 
    text-align: left; 
    margin: 10px 0; 
    padding: 10px; 
    border: 1px solid 
    border-radius: 5px; 
} 
.section-title { 
    font-weight: bold; 
    color: 
    margin-bottom: 5px; 
}
.button { 
    text-align: left; 
    margin: 10px 0; 
    padding: 10px; 
    border: 1px solid 
    border-radius: 5px; 
    cursor: pointer; 
}
.button .content { 
    margin-top: 5px; 
}
.mnemonic-container {
    font-size: 18px;
    line-height: 1.4;
}
.mnemonic-container * {
    font-size: inherit !important;
}
.mnemonic-container .radical,
.mnemonic-container .kanji,
.mnemonic-container .reading {
    font-size: inherit !important;
}
""",
)

def get_all_subjects() -> Dict[str, Dict[int, Dict[str, Any]]]:
    """Fetch all subjects (radicals, kanji, vocabulary) from WaniKani API"""
    headers = {"Authorization": f"Bearer {WANIKANI_API_KEY}"}
    subjects = {
        'radical': {},
        'kanji': {},
        'vocabulary': {}
    }
    
    for subject_type in ['radical', 'kanji', 'vocabulary']:
        next_url = f"https://api.wanikani.com/v2/subjects?types={subject_type}"
        request_count = 0
        
        while next_url:
            try:
                print(f"Fetching {subject_type} page: {next_url}")
                response = requests.get(next_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                for subject in data["data"]:
                    subjects[subject_type][subject["id"]] = subject
                
                request_count += 1
                next_url = data["pages"]["next_url"] if data["pages"]["next_url"] else None
                
                if next_url and request_count > 59:
                    print(f"Waiting {REQUEST_DELAY} seconds before next request...")
                    time.sleep(REQUEST_DELAY)
                    request_count = 0
                    
            except requests.exceptions.RequestException as e:
                print(f"API Error: {e}")
                break
    
    return subjects

def format_meanings(meanings: List[Dict[str, Any]]) -> str:
    """Format meanings as comma-separated list"""
    primary = [m['meaning'] for m in meanings if m['primary']]
    secondary = [m['meaning'] for m in meanings if not m['primary']]
    return ", ".join(primary + secondary)

def format_aux_meanings(aux_meanings: List[Dict[str, Any]]) -> str:
    """Format auxiliary meanings"""
    return ", ".join(am['meaning'] for am in aux_meanings) if aux_meanings else ""

def format_readings(readings: List[Dict[str, Any]]) -> str:
    """Format readings as comma-separated list"""
    onyomi = [r['reading'] for r in readings if r['type'] == 'onyomi']
    kunyomi = [r['reading'] for r in readings if r['type'] == 'kunyomi']
    nanori = [r['reading'] for r in readings if r['type'] == 'nanori']
    return ", ".join(onyomi + kunyomi + nanori)

def format_component_ids(ids: List[int], subjects: Dict[str, Dict[int, Dict[str, Any]]]) -> str:
    """Format component IDs (radicals/kanji) as characters"""
    if not ids:
        return ""
    
    components = []
    for id in ids:
        if id in subjects['kanji']:
            char = subjects['kanji'][id]["data"]["characters"]
        elif id in subjects['radical']:
            char = subjects['radical'][id]["data"]["characters"]
        else:
            char = str(id)
        components.append(str(char))
    
    return ", ".join(components)

def format_amalgamation_ids(ids: List[int], vocabulary: Dict[int, Dict[str, Any]]) -> str:
    """Format vocabulary IDs as characters"""
    if not ids:
        return ""
    return ", ".join(vocabulary[id]["data"]["characters"] if id in vocabulary else str(id) for id in ids)

def clean_html_text(text: str) -> str:
    """Clean WaniKani HTML formatting"""
    if not text:
        return ""
    replacements = [
        ("<radical>", "<span class='radical'>"),
        ("</radical>", "</span>"),
        ("<kanji>", "<span class='kanji'>"),
        ("</kanji>", "</span>"),
        ("<reading>", "<span class='reading'>"),
        ("</reading>", "</span>")
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def create_anki_deck(subjects: Dict[str, Dict[int, Dict[str, Any]]]) -> genanki.Deck:
    """Create Anki deck with all kanji cards"""
    deck = genanki.Deck(DECK_ID, "WaniKani Kanji")
    
    for kanji_id, kanji_data in subjects['kanji'].items():
        data = kanji_data["data"]
        
        fields = [
            str(kanji_id),
            data["characters"],
            str(data["level"]),
            format_meanings(data["meanings"]),
            format_aux_meanings(data.get("auxiliary_meanings", [])),
            format_readings(data["readings"]),
            clean_html_text(data["meaning_mnemonic"]),
            clean_html_text(data["reading_mnemonic"]),
            clean_html_text(data.get("meaning_hint", "")),
            clean_html_text(data.get("reading_hint", "")),
            format_amalgamation_ids(data["amalgamation_subject_ids"], subjects['vocabulary']),
            format_component_ids(data["component_subject_ids"], subjects),
            data["document_url"],
            str(data["lesson_position"]),
            data["created_at"],
            kanji_data["data_updated_at"],
            format_component_ids(data.get("visually_similar_subject_ids", []), subjects),
            str(data["spaced_repetition_system_id"]),
            str(data.get("hidden_at", "")),
            data["slug"]
        ]
        
        note = genanki.Note(model=wanikani_model, fields=fields)
        deck.add_note(note)
    
    return deck

def main():
    """Main workflow to fetch all data and create Anki deck"""
    print("Starting WaniKani to Anki import process...")
    
    print("Fetching all subjects from WaniKani...")
    all_subjects = get_all_subjects()
    
    if not all_subjects['kanji']:
        print("No kanji found or error occurred during fetch.") 
        return
    
    print(f"Found {len(all_subjects['kanji'])} kanji, {len(all_subjects['radical'])} radicals, "
          f"{len(all_subjects['vocabulary'])} vocabulary items")
    
    print("Creating Anki deck...")
    deck = create_anki_deck(all_subjects)
    
    print("Generating Anki package...")
    package = genanki.Package(deck)
    package.models = [wanikani_model]
    output_file = f"wanikani_kanji_detailed_{datetime.now().strftime('%Y%m%d')}.apkg"
    package.write_to_file(output_file)
    
    print("\nImport complete!")
    print(f"Created deck with {len(all_subjects['kanji'])} kanji")
    print(f"Output file: {output_file}")

if __name__ == "__main__":
    main()