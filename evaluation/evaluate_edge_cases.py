import json

from src.agents.graph import graph


# --------------------------------------------------
# Load Tests
# --------------------------------------------------

with open(
    "evaluation/edge_case_tests.json",
    "r",
    encoding="utf-8"
) as file:
    tests = json.load(file)


# --------------------------------------------------
# Counters
# --------------------------------------------------

passed = 0
failed = 0


# --------------------------------------------------
# Run Tests
# --------------------------------------------------

print("\n" + "=" * 60)
print("SUPPORTCOPILOT EDGE-CASE EVALUATION")
print("=" * 60)


for number, test in enumerate(tests, start=1):

    question = test["question"]
    expected_intent = test["expected_intent"]

    try:

        result = graph.invoke({
            "message": question,
            "response": "",
            "intent": "",
            "tool_result": {},
            "tool_used": "",
            "context": []
        })

        actual_intent = result["intent"]
        response = result["response"]

        # --------------------------------------------------
        # Intent Check
        # --------------------------------------------------

        intent_passed = (
            actual_intent == expected_intent
        )

        # --------------------------------------------------
        # Keyword Check
        # --------------------------------------------------

        keyword_passed = True

        if "expected_keywords" in test:

            response_lower = response.lower()

            # At least ONE acceptable phrase
            # must appear in the response.
            keyword_passed = any(
                keyword.lower() in response_lower
                for keyword in test["expected_keywords"]
            )

        # --------------------------------------------------
        # Final Result
        # --------------------------------------------------

        test_passed = (
            intent_passed
            and keyword_passed
        )

        if test_passed:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        print("\n" + "-" * 60)
        print(f"Test {number}: {status}")
        print("Question:", question)
        print("Expected intent:", expected_intent)
        print("Actual intent:", actual_intent)

        if "expected_keywords" in test:
            print(
                "Expected keywords:",
                test["expected_keywords"]
            )

        if not test_passed:
            print("Actual response:", response)

    except Exception as error:

        failed += 1

        print("\n" + "-" * 60)
        print(f"Test {number}: FAIL")
        print("Question:", question)
        print("ERROR:", str(error))


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
print("EDGE-CASE EVALUATION SUMMARY")
print("=" * 60)

print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print(f"Edge-Case Accuracy: {accuracy:.2f}%")