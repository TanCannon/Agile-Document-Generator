from google import genai
from config.settings import settings
from .classes import GeminiQnAProcessor
from helper import utils
from helper import pdfreader 
from helper.extractor import extract_pdf_toc, extract_from_csv_and_write 

# pdf_content_path = settings.pdfreader_output_path
def main(frd_path:str = "") -> None:
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    # #reading the input pdf and saving it 
    # if frd_path != "":
    #     frd_data = pdfreader.read_pdf(frd_path, pdf_content_path)
    # else:
    #     print("FRD file path empty")
    #     return
    
    #preparing table of content
    extract_pdf_toc(frd_path, settings.output_heads_subheads)

    # reset prompts by overwriting
    print(f"Resettting! prompt1 {settings.input_file1_1} ...")
    processor.reset_prompts(settings.Resetquestions1_1, settings.input_file1_1)
    print("Resettting! Finished!")

    #preparing prompt head/subheads for detailed plan
    processor.append_result(settings.output_heads_subheads, settings.input_file1_1)

    #preparing required head/subheads for detailed plan
    print(f"Preparing! required head/subheads for detailed plan from prompt1 {settings.input_file1_1} ...")
    processor.run(settings.input_file1_1, settings.output_file1_1)
    print(f"FINISHED!")

    # # reset prompts by overwriting
    # print(f"Resettting! prompt1 {settings.input_file1_1} ...")
    # processor.reset_prompts(settings.Resetquestions1_1, settings.input_file1_1)
    # print("Resettting! Finished!")

    #extract content of required head/subheads for detailed plan
    extract_from_csv_and_write(frd_path, settings.output_file1_1, settings.extract_output_file1_1)

    # reset prompts by overwriting
    print(f"Resettting! prompt1 {settings.input_file1} ...")
    processor.reset_prompts(settings.questions1_reset, settings.input_file1)
    print("Resettting! Finished!")
    
    #preparing prompt
    processor.append_result(settings.extract_output_file1_1, settings.input_file1)

    #preparing user_stories
    print(f"Preparing! user_stories from prompt1 {settings.input_file1} ...")
    processor.run(settings.input_file1, settings.output_file1)
    utils.csv_to_excel(settings.output_file1, settings.output_file1_xlsx)
    print("Finished! user_stories")

    # # reset prompts by overwriting
    # print(f"Resettting! prompt1 {settings.input_file1} ...")
    # processor.reset_prompts(settings.questions1_reset, settings.input_file1)
    # print("Resettting! Finished!")

if __name__ == "__main__":
    file_path = "./documents/DIG-ITS FRD_v2.pdf"
    main(file_path)

