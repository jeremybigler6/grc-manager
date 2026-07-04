from openai import OpenAI

client = OpenAI()


def analyze_scenario(scenario):
    prompt = f"""
You are a cybersecurity GRC analyst.

Analyze this scenario:

{scenario}

Return the answer in this format:

Potential Risks:
- 

Recommended Controls:
- 

Framework Mapping:
- 

Suggested Risk Register Entry:
Risk Name:
Category:
Likelihood:
Impact:
Risk Score:
Risk Level:
Treatment Plan:
Status:
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text


def main():
    print("AI Risk & Control Advisor")

    scenario = input("\nDescribe the business or cybersecurity scenario: ")

    result = analyze_scenario(scenario)

    print("\n========== AI Analysis ==========")
    print(result)


if __name__ == "__main__":
    main()