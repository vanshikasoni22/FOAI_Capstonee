from core.llm import generate_response

def classify_intent(query):
    system_prompt = (
        "Classify the student's query into exactly one of these categories: "
        "admissions_info, fees_info, hostel_info, academics_info, events_info, "
        "contacts_info, ambiguous, unknown. "
        "Reply with ONLY the category label, nothing else."
    )
    
    label = generate_response(system_prompt, query)
    
    # Sanitize label (sometimes LLM adds extra text or quotes)
    valid_intents = [
        "admissions_info", "fees_info", "hostel_info", "academics_info", 
        "events_info", "contacts_info", "ambiguous", "unknown"
    ]
    
    label_clean = label.strip().lower().replace('"', '').replace("'", "")
    for intent in valid_intents:
        if intent in label_clean:
            return intent
            
    return "unknown"
