from modules.whisper_steward import intake_ritual_scroll

# Test the intake function
result = intake_ritual_scroll('rituals/request_expense.breathe')
print("Successfully parsed ritual scroll:")
print(result)
