import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 output encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ==========================================
# SYSTEM PARAMETERS
# ==========================================
LOCAL_OLLAMA_MODELS = ["llama3.2:3b", "qwen2.5-coder:7b"]
CLOUD_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
# ==========================================

def get_inbox():
    inbox = []
    try:
        with open("inputs.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            for idx, line in enumerate(lines, 1):
                inbox.append({"id": f"MSG-{idx:03d}", "text": line})
    except FileNotFoundError:
        print("❌ Could not find inputs.txt. Please create it with one prompt per line.")
        sys.exit(1)
    return inbox

def run_inbox_router():
    """
    Executes GLiNER2.5-Decide as a fast local AI router to route requests
    to specific parameterized models.
    """
    print("=" * 70)
    print("🚀 GLiNER2.5-Decide: I Replaced an LLM Router With a 340M AI")
    print("=" * 70)
    
    inbox = get_inbox()

    # GLiNER works via semantic span extraction. 
    router_schema = {
        "department": ["Billing", "Support", "Technical", "Security", "Sales", "Moderation", "Escalation"],
        "priority": ["Low", "Medium", "High", "Critical", "Urgent"],
        "task_complexity": ["Simple Request", "Coding Problem", "Complex Analysis", "Spam Message", "Human Intervention"]
    }

    results = []

    try:
        from gliner2 import AutoExtractor
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        print("⚠️ Required packages are missing. Run: `pip install gliner2 jinja2 python-dotenv`")
        return

    print("\n📦 Loading GLiNER2.5-Decide 340M AI Router...")
    model = AutoExtractor.from_pretrained("fastino/GLiNER2.5-Decide")
    print("✅ Router model loaded and ready in memory!\n")

    # Map the AI's semantic decision to our system's actual parameterized LLM architecture
    llm_mapping = {
        "Simple Request": LOCAL_OLLAMA_MODELS[0],
        "Coding Problem": LOCAL_OLLAMA_MODELS[1],
        "Complex Analysis": CLOUD_GEMINI_MODEL,
        "Spam Message": "Drop",
        "Human Intervention": "Human"
    }

    for msg in inbox:
        start_t = time.time()
        # The AI makes the full decision based on semantic intent
        decision = model.classify_text(msg["text"], router_schema)
        
        dept = decision.get("department", "Support").title()
        prio = decision.get("priority", "Medium").title()
        task_type = decision.get("task_complexity", "Simple Request")
        
        # Translate the AI's decision to our routing targets
        llm = llm_mapping.get(task_type, LOCAL_OLLAMA_MODELS[0])

        # Real local benchmark latency
        latency = (time.time() - start_t) * 1000

        results.append({
            "id": msg["id"],
            "text": msg["text"],
            "department": dept,
            "priority": prio,
            "target_llm": llm,
            "latency_ms": round(latency, 2)
        })

    # Terminal Output
    print(f"{'ID':<8} | {'Department':<12} | {'Priority':<10} | {'Target AI / Action':<25} | {'Latency'}")
    print("-" * 100)
    for r in results:
        print(f"{r['id']:<8} | {r['department']:<12} | {r['priority']:<10} | {r['target_llm']:<25} | {r['latency_ms']}ms")
    
    print("\n⚡ Note: 340M model -> Zero generated tokens -> Structured JSON -> Instant Automation.")

    # 3. Append outputs to Markdown File
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    
    md_path = out_dir / "outputs.md"
    
    # Create header if file doesn't exist
    if not md_path.exists():
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# 🚀 GLiNER2.5-Decide Router Logs\n\n")
            f.write("| ID | Department | Priority | Target AI / Action | Latency |\n")
            f.write("|---|---|---|---|---|\n")
            
    with open(md_path, "a", encoding="utf-8") as f:
        for r in results:
            f.write(f"| {r['id']} | `{r['department']}` | {r['priority']} | **{r['target_llm']}** | {r['latency_ms']}ms |\n")
    
    print(f"\n📝 Appended routing results to `{md_path}`")
    print("=" * 70)

if __name__ == "__main__":
    run_inbox_router()
