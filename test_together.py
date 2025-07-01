from models.together_client import generate_manual

prompt = """
Generate a step-by-step user manual for installing a home Wi-Fi router. 
Use simple language for beginners.
"""

result = generate_manual(prompt)
print(result)
