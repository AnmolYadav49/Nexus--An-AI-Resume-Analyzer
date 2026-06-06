import re

# Dramatically expanded domain knowledge dictionary
SKILL_DICTIONARY = {
    "Python Developer": ["python", "django", "flask", "fastapi", "rest", "api", "postgres", "mysql", "docker", "aws", "celery", "redis", "sql", "git", "linux"],
    "Data Scientist": ["python", "r", "sql", "machine learning", "statistics", "scikit-learn", "tensorflow", "keras", "pandas", "numpy", "matplotlib", "seaborn", "tableau", "nlp", "deep learning"],
    "ML Engineer": ["python", "c++", "pytorch", "tensorflow", "keras", "aws", "gcp", "docker", "kubernetes", "nlp", "computer vision", "opencv", "yolo", "cuda", "llm", "langchain"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "express", "mongodb", "vue.js", "angular", "tailwind", "bootstrap", "sass", "git", "typescript"],
    "UI/UX Designer": ["figma", "adobe xd", "sketch", "user research", "wireframing", "prototyping", "design systems", "user flows", "interaction design", "principle", "after effects", "css", "html"],
    "Civil Engineer": ["autocad", "civil 3d", "sap2000", "staad", "etabs", "structural analysis", "concrete", "steel", "project management", "estimation", "surveying", "revit"],
    "Marketing Specialist": ["seo", "sem", "google analytics", "hubspot", "content strategy", "social media", "meta ads", "google ads", "cro", "copywriting"],
    "Financial Analyst": ["excel", "financial modeling", "sql", "bloomberg", "valuation", "accounting", "corporate finance", "risk assessment"],
    "DevOps Engineer": ["jenkins", "gitlab", "kubernetes", "docker", "aws", "terraform", "ansible", "ci/cd", "linux", "bash", "prometheus", "grafana"],
    "Product Manager": ["agile", "jira", "roadmap", "a/b testing", "cross-functional", "scrum", "confluence", "product strategy"],
    "HR Manager": ["talent acquisition", "employee relations", "workday", "hris", "greenhouse", "recruiting", "compliance", "onboarding"],
    "Mechanical Engineer": ["solidworks", "autocad mechanical", "thermodynamics", "hvac", "catia", "matlab", "simulink", "cad", "manufacturing"],
    "Backend Developer": ["java", "go", "rust", "c#", "kubernetes", "grpc", "kafka", "cassandra", "aws", "sql", "mongodb", "redis", "microservices"],
    "Cloud Architect": ["aws", "azure", "gcp", "solutions architecture", "terraform", "cloudformation", "iam", "networking", "distributed systems"],
    "Network Engineer": ["cisco", "bgp", "ospf", "wan", "ccna", "ccnp", "firewalls", "tcp/ip", "wireshark", "routing", "switching"],
    "Cybersecurity Analyst": ["penetration testing", "threat hunting", "soc", "wireshark", "metasploit", "siem", "owasp", "sast", "dast", "security analysis"],
    "Mobile Developer": ["kotlin", "java", "swift", "objective-c", "android", "ios", "jetpack compose", "room", "coroutines", "xcode", "react native", "flutter"]
}

def extract_skills(text, role, job_description=None):
    """
    Extract skills from text dynamically. 
    If job_description is provided, it prioritizes keywords found in the JD.
    """
    text = text.lower()
    found_skills = []
    
    # 1. Define the search space: either JD keywords or role-specific dictionary
    search_space = set()
    if job_description:
        # Extract skills from JD first
        jd_skills = extract_jd_skills(job_description)
        search_space.update(jd_skills)
    
    # Always include role-specific dictionary as a baseline
    search_space.update(SKILL_DICTIONARY.get(role, []))
    
    # If search space is still small, pull from a broader "global" set for the domain (optional refinement)
    # But for now, let's stick to the high-relevance terms
        
    for skill in search_space:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            if skill not in found_skills:
                found_skills.append(skill)
            
    return found_skills

def extract_jd_skills(jd_text):
    """
    Sweeps a JD for any known skills across ALL domains to build a target profile.
    """
    jd_text = jd_text.lower()
    discovered = []
    
    # Flatten all known skills from the master dictionary
    all_known = set()
    for s_list in SKILL_DICTIONARY.values():
        all_known.update(s_list)
        
    for skill in all_known:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_text):
            discovered.append(skill)
    return discovered

def get_missing_skills(found_skills, role, job_description=None):
    """
    Identify gaps by comparing found skills against either JD requirements or role baseline.
    """
    target_skills = []
    if job_description:
        target_skills = extract_jd_skills(job_description)
    
    # If JD is empty or yields no keywords, fallback to role dictionary
    if not target_skills:
        target_skills = SKILL_DICTIONARY.get(role, [])
        
    missing = [skill for skill in target_skills if skill not in found_skills]
    
    # Remove duplicates and return
    return sorted(list(set(missing)))[:8]
