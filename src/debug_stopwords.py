from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re

print(f"Size of stop words: {len(ENGLISH_STOP_WORDS)}")
test_words = ['the', 'and', 'was', 'to', 'of', 'it', 'frustrated']

print("Testing individual words:")
for w in test_words:
    print(f"'{w}' in stop words? {w in ENGLISH_STOP_WORDS}")

print("\nTesting tokenization logic:")
text = "The user fell frustrated because of the error."
clean_text = re.sub(r'[^\w\s]', '', text.lower())
tokens = clean_text.split()
print(f"Tokens: {tokens}")
filtered = [t for t in tokens if t not in ENGLISH_STOP_WORDS]
print(f"Filtered: {filtered}")
