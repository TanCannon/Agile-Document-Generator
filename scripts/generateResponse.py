from google import genai
from config.settings import settings
from .classes import GeminiQnAProcessor
from helper import utils

def main():
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    input_file = "./test/test-prompts/questions-workflow1.csv"
    output_file = "./test./test-answers./answers-workflow1.html"

    # preparing gant_chart
    # print(f"Preparing! response from prompt ./test/test-prompts/questions-ui-mockups4.csv ...")
    # processor.run( "./test/test-prompts/questions-ui-mockups4.csv", "./test/test-answers/answers-ui-mockups5.csv") 
    print(f"Preparing! response from prompt {input_file}...")
    processor.run_stream_to_file(input_file, output_file) 
    print("Finished!")

if __name__ == "__main__":
    main()
