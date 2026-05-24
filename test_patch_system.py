from core.patches.safe_writer import SafeWriter

writer = SafeWriter(root=".")

result = writer.propose_write(
    "demo_test.txt",
    "Hello from safe Jarvis patch system\n",
    "Testing confirm-before-write mode"
)

print("PROPOSAL ID:", result["proposal"]["id"])
print(result["diff"])

proposal_id = result["proposal"]["id"]

print(writer.apply_proposal(proposal_id, confirm=True))
print(writer.rollback_proposal(proposal_id))