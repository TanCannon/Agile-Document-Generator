from google import genai
from settings import settings

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
    # def write_results(self, results: list, output_file1: str, output_file2: str = "input_prompt_sprint_plan.csv") -> None:
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
        
        #append the result in output_file2 (input_prompt_sprint_plan.csv)
        # with open(output_file2, "a", encoding="utf-8") as f2:
        #     f2.write("\n".join(lines))
        # print(f"Appended! {output_file1} into {output_file2} ")
    
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

    def run(self, input_file: str, output_file: str) -> None:
        """Full processing pipeline."""
        questions = self.read_questions(input_file)
        results = self.process_questions(questions)
        self.write_results(results, output_file)
        # print(f"Finished! Answers saved to {output_file}")


if __name__ == "__main__":
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    #preparing user_stories
    print("Preparing! user_stories...")
    processor.run(settings.input_file, settings.output_file)
    print("Finished! user_stories")

    processor.append_result(settings.output_file, "./prompts/questions4.csv")

    # preparing sprint_plan
    print("Preparing! sprint_plan...")
    processor.run( "./prompts/questions4.csv", "./prompts/answers4.csv") 
    print("Finished! sprint_plan")


    processor.append_result( "./prompts/answers4.csv", "./prompts/questions5.csv")

    # preparing gant_chart
    print("Preparing! gant_chart...")
    processor.run( "./prompts/questions5.csv", "./prompts/answers5.csv") 
    print("Finished! gant_chart")

    # reset prompts by overwriting
    print("Resettting! all prompts...")
    processor.reset_prompts( "./prompts/Resetquestions1.csv", "./prompts/questions4.csv")
    processor.reset_prompts( "./prompts/Resetquestions2.csv", "./prompts/questions5.csv")
    print("Resettting! Finished!")
