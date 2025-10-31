from google import genai
from settings import settings
from classes import GeminiQnAProcessor
import utils
import pdfreader 

output_path = "./uploades/pdf-text.txt"
def main(frd_path:str = "") -> None:
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    #reading the input pdf and saving it 
    if frd_path != "":
        frd_data = pdfreader.read_pdf(frd_path, output_path)
    else:
        print("FRD file path empty")
        return
    
    #preparing prompt
    processor.append_result("./uploades/pdf-text.txt", settings.input_file1)

    #preparing user_stories
    print(f"Preparing! user_stories from prompt1 {settings.input_file1} ...")
    processor.run(settings.input_file1, settings.output_file1)
    utils.csv_to_excel(settings.output_file1, "./outputs/UserStories.xlsx")
    print("Finished! user_stories")

    # reset prompts by overwriting
    print(f"Resettting! prompt1 {settings.input_file1} ...")
    processor.reset_prompts( "./prompts/Resetquestions1.csv", settings.input_file1)
    print("Resettting! Finished!")

if __name__ == "__main__":
    file_path = "./documents/demo-FRD.pdf"
    main("./documents/demo-FRD.pdf")

