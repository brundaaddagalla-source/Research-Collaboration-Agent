from algorithms.funding_agent.funding_agent import FundingAgent


def main():

    print("=" * 60)
    print("FUNDING AGENT TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Sample research project
    # ---------------------------------------------------------

    project = {
        "research_area": "Artificial Intelligence and Machine Learning",
        "project_title": "AI Based Poultry Disease Detection",
        "project_description": (
            "A research project using artificial intelligence, "
            "machine learning, computer vision, and data analysis "
            "to detect poultry diseases at an early stage."
        ),
        "researcher_type": "Student",
        "research_stage": "Early Stage",
        "required_amount": 500000
    }

    print("\n[1] Project created")
    print(f"Title: {project['project_title']}")
    print(f"Research Area: {project['research_area']}")
    print(f"Required Amount: ₹{project['required_amount']:,}")

    # ---------------------------------------------------------
    # 2. Initialize Funding Agent
    # ---------------------------------------------------------

    print("\n[2] Initializing Funding Agent...")

    try:
        agent = FundingAgent()
        print("SUCCESS: FundingAgent initialized.")

    except Exception as e:
        print("FAILED: Could not initialize FundingAgent.")
        print(f"Error: {e}")
        return

    # ---------------------------------------------------------
    # 3. Find funding
    # ---------------------------------------------------------

    print("\n[3] Finding funding opportunities...")

    try:
        results = agent.find_funding(project)

    except Exception as e:
        print("FAILED: Funding search failed.")
        print(f"Error: {e}")
        return

    # ---------------------------------------------------------
    # 4. Validate results
    # ---------------------------------------------------------

    print("\n[4] Validating results...")

    if not isinstance(results, list):
        print("FAILED: Result is not a list.")
        return

    print(f"SUCCESS: Received {len(results)} matches.")

    if len(results) > 5:
        print("FAILED: More than 5 results returned.")
        return

    print("SUCCESS: Top-5 limit is working.")

    # ---------------------------------------------------------
    # 5. Display matches
    # ---------------------------------------------------------

    print("\n[5] FUNDING MATCHES")
    print("-" * 60)

    if not results:
        print("No funding opportunities matched.")
        return

    for index, result in enumerate(results, start=1):

        funding = result["funding"]
        score = result["score"]

        print(f"\n#{index}")
        print(f"Funding: {funding.get('name', 'Unknown')}")
        print(f"Score: {score}")

        explanation = result.get("explanation")

        if not explanation:
            print("FAILED: Missing LLM explanation.")
            return

        print("LLM Explanation:")
        print(explanation)

    # ---------------------------------------------------------
    # 6. Verify sorting
    # ---------------------------------------------------------

    scores = [result["score"] for result in results]

    if scores != sorted(scores, reverse=True):
        print("\nFAILED: Results are not sorted correctly.")
        return

    print("\nSUCCESS: Results sorted highest → lowest.")

    # ---------------------------------------------------------
    # 7. Verify result structure and LLM integration
    # ---------------------------------------------------------

    for result in results:

        if "funding" not in result:
            print("FAILED: Missing 'funding' field.")
            return

        if "score" not in result:
            print("FAILED: Missing 'score' field.")
            return

        if "explanation" not in result:
            print("FAILED: Missing 'explanation' field.")
            return

        if not isinstance(result["explanation"], str):
            print("FAILED: LLM explanation is not a string.")
            return

        if not result["explanation"].strip():
            print("FAILED: LLM explanation is empty.")
            return

    print("SUCCESS: Result structure is valid.")
    print("SUCCESS: LLM explanations generated.")
    # ---------------------------------------------------------
    # Final
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("FUNDING AGENT TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()