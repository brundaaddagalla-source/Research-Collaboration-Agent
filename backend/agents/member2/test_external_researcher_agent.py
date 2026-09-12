# import sys
# import os

# sys.path.append(
#     os.path.abspath(
#         os.path.join(os.path.dirname(__file__), "../..")
#     )
# )

# from agents.member2.external_researcher_agent import ExternalResearcherAgent


# researcher = {
#     "name": "Researcher A",
#     "research_interests": [
#         "Artificial Intelligence",
#         "Machine Learning",
#         "Computer Vision"
#     ],
#     "skills": [
#         "Python",
#         "Deep Learning"
#     ]
# }


# candidates = [
#     {
#         "name": "Researcher B",
#         "research_interests": [
#             "Artificial Intelligence",
#             "Machine Learning",
#             "Computer Vision"
#         ],
#         "skills": [
#             "Python",
#             "Deep Learning"
#         ]
#     },
#     {
#         "name": "Researcher C",
#         "research_interests": [
#             "Agriculture",
#             "Biotechnology"
#         ],
#         "skills": [
#             "Python"
#         ]
#     },
#     {
#         "name": "Researcher D",
#         "research_interests": [
#             "Machine Learning",
#             "Computer Vision"
#         ],
#         "skills": [
#             "Python"
#         ]
#     }
# ]


# agent = ExternalResearcherAgent()

# result = agent.run(
#     researcher,
#     candidates
# )


# print("\n====================================")
# print("EXTERNAL RESEARCHER AGENT TEST")
# print("====================================")

# print("\nRANKED MATCHES:")

# for match in result["matches"]:
#     print(
#         match["candidate"]["name"],
#         "->",
#         match["match_score"]
#     )

# print("\nLLM EXPLANATION:")
# print(result["explanation"])

# print("====================================")

from agents.member2.external_researcher_agent import ExternalResearcherAgent


def main():

    researcher = {
        "name": "Researcher A",
        "research_interests": [
            "Artificial Intelligence",
            "Machine Learning",
            "Computer Vision"
        ],
        "skills": [
            "Python",
            "Deep Learning"
        ]
    }

    agent = ExternalResearcherAgent()

    result = agent.run(researcher)

    print("\n========================================")
    print("EXTERNAL RESEARCHER AGENT TEST")
    print("========================================")

    print("\nMATCHES:")
    for match in result["matches"]:
        print(match)

    print("\nLLM EXPLANATION:")
    print(result["explanation"])

    print("\n========================================")
    print("TEST COMPLETED")
    print("========================================")


if __name__ == "__main__":
    main()