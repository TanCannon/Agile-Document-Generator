from google import genai
from config.settings import settings
from .classes import GeminiQnAProcessor
from helper import utils

def main():
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    # reset prompts by overwriting
    print(f"Resettting! prompt2 {settings.input_file2} ...")
    processor.reset_prompts(settings.questions2_reset, settings.input_file2)
    print("Resettting! Finished!")

    if not utils.is_file_empty_getsize(settings.output_file1):
        processor.append_result(settings.output_file1, settings.input_file2)
    else:
        print(f"The file '{settings.output_file1}' is empty.")
        return
    
    # preparing sprint_plan
    print(f"Preparing! sprint_plan prompt2 {settings.input_file2} ...")
    processor.run( settings.input_file2, settings.output_file2) 
    utils.csv_to_excel(settings.output_file2, settings.output_file2_xlsx)
    print("Finished! sprint_plan")

    # # reset prompts by overwriting
    # print(f"Resettting! prompt2 {settings.input_file2} ...")
    # processor.reset_prompts(settings.questions2_reset, settings.input_file2)
    # print("Resettting! Finished!")
if __name__ == "__main__":
    main()