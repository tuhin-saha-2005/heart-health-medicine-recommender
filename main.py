import os
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Initialize Groq client (FREE API - fast and reliable!)
# Get your free API key from: https://console.groq.com
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def search_heart_condition(query: str) -> str:
    """Search for heart conditions and medicine recommendations"""
    retrieved_docs = retriever.invoke(query)
    results = []
    for doc in retrieved_docs:
        results.append(doc.page_content)
    return "\n\n".join(results)

def assess_emergency(query: str) -> bool:
    """Check if symptoms indicate emergency"""
    emergency_keywords = [
        "severe chest pain", "crushing pain", "cannot breathe", 
        "sudden", "intense", "radiating pain", "arm pain",
        "jaw pain", "severe shortness", "fainting", "heart attack"
    ]
    return any(keyword in query.lower() for keyword in emergency_keywords)

def get_medicine_recommendation(symptoms):
    """Get medicine recommendations based on symptoms using Groq API"""
    
    # Check for emergency first
    emergency_warning = None
    if assess_emergency(symptoms):
        emergency_warning = """⚠️ EMERGENCY ALERT ⚠️

Your symptoms may indicate a MEDICAL EMERGENCY!

IMMEDIATE ACTIONS:
1. CALL 911 or emergency services NOW
2. Chew 325mg Aspirin if available and not allergic
3. Sit down and stay calm
4. Do NOT drive yourself to hospital
5. Unlock your door for emergency responders

DO NOT DELAY - Call emergency services immediately!
"""
    
    # Search medical database
    context = search_heart_condition(symptoms)
    
    # Create prompt for recommendation
    prompt = f"""You are a knowledgeable cardiac medication advisor. Based on the medical information below, provide helpful recommendations.

Medical Knowledge Base:
{context}

Patient's Symptoms: {symptoms}

Provide a clear response with:
1. Possible heart condition
2. Recommended medications with dosages
3. Important precautions and side effects
4. When to seek medical care

Remember to remind the patient to consult a healthcare professional.

Response:"""
    
    # Call Groq API (using llama-3.3-70b for best quality)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable cardiac medication advisor who provides evidence-based recommendations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile",  # Latest and most powerful!
        temperature=0.3,  # Lower temperature for more consistent medical advice
        max_tokens=1000
    )
    
    response = chat_completion.choices[0].message.content
    return response, emergency_warning

def main():
    """Main chatbot loop for testing"""
    print("=" * 70)
    print(" 🪐 HEART HEALTH - MEDICINE RECOMMENDATION ASSISTANT")
    print("=" * 70)
    print(" Powered by Groq AI (FREE & FAST)")
    print("=" * 70)
    print("Describe your heart-related symptoms to get medicine recommendations.")
    print("Type 'exit' to quit.\n")
    
    print("-" * 70)
    
    while True:
        user_input = input("\n💬 Describe your symptoms: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye', 'stop']:
            print("\n❤️ Take care of your heart! Stay healthy. Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("\n🔍 Analyzing your symptoms...\n")
        
        try:
            response, emergency = get_medicine_recommendation(user_input)
            
            if emergency:
                print(emergency)
            
            print("\n" + "=" * 70)
            print(" 💊 RECOMMENDATION:")
            print("=" * 70)
            print(response)
            print("\n" + "=" * 70)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Make sure you have set GROQ_API_KEY environment variable.")
        
        print("-" * 70)

if __name__ == "__main__":
    main()