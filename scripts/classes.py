from google import genai
import os

class GeminiQnAProcessor:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """Initialize Gemini client and model."""
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def read_questions(self, input_file: str) -> list[str]:
        """Read questions from a file (skipping the header)."""
        with open(input_file, "r", encoding="utf-8") as f:
            # lines = f.read().strip().split("\n") #uncomment to pass each line as a invidual prompt
            next(f) # skipping 1st line 
            lines = f.read().strip()
        # return [line.strip() for line in lines[1:] if line.strip()] #uncomment to pass each line as a invidual prompt
        return [lines]

    def get_answer(self, question: str) -> str:
        """Send a question to the Gemini model and return the answer."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=question
            )
            return response.text.strip() if hasattr(response, "text") else "No answer"
        except Exception as e:
            return f"Error: {e}"

    def process_questions(self, questions: list[str]) -> list[tuple[str, str]]:
        """Process a list of questions and return (question, answer) pairs."""
        results = []
        for q in questions:
            answer = self.get_answer(q)
            
            # results.append((q, answer))
            results.append(answer)
            print(f"Q: {q}\nA: {answer}\n{'-'*50}")
        return results

    def write_results(self, results: list, output_file1: str) -> None:
        """Write questions and answers to a CSV file."""
        # lines = ["question,answer"] #uncomment to add header ("question,answer") to answer file
        lines = []
        for a in results:
            #q_escaped = f'"{q}"' if ',' in q else q
            #a_escaped = f'"{a}"' if ',' in a else a
            #lines.append(f"{q_escaped},{a_escaped}")
            lines.append(a)
        with open(output_file1, "w", encoding="utf-8") as f1:
            f1.write("\n".join(lines))
        print(f"Finished! Answers saved to {output_file1}")

    def append_result(self, input_file: str, output_file: str) -> None:
        with open(input_file, "r", encoding="utf-8") as source_file:
            # Read the content of the source file
            file_content = source_file.read()
        with open(output_file, "a", encoding="utf-8") as destination_file:
            # Write the content to the destination file
            destination_file.write(file_content)
        
        print(f"Contents of '{input_file}' copied to '{output_file}' successfully.")
    
    def reset_prompts(self, input_file: str, output_file: str) -> None:
        with open(input_file, "r", encoding="utf-8") as source_file:
            # Read the content of the source file
            file_content = source_file.read()
        with open(output_file, "w", encoding="utf-8") as destination_file:
            # Write the content to the destination file
            destination_file.write(file_content)
        
        print(f"Contents of '{input_file}' overwrite to '{output_file}' successfully.")

    def run_stream_to_file(self, input_file: str, output_file: str) -> None:
        """Stream answers and save directly to a file (no big in-memory strings)."""
        run_status = True
        questions = self.read_questions(input_file)
        with open(output_file, "w", encoding="utf-8") as f:
            for q in questions:
                # f.write(f"Q: {q}\nA: ")
                # print(f"Q: {q}\nA: ", end="", flush=True)

                try:
                    stream = self.client.models.generate_content_stream(
                        model=self.model,
                        contents=[q]
                    )
                    for chunk in stream:
                        # each chunk may have text or finish info
                        if chunk.text:
                            f.write(chunk.text)
                            f.flush()
                            # print(chunk.text, end="", flush=True)

                        # check finish reason (optional, helps debug cutoffs)
                        if hasattr(chunk, "candidates") and chunk.candidates:
                            finish_reason = chunk.candidates[0].finish_reason
                            if finish_reason and finish_reason != "STOP":
                                f.write(f"\n[Warning: generation stopped early, reason={finish_reason}]\n")
                                print(f"\n[Warning: generation stopped early, reason={finish_reason}]\n")
                                run_status = False

                except Exception as e:
                    f.write(f"\nError: {e}\n")
                    print(f"\nError: {e}")
                    run_status = False
        return run_status

    def run(self, input_file: str, output_file: str) -> None:
        """Full processing pipeline."""
        questions = self.read_questions(input_file)
        results = self.process_questions(questions)
        self.write_results(results, output_file)

        # print(f"Finished! Answers saved to {output_file}")