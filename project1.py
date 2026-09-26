import random
import re

print("==============================================")
print("Project 1: Attribute-Based Access Control")
print("==============================================")

n = int(input("Enter the number of attributes: "))

if n < 2:
    print("You must enter at least 2 attributes.")
    exit()

attributes = []

for i in range(n):
    attribute = input("Enter attribute " + str(i + 1) + ": ")
    attributes.append(attribute)

print("\nAttributes in the system:")
print(attributes)

users = {}

for i in range(10):
    number_of_attributes = random.randint(2, n)
    users[i + 1] = random.sample(attributes, number_of_attributes)

print("\n==============================================")
print("10 Randomly Generated Users")
print("==============================================")

for user_number in users:
    print("User", user_number, ":", users[user_number])

print("\n==============================================")
print("Access Control Policy")
print("==============================================")

print("Example 1:")
print("(student AND staff) OR (write AND execute)")

print("\nExample 2:")
print("(student AND staff) OR (2 of (write, execute, read))")

policy = input("\nEnter the access control policy: ")

if "and" in policy or "or" in policy:
    print("\nERROR: AND and OR must be uppercase.")
    exit()


def evaluate_two_of(attribute_text, user_attributes):
    parts = attribute_text.split(",")
    count = 0

    for attribute in parts:
        attribute = attribute.strip()

        if attribute in user_attributes:
            count += 1

    return count >= 2


def evaluate_policy(policy, user_attributes):
    two_of_pattern = r"2\s+of\s*\(([^()]*)\)"

    while re.search(two_of_pattern, policy):
        match = re.search(two_of_pattern, policy)
        attributes_inside = match.group(1)

        result = evaluate_two_of(
            attributes_inside,
            user_attributes
        )

        if result:
            policy = policy[:match.start()] + "True" + policy[match.end():]
        else:
            policy = policy[:match.start()] + "False" + policy[match.end():]

    for attribute in attributes:
        if attribute in user_attributes:
            policy = re.sub(
                r"\b" + re.escape(attribute) + r"\b",
                "True",
                policy
            )
        else:
            policy = re.sub(
                r"\b" + re.escape(attribute) + r"\b",
                "False",
                policy
            )

    policy = policy.replace("AND", "and")
    policy = policy.replace("OR", "or")

    try:
        return bool(eval(policy))
    except:
        return None


print("\n==============================================")
print("User Access Evaluation")
print("==============================================")

while True:
    user_number = input(
        "\nEnter the user number to evaluate (1-10), or Q to quit: "
    )

    if user_number.upper() == "Q":
        break

    if not user_number.isdigit():
        print("Invalid input. Please enter a number from 1 to 10.")
        continue

    user_number = int(user_number)

    if user_number not in users:
        print("Invalid user number. Please enter a number from 1 to 10.")
        continue

    print("\nUser", user_number, "attributes:")
    print(users[user_number])

    result = evaluate_policy(policy, users[user_number])

    if result is True:
        print("\nTRUE - Access Granted")
    elif result is False:
        print("\nFALSE - Access Denied")
    else:
        print("\nInvalid access control policy.")

print("\nProgram ended.")