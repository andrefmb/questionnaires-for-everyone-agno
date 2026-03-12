import sys
import os
import time

# Ensure we use the venv
sys.path.append(os.path.join(os.getcwd(), 'venv/lib/python3.13/site-packages'))

from translation_utils import translate_statements, warm_up

def test_optimization():
    print("--- Optimized Argos Test ---")
    
    # 1. Warm up
    start = time.time()
    warm_up('en', 'pt')
    print(f"Warm-up took: {time.time() - start:.2f}s")
    
    # 2. First translation (should be faster now)
    source_texts = ["Hello world.", "This is a performance test."]
    print("\nTranslating first batch...")
    start = time.time()
    res1 = translate_statements(source_texts, 'en', 'pt')
    print(f"First batch took: {time.time() - start:.2f}s")
    for s, t in zip(source_texts, res1):
        print(f"  {s} -> {t}")
        
    # 3. Second translation (should be very fast)
    print("\nTranslating second batch...")
    start = time.time()
    res2 = translate_statements(["The sun is shining today."], 'en', 'pt')
    print(f"Second batch took: {time.time() - start:.2f}s")
    print(f"  Result: {res2[0]}")

if __name__ == "__main__":
    test_optimization()
