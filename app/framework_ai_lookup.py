from openai import OpenAI

client = OpenAI()


def explain_framework_control(framework, control_id):
    prompt = f"""
You are a cybersecurity GRC analyst.

Explain this framework control in plain English:

Framework: {framework}
Control ID: {control_id}

Return the answer in this format:

Control Summary:
-

What It Means:
-

Why It Matters:
-

Implementation Steps:
1.
2.
3.
4.
5.

Evidence To Keep:
-

Common Mistakes:
-

Beginner-Friendly Explanation:
-
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text


def main():
    print("AI Framework Control Lookup")

    framework = input("\nFramework name: ")
    control_id = input("Control ID: ")

    result = explain_framework_control(framework, control_id)

    print("\n========== Framework Control Explanation ==========")
    print(result)


if __name__ == "__main__":
    main()