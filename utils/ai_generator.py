import re

def enhance_bullet(text):
    """Deterministically transforms passive/weak verbs to strong action syntax."""
    replacements = {
        r'\bmade\b': 'Engineered',
        r'\bdid\b': 'Executed',
        r'\bhelped\b': 'Facilitated',
        r'\bworked on\b': 'Spearheaded',
        r'\bbuilt\b': 'Architected',
        r'\bran\b': 'Orchestrated',
        r'\bgot\b': 'Secured',
        r'\bfixed\b': 'Resolved',
        r'\bmanaged\b': 'Orchestrated',
        r'\bled\b': 'Spearheaded',
        r'\bimproved\b': 'Optimised',
        r'\bused\b': 'Leveraged',
        r'\blooked at\b': 'Analyzed',
        r'\bchecked\b': 'Audited',
        r'\bsaved\b': 'Economized',
        r'\bchanged\b': 'Transformed',
        r'\bshowed\b': 'Demonstrated',
        r'\bgave\b': 'Delivered'
    }
    
    text = text.strip()
    if not text:
        return ""
        
    for weak, strong in replacements.items():
        text = re.sub(weak, strong, text, flags=re.IGNORECASE)
        
    # Apply casing to the first word specifically after replacement
    words = text.split()
    if words:
        words[0] = words[0].capitalize()
        text = " ".join(words)

    if not text.endswith('.'):
        text += '.'
        
    return text

def heuristic_resume_build(data):
    """
    Simulates a comprehensive LLM capability by applying deterministic Python heuristic vectors 
    against user inputs, translating passive wording into hard action verbs.
    """
    if not data:
        return {"error": "No input data provided."}
        
    processed = data
    
    # 1. Synthesize Summary Profile
    role = data.get('target', {}).get('role', 'Professional')
    ind = data.get('target', {}).get('industry', '')
    level = data.get('target', {}).get('level', '')
    
    ind_str = f" in the {ind} sector" if ind else ""
    lvl_str = f"An adaptable {level}" if level else "A dedicated professional"
    
    processed['synthetic_summary'] = f"{lvl_str} actively seeking a {role} position{ind_str}. Focused on driving continuous optimization, bridging cross-functional deployments, and delivering measurable impact through structured methodologies."
    
    # 2. Synthesize Experience Bullets
    if 'experience' in processed:
        for exp in processed['experience']:
            desc_raw = exp.get('desc', '')
            bullets = [d.strip() for d in desc_raw.split('\n') if d.strip()]
            exp['synthetic_bullets'] = [enhance_bullet(b) for b in bullets]
            
    # 3. Synthesize Project Bullets
    if 'projects' in processed:
        for proj in processed['projects']:
            desc_raw = proj.get('desc', '')
            bullets = [d.strip() for d in desc_raw.split('\n') if d.strip()]
            proj['synthetic_bullets'] = [enhance_bullet(b) for b in bullets]
            
    return processed


def extract_experience_lines(raw_text):
    """
    Parses raw resume text to extract potential work experience bullet lines.
    Filters by line length and patterns indicating action/passive descriptions.
    """
    if not raw_text:
        return []
        
    lines = raw_text.split('\n')
    candidates = []
    
    bullet_verbs = ['made', 'did', 'helped', 'worked', 'built', 'ran', 'got', 'fixed', 'managed', 'led', 'improved', 'used', 'developed', 'created', 'designed', 'assisted', 'coordinated', 'support', 'responsible', 'implemented']
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        clean_line = re.sub(r'^[-\*•o+■\d\.\s]+', '', line).strip()
        
        if 35 <= len(clean_line) <= 200:
            lower_line = clean_line.lower()
            word_tokens = lower_line.split()
            
            if len(word_tokens) >= 5:
                contains_verb = any(verb in word_tokens[:3] for verb in bullet_verbs) or clean_line[0].isupper()
                if contains_verb:
                    candidates.append(clean_line)
                    
    if len(candidates) < 2:
        candidates = []
        for line in lines:
            line = line.strip()
            clean_line = re.sub(r'^[-\*•o+■\d\.\s]+', '', line).strip()
            if 30 <= len(clean_line) <= 250 and len(clean_line.split()) >= 4:
                candidates.append(clean_line)
                
    seen = set()
    enhanced = []
    for c in candidates:
        enhanced_c = enhance_bullet(c)
        if enhanced_c and enhanced_c not in seen:
            seen.add(enhanced_c)
            enhanced.append(enhanced_c)
            if len(enhanced) >= 4:
                break
                
    return enhanced


