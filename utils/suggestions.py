import random

def generate_suggestions(found_skills, missing_skills, match_score, role, resume_text):
    suggestions = []
    resume_lower = resume_text.lower()
    
    # 1. Structural Suggestions (Dynamic based on content)
    word_count = len(resume_text.split())
    if word_count < 250:
        suggestions.append(f"Content Density: Your profile is relatively brief ({word_count} words). For a {role} role, aim for 400-600 words to ensure sufficient semantic depth for ATS algorithms.")
    
    if "project" not in resume_lower:
        suggestions.append(f"Portfolio Gap: Targeted {role} roles favor candidates with documented project implementations. Consider adding a 'Projects' section to showcase applied technical skills.")

    # 2. Match Score Qualitative Analysis
    if match_score < 40:
        suggestions.append(f"Semantic Alignment: Your match score ({match_score:.0f}%) indicates a severe keyword deficit. Align your terminology precisely with the industry-standard nomenclature for {role}.")
    elif match_score < 75:
        suggestions.append(f"Refinement Pass: You have a solid foundation, but increasing the density of core {role} keywords will push you into the 'Superior Match' category.")

    # 3. Dynamic Skill-Based Suggestions (THE CORE FIX)
    if missing_skills:
        # Sort or randomize for variety? Let's take the first 3
        primary_gaps = ", ".join(missing_skills[:3]).title()
        
        # Multiple phrasing options for variety
        templates = [
            f"Integrate {primary_gaps} into your Professional Summary to instantly boost your visibility metrics for this target role.",
            f"Our heuristics identified a deficit in {primary_gaps}. Direct injection of these terms into your bullet points is highly recommended.",
            f"To achieve keyword saturation, ensure {primary_gaps} are clearly articulated within your Skills matrix."
        ]
        suggestions.append(random.choice(templates))

    # 4. Action Verb Optimization
    action_verbs = ["architected", "orchestrated", "engineered", "optimized", "increased", "spearheaded", "developed", "managed"]
    found_verbs = [v for v in action_verbs if v in resume_lower]
    if len(found_verbs) < 3:
        suggestions.append("Syntactic Polish: Shift from passive descriptions to active results. Use high-impact verbs like 'Architected' or 'Orchestrated' to lead your experience bullets.")

    # 5. Final Grounding
    if match_score > 85 and not missing_skills:
        suggestions.append("Benchmark Achievement: Your profile aligns with top-percentile candidate scores. Focus on visual formatting and layout stability for human review.")

    # Cap to 4 highest priority suggestions for premium layout balance
    return suggestions[:4]
