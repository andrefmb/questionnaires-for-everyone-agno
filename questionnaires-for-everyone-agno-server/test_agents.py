import os
import sys

# Add current directory to path so we can import our modules
sys.path.append(os.getcwd())

try:
    from agents import gemba_agent, ssa_agent
    from config import settings
    print(f"--- Configuration ---")
    print(f"LLM_PROVIDER: {settings.LLM_PROVIDER}")
    print(f"GOOGLE_API_KEY: {'Configured' if settings.GOOGLE_API_KEY else 'NOT Configured'}")
    print(f"OPENAI_API_KEY: {'Configured' if settings.OPENAI_API_KEY or settings.OPENAI_AUTH_KEY else 'NOT Configured'}")
    print(f"---------------------\n")

    # test inputs
    source_items = ["Hello, how are you?"]
    translated_items = ["Olá, como vai você?"]
    src_lang = "English"
    tgt_lang = "Portuguese"

    print("Testing GEMBA Agent...")
    # Mocking a run if keys are not present to at least verify initialization
    if (settings.LLM_PROVIDER == "google" and not settings.GOOGLE_API_KEY) or \
       (settings.LLM_PROVIDER == "openai" and not (settings.OPENAI_API_KEY or settings.OPENAI_AUTH_KEY)):
        print("Skipping live test: API key missing for configured provider.")
    else:
        from evaluation_utils import evaluate_gemba, evaluate_ssa
        
        gemba_res = evaluate_gemba(source_items, translated_items, src_lang, tgt_lang, 'single')
        print(f"GEMBA Result: {gemba_res}")

        print("\nTesting SSA Agent...")
        ssa_res = evaluate_ssa(source_items, translated_items, src_lang, tgt_lang, 'single')
        print(f"SSA Result: {ssa_res}")

except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
