from google import genai
from settings import settings

# Initialize Gemini client
client = genai.Client(api_key = settings.api_key)

# File paths
input_file = "questions.csv"   # Should contain one question per line after header
output_file = "questions_with_answers.csv"

# Read questions (skip header)
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.read().strip().split("\n")

# First line is header
# header = lines[0]
questions = lines[1:]  # All remaining lines are questions

# Output data (add header)
output_lines = ["question,answer"]

for q in questions:
    q = q.strip()
    if not q:
        continue  # Skip empty lines
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=q
        )
        answer = response.text.strip() if hasattr(response, "text") else "No answer"
    except Exception as e:
        answer = f"Error: {e}"

    output_lines.append(f"{q},{answer}")
    print(f"Q: {q}\nA: {answer}\n{'-'*50}")

# Write output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Finished! Answers saved to {output_file}")
