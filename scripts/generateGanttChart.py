from google import genai
from config.settings import settings
from .classes import GeminiQnAProcessor
from helper import utils

def main():
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    # reset prompts by overwriting
    print(f"Resettting! prompts3 {settings.input_file3} ...")
    processor.reset_prompts(settings.questions3_reset, settings.input_file3)
    print("Resettting! Finished!")

    if not utils.is_file_empty_getsize(settings.output_file2):
        processor.append_result(settings.output_file2, settings.input_file3)
    else:
        print(f"The file '{settings.output_file2}' is empty.")
        return
    
    # preparing gant_chart
    print(f"Preparing! gant_chart from prompt3 {settings.input_file3} ...")
    processor.run( settings.input_file3, settings.output_file3) 
    utils.csv_to_excel(settings.output_file3, settings.output_file3_xlsx)
    print("Finished! gant_chart")

    # # reset prompts by overwriting
    # print(f"Resettting! prompts3 {settings.input_file3} ...")
    # processor.reset_prompts(settings.questions3_reset, settings.input_file3)
    # print("Resettting! Finished!")

if __name__ == "__main__":
    main()
