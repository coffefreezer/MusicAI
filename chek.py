try:
    from genai import Client
    print("הצלחנו! הספרייה הותקנה ומזוהה.")
except ImportError:
    print("עדיין יש בעיה בזיהוי הספרייה.")