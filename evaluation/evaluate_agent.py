import json

from src.agents.graph import graph


# --------------------------------------------------
# Load Test Cases
# --------------------------------------------------

with open("evaluation/test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)


# --------------------------------------------------
# Counters
# --------------------------------------------------

passed = 0
failed = 0

intent_correct = 0
intent_wrong = 0

tool_correct = 0
tool_wrong = 0

rag_correct = 0
rag_wrong = 0

answer_correct = 0
answer_wrong = 0


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

print("\n" + "=" * 60)
print("SUPPORTCOPILOT EVALUATION")
print("=" * 60)


for number, test in enumerate(test_cases, start=1):

    question = test["question"]
    expected_intent = test["expected_intent"]

    result = graph.invoke({
        "message": question,
        "response": "",
        "intent": "",
        "tool_result": {},
        "tool_used": "",
        "context": []
    })

    actual_intent = result["intent"]
    actual_tool = result.get("tool_used", "")
    response = result["response"]

    # --------------------------------------------------
    # Intent Check
    # --------------------------------------------------

    intent_passed = actual_intent == expected_intent

    if intent_passed:
        intent_correct += 1
    else:
        intent_wrong += 1

    # --------------------------------------------------
    # Tool Check
    # --------------------------------------------------

    tool_passed = True

    if "expected_tool" in test:

        tool_passed = (
            actual_tool == test["expected_tool"]
        )

        if tool_passed:
            tool_correct += 1
        else:
            tool_wrong += 1

    # --------------------------------------------------
    # RAG Source Check
    # --------------------------------------------------

    source_passed = True

    if "expected_source" in test:

        expected_source = test["expected_source"]

        sources = [
            item["source"]
            for item in result.get("context", [])
        ]

        source_passed = expected_source in sources

        if source_passed:
            rag_correct += 1
        else:
            rag_wrong += 1

    # --------------------------------------------------
    # Answer Quality Check
    # --------------------------------------------------

    answer_passed = True

    if "expected_keywords" in test:

        response_lower = response.lower()

        # At least ONE acceptable phrase/keyword
        # must appear in the response.
        answer_passed = any(
            keyword.lower() in response_lower
            for keyword in test["expected_keywords"]
        )

        if answer_passed:
            answer_correct += 1
        else:
            answer_wrong += 1

    # --------------------------------------------------
    # Final Test Result
    # --------------------------------------------------

    test_passed = (
        intent_passed
        and tool_passed
        and source_passed
        and answer_passed
    )

    if test_passed:
        passed += 1
        status = "PASS"
    else:
        failed += 1
        status = "FAIL"

    # --------------------------------------------------
    # Print Test
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print(f"Test {number}: {status}")
    print("Question:", question)
    print("Expected intent:", expected_intent)
    print("Actual intent:", actual_intent)

    if "expected_tool" in test:
        print("Expected tool:", test["expected_tool"])
        print("Actual tool:", actual_tool)

    if "expected_source" in test:
        print("Expected source:", test["expected_source"])

    if "expected_keywords" in test:
        print(
            "Expected keywords:",
            test["expected_keywords"]
        )

    if not test_passed:
        print("Actual response:", response)


# --------------------------------------------------
# Metrics
# --------------------------------------------------

total = len(test_cases)

overall_accuracy = (
    passed / total * 100
    if total > 0
    else 0
)

intent_accuracy = (
    intent_correct / total * 100
    if total > 0
    else 0
)

tool_tests = tool_correct + tool_wrong

tool_accuracy = (
    tool_correct / tool_tests * 100
    if tool_tests > 0
    else 100
)

rag_tests = rag_correct + rag_wrong

rag_accuracy = (
    rag_correct / rag_tests * 100
    if rag_tests > 0
    else 100
)

answer_accuracy = (
    answer_correct / total * 100
    if total > 0
    else 0
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("EVALUATION SUMMARY")
print("=" * 60)

print("Total tests:", total)
print("Passed:", passed)
print("Failed:", failed)

print("\nIntent Routing:")
print("Correct:", intent_correct)
print("Wrong:", intent_wrong)
print(f"Intent Accuracy: {intent_accuracy:.2f}%")

print("\nTool Selection:")
print("Correct:", tool_correct)
print("Wrong:", tool_wrong)
print(f"Tool Accuracy: {tool_accuracy:.2f}%")

print("\nRAG Retrieval:")
print("Correct:", rag_correct)
print("Wrong:", rag_wrong)
print(f"RAG Retrieval Accuracy: {rag_accuracy:.2f}%")

print("\nAnswer Quality:")
print("Correct:", answer_correct)
print("Wrong:", answer_wrong)
print(f"Answer Accuracy: {answer_accuracy:.2f}%")

print("\nOverall Accuracy:")
print(f"{overall_accuracy:.2f}%")