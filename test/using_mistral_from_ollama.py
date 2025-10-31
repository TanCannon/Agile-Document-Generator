import ollama

def run_prompt(prompt, model="mistral"):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    
    if 'message' in response and 'content' in response['message']:
        return response['message']['content'].strip()
    return "No answer"

# File paths
input_file = "questions.csv"    # Should have a header "question"
output_file = "questions_with_answers.csv"

# Read questions (skip header)
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.read().strip().split("\n")

# header = lines[0]             # First row header
questions = lines[1:]           # Remaining rows are questions

# Prepare output with header
output_lines = ["question,answer"]

for q in questions:
    q = q.strip()
    if not q:
        continue
    try:
        answer = run_prompt(q)
    except Exception as e:
        answer = f"Error: {e}"

    # Escape any commas in the text to keep CSV valid
    q_escaped = f'"{q}"' if ',' in q else q
    ans_escaped = f'"{answer}"' if ',' in answer else answer

    output_lines.append(f"{q_escaped},{ans_escaped}")
    print(f"Q: {q}\nA: {answer}\n{'-'*50}")

# Save to output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Finished! Answers saved to {output_file}")
