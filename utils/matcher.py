from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def calculate_dna_matrix(resume_text, found_skills):
    """
    Generate a 5-dimension array modeling Resume DNA out of 100.
    Dimensions: [Technical, Leadership, Impact, Communication, Problem Solving]
    """
    text = resume_text.lower()
    
    tech = min(100, len(found_skills) * 8 + 30)
    
    ld_count = sum(1 for w in ['led', 'managed', 'directed', 'coordinated', 'head', 'mentor', 'spearheaded', 'ceo', 'manager'] if w in text)
    leadership = min(100, ld_count * 15 + 20)
    
    im_count = sum(1 for w in ['increased', 'decreased', 'improved', 'resolved', 'achieved', '%', '$', 'revenue', 'delivered'] if w in text)
    impact = min(100, im_count * 10 + 25)
    
    co_count = sum(1 for w in ['presented', 'negotiated', 'collaborated', 'communicated', 'authored', 'wrote', 'published'] if w in text)
    comm = min(100, co_count * 12 + 30)
    
    pr_count = sum(1 for w in ['analyzed', 'solved', 'optimized', 'troubleshot', 'engineered', 'architected', 'researched'] if w in text)
    prob_solve = min(100, pr_count * 12 + 35)
    
    return [tech, leadership, impact, comm, prob_solve]

def calculate_detailed_breakdown(ats_score, resume_strength, found_skills, missing_skills, resume_text):
    """
    Compute specific percentage metrics breaking down the holistic score.
    """
    text = resume_text.lower()
    word_count = len(text.split())
    
    total_skills = len(found_skills) + len(missing_skills)
    skills_score = int((len(found_skills) / max(total_skills, 1)) * 100) if total_skills else 50
    
    impact_score = min(100, sum(1 for w in ['increased', 'improved', 'achieved', '%', '$', 'revenue'] if w in text) * 15 + 40)
    
    formatting_score = min(100, int((word_count / 400) * 100)) if word_count < 800 else max(40, 100 - int((word_count - 800)/10))
    
    keyword_score = int(ats_score)
    
    return {
        'skills': skills_score,
        'impact': impact_score,
        'formatting': formatting_score,
        'keyword': keyword_score
    }

def calculate_ats_score(resume_text, jd_text):
    """
    Computes a basic ATS match score using Cosine Similarity between resume and JD.
    """
    if not jd_text.strip():
        return 0.0
        
    documents = [resume_text, jd_text]
    vectorizer = CountVectorizer(stop_words='english')
    
    try:
        count_matrix = vectorizer.fit_transform(documents)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        return round(match_percentage, 2)
    except:
        return 0.0

def calculate_resume_strength(found_skills, missing_skills, ats_score, resume_text):
    """
    Calculate an overall resume strength rating out of 100.
    """
    strength = 0
    word_count = len(resume_text.split())
    if word_count > 300:
        strength += 30
    elif word_count > 150:
        strength += 20
    else:
        strength += 10
        
    total_skills = len(found_skills) + len(missing_skills)
    if total_skills > 0:
        skill_ratio = len(found_skills) / total_skills
        strength += int(skill_ratio * 40)
        
    strength += int((ats_score / 100) * 30)
    
    return min(strength, 100)
