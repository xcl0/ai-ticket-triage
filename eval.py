from main import triage_ticket

test_cases = [
    {
        "ticket": "Entire website unavailable for all users", 
        "expected_category": "technical",
         "expected_priority": "critical",
         "expected_assigned": "technical_support"
    },

    {
        "ticket": "Customer asking about subscription pricing",
        "expected_category": "billing",
        "expected_priority": "low",
        "expected_assigned": "billing_support"
    },

    {
        "ticket": "One customer unable to log in, with no workaround",
        "expected_category": "account",
        "expected_priority": "high",
        "expected_assigned": "account_support"
    }
]

total = len(test_cases)
correct_category_count = 0
correct_priority_count = 0
correct_assigned_count = 0

for test_case in test_cases:
    result = triage_ticket(test_case["ticket"])

    correct_category = result.category == test_case["expected_category"]
    correct_priority = result.priority == test_case["expected_priority"]
    correct_assigned = result.assigned_team == test_case["expected_assigned"]

    if correct_category:
        correct_category_count +=1

    if correct_priority:
        correct_priority_count +=1

    if correct_assigned:
        correct_assigned_count +=1

category_accuracy = correct_category_count/total*100
priority_accuracy = correct_priority_count/total*100
assigned_accuracy = correct_assigned_count/total*100

print(f"category accuracy: {category_accuracy}%")
print(f"priority accuracy: {priority_accuracy}%")


