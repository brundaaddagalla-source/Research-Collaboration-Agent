from agents.member2.impact_agent import ImpactAgent


def main():
    agent = ImpactAgent()

    result = agent.run()

    print("\n=== COLLABORATION IMPACT ===")

    print(
        "Total collaborations:",
        result["total_collaborations"]
    )

    print(
        "Internal collaborations:",
        result["internal_collaborations"]
    )

    print(
        "External collaborations:",
        result["external_collaborations"]
    )

    print(
        "Funded projects:",
        result["funded_projects"]
    )

    print("\n=== MoU IMPACT ===")

    print(
        "Total MoUs:",
        result["total_mous"]
    )

    print(
        "Active MoUs:",
        result["active_mous"]
    )

    print(
        "Underutilized MoUs:",
        result["underutilized_mous"]
    )

    print(
        "Dormant MoUs:",
        result["dormant_mous"]
    )

    print(
        "Joint publications:",
        result["total_joint_publications"]
    )

    print(
        "Joint projects:",
        result["total_joint_projects"]
    )

    print("\n=== STAGE SUMMARY ===")

    for stage, count in result["stage_summary"].items():
        print(f"{stage}: {count}")

    # Basic validation
    assert result["total_collaborations"] >= 0
    assert result["internal_collaborations"] >= 0
    assert result["external_collaborations"] >= 0
    assert result["total_mous"] >= 0

    print("\nIMPACT AGENT TEST PASSED")


if __name__ == "__main__":
    main()