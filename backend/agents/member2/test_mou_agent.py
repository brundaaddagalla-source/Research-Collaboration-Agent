from agents.member2.mou_agent import MoUAgent


def main():

    print("=" * 60)
    print("MoU INTELLIGENCE AGENT TEST")
    print("=" * 60)

    agent = MoUAgent()

    mous = agent.get_mous()

    print(f"\nTotal MoUs: {len(mous)}")

    for mou in mous:

        print("\n----------------------------------------")

        print("Institution:", mou["institution"])
        print("Country:", mou["country"])
        print("Research Area:", mou["research_area"])
        print("Status:", mou["status"])
        print(
            "Joint Publications:",
            mou["joint_publications"]
        )
        print(
            "Joint Projects:",
            mou["joint_projects"]
        )

    result = agent.run()

    print("\n========================================")
    print("MoU SUMMARY")
    print("========================================")

    print(
        "Total:",
        result["total_mous"]
    )

    print(
        "Active:",
        len(result["active_mous"])
    )

    print(
        "Underutilized:",
        len(result["underutilized_mous"])
    )

    print(
        "Dormant:",
        len(result["dormant_mous"])
    )

    print("\nMoU AGENT TEST PASSED")


if __name__ == "__main__":
    main()