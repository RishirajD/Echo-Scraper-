import json
import random
from functools import lru_cache

EXAMPLES_FILE = "prompt_examples.json"

@lru_cache()
def load_all_examples():
    with open(EXAMPLES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def load_examples(intent: str, max_examples: int = 10):
    all_examples = load_all_examples()
    filtered = [ex for ex in all_examples if intent.lower() in ex["intent"].lower()]
    
    # Avoid duplicates in fallback
    if len(filtered) < max_examples:
        remaining = [ex for ex in all_examples if ex not in filtered]
        filtered += random.sample(remaining, max(0, max_examples - len(filtered)))
    
    return filtered[:max_examples]

def infer_label_from_intent(intent: str) -> str:
    """
    Maps intent keywords to labels like 'Products', 'Cuisines', etc.
    """
    mapping = {
        "product": "Products",
        "cuisine": "Cuisines",
        "event": "Events",
        "course": "Courses",
        "job": "Job Listings",
        "testimonial": "Testimonials",
        "headline": "Headlines",
        "news": "Headlines",
        "blog": "Blog Titles",
        "menu": "Menu Items",
        "offer": "Offers",
        "price": "Prices"
    }
    for keyword, label in mapping.items():
        if keyword in intent.lower():
            return label
    return "Items"  # fallback

def infer_intent_from_html(html: str, url: str = "") -> str:
    """
    Suggests a parse description based on HTML content or URL.
    """
    # You can expand this with ML/NLP later.
    if "cuisine" in html.lower():
        return "List all available cuisines"
    elif "product" in html.lower() or "price" in html.lower():
        return "Extract product names and prices"
    elif "course" in html.lower():
        return "List all available courses"
    elif "event" in html.lower():
        return "List upcoming events"
    elif "job" in html.lower():
        return "Extract job listings"
    elif "menu" in html.lower():
        return "Extract food menu items"
    elif "offer" in html.lower():
        return "List available offers"
    elif "testimonial" in html.lower():
        return "Extract user testimonials"
    elif "blog" in html.lower() or "article" in html.lower():
        return "Extract blog titles or article names"
    elif "headline" in html.lower() or "news" in html.lower():
        return "Extract news headlines"
    return "Extract relevant information"

def get_prompt(dom_chunk: str, parse_description: str = None, url: str = ""):
    if not parse_description:
        parse_description = infer_intent_from_html(dom_chunk, url)
    examples = load_examples(parse_description)
    prompt = "You are a helpful AI assistant that extracts useful information from raw HTML.\n\n"

    for i, ex in enumerate(examples, 1):
        formatted_output = '\n'.join([f"{j+1}. {line}" for j, line in enumerate(ex["output"])])
        prompt += f"""---\nExample {i} ({ex['site'].capitalize()}):
🎯 Description:
{ex['intent']}

📥 HTML:
{ex['html']}

📤 {ex['label']}:
{formatted_output}\n"""
    
    inferred_label = infer_label_from_intent(parse_description)
    prompt += f"""\n---\nNow extract all relevant content from the HTML below.
🎯 Description: {parse_description}

📥 HTML:
{dom_chunk}

📤 {inferred_label}:"""
    return prompt
