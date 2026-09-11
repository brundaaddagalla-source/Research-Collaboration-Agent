from llm_service import LLMService


def main():
    llm = LLMService()

    response = llm.generate(
        "Reply with exactly: LLM service is working."
    )

    print("\n========================================")
    print("LLM SERVICE TEST")
    print("========================================")
    print(response)
    print("========================================")


if __name__ == "__main__":
    main()