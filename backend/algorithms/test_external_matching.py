from external_matching import (
    calculate_match_score,
    rank_candidates
)


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


candidates = [
    {
        "name": "Researcher B",
        "research_interests": [
            "Artificial Intelligence",
            "Machine Learning",
            "Computer Vision"
        ],
        "skills": [
            "Python",
            "Deep Learning"
        ]
    },
    {
        "name": "Researcher C",
        "research_interests": [
            "Agriculture",
            "Biotechnology"
        ],
        "skills": [
            "Python"
        ]
    },
    {
        "name": "Researcher D",
        "research_interests": [
            "Machine Learning",
            "Computer Vision"
        ],
        "skills": [
            "Python"
        ]
    }
]


results = rank_candidates(
    researcher,
    candidates
)


print("\n==============================")
print("RESEARCH MATCHING TEST")
print("==============================")

for result in results:

    print(
        result["candidate"]["name"],
        "->",
        result["match_score"]
    )

print("==============================")