from dotenv import load_dotenv
from graph import run_pipeline

load_dotenv()

def display_result(result):
    confidence_colors = {"high": "✅", "medium": "⚠️", "low": "❌"}
    indicator = confidence_colors.get(result.confidence, "❓")

    print("\n" + "═" * 50)
    print("RESEARCH RESULT")
    print("═" * 50)
    print(f"\nTopic      : {result.topic}")
    print(f"\nSummary    :\n{result.verified_summary}")
    print(f"\nKey Points :")
    for point in result.key_points:
        print(f"  • {point}")
    if result.flagged_claims:
        print(f"\nFlagged Claims ⚠️ :")
        for claim in result.flagged_claims:
            print(f"  • {claim}")
    print(f"\nConfidence : {indicator} {result.confidence.upper()}")
    print(f"\nSources    : {', '.join(result.sources)}")
    print("\n" + "═" * 50)

if __name__ == "__main__":
    query = input("What do you want to research? ")
    result = run_pipeline(query)
    display_result(result)