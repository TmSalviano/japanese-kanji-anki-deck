import genanki
from datetime import datetime


wanikani_model = genanki.Model(
    1607392319,  
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
    {{Meaning_Mnemonic}}
</div>

<div class="section">
    <div class="section-title">Reading Mnemonic</div>
    {{Reading_Mnemonic}}
</div>

<div class="button">
    <div class="section-title">Components & Relations</div>
    <div class="content">
        Component IDs: {{Component_Subject_Ids}}<br>
        Amalgamation IDs: {{Amalgamation_Subject_Ids}}<br>
        Visually Similar IDs: {{Visually_Similar_Subject_Ids}}
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
        
        // Hide content initially
        content.style.display = 'none';
        
        title.addEventListener('click', () => {
            if (content.style.display === 'none') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
        
        // Add cursor pointer to indicate clickable
        title.style.cursor = 'pointer';
    });
</script>""",
        }
    ],
    css="""\
.card { font-family: Arial; font-size: 16px; text-align: center; } 
.kanji { font-size: 120px; margin-bottom: 20px; } 
.section { text-align: left; margin: 10px 0; padding: 10px; border: 1px solid 
.section-title { font-weight: bold; color: 
.button { text-align: left; margin: 10px 0; padding: 10px; border: 1px solid 
.button .content { margin-top: 5px; }
""",
)


wanikani_deck = genanki.Deck(
    2059400110,  
    "WaniKani Kanji (Template)"
)

example_note = genanki.Note(
    model=wanikani_model,
    fields=[
        "1",                                   
        "水",                                  
        "1",                                   
        "water, Wednesday",                   
        "",                                    
        "すい, みず",                         
        "This is the meaning mnemonic...",    
        "This is the reading mnemonic...",     
        "",                                    
        "",                                    
        "2,3,4",                              
        "5,6",                                
        "https://www.wanikani.com/kanji/水",  
        "10",                                  
        datetime.now().isoformat(),            
        datetime.now().isoformat(),            
        "",                                   
        "1",                                  
        "",                                   
        "water"                               
    ]
)

wanikani_deck.add_note(example_note)


package = genanki.Package(wanikani_deck)
package.models = [wanikani_model]
package.write_to_file('wanikani_kanji_template_with_example_toggle.apkg')

print("Arquivo gerado: 'wanikani_kanji_template_with_example.apkg'")
print("Contém:")
print("- Modelo 'WaniKani Kanji Detailed'")
print("- 1 card de exemplo (kanji 水)")