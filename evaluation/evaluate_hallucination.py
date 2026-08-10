import json

from src.agents.graph import graph


# --------------------------------------------------
# Load Tests
# --------------------------------------------------

with open(
    "evaluation/hallucination_tests.json",
    "r",
    encoding="utf-8"
) as file:
    tests = json.load(file)


# --------------------------------------------------
# Expected Refusal Phrases
# --------------------------------------------------

refusal_phrases = [
    "not enough information",
    "do not have enough information",
    "don't have enough information",
    "does not contain",
    "does not mention",
    "recommend contacting",
    "contact novacart support"
]


# --------------------------------------------------
# Run Tests
# --------------------------------------------------

passed = 0
failed = 0


print("\n" + "=" * 60)
print("SUPPORTCOPILOT HALLUCINATION EVALUATION")
print("=" * 60)


for number, test in enumerate(tests, start=1):

    question = test["question"]

    result = graph.invoke({
        "message": question,
        "response": "",
        "intent": "",
        "tool_result": {},
        "tool_used": "",
        "context": []
    })

    response = result["response"].lower()

    # Check whether the response contains
    # a refusal / insufficient-information signal
    refused = any(
        phrase in response
        for phrase in refusal_phrases
    )

    if refused:
        passed += 1
        status = "PASS"
    else:
        failed += 1
        status = "FAIL"

    print("\n" + "-" * 60)
    print(f"Test {number}: {status}")
    print("Question:", question)
    print("Response:", result["response"])


# --------------------------------------------------
# Summary
# --------------------------------------------------

total = len(tests)

accuracy = (
    passed / total * 100
    if total > 0
    else 0
)


print("\n" + "=" * 60)
print("HALLUCINATION EVALUATION SUMMARY")
print("=" * 60)

print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print(f"Hallucination Safety Accuracy: {accuracy:.2f}%")