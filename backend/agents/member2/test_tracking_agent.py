from agents.member2.tracking_agent import TrackingAgent


def main():

    print("=" * 60)
    print("COLLABORATION TRACKING AGENT TEST")
    print("=" * 60)

    agent = TrackingAgent()

    records = agent.get_tracking_records()

    print(f"\nTotal tracking records: {len(records)}")

    for record in records:

        print("\n----------------------------------------")

        print("Faculty A:", record["faculty_a"])
        print("Faculty B:", record["faculty_b"])
        print(
            "External Researcher ID:",
            record["external_researcher_id"]
        )
        print(
            "External Institution:",
            record["external_institution"]
        )
        print("Topic:", record["topic"])
        print("Current Stage:", record["current_stage"])
        print("Last Updated:", record["last_updated"])

    result = agent.run()

    print("\n========================================")
    print("TRACKING SUMMARY")
    print("========================================")

    print(
        "Total:",
        result["total_collaborations"]
    )

    print(
        "Internal:",
        len(result["internal_collaborations"])
    )

    print(
        "External:",
        len(result["external_collaborations"])
    )

    print(
        "Stage Summary:",
        result["stage_summary"]
    )

    print("\nTRACKING AGENT TEST PASSED")


if __name__ == "__main__":
    main()