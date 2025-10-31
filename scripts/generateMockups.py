from google import genai
from config.settings import settings
from .classes import GeminiQnAProcessor
from helper import extractor
from helper import utils
from helper.capturepages import capture_sections_screenshots
import csv
import time
import pathlib
import os

cooldown_time = 2

def main(input_pdf_path: str, output_heads_subheads: str = settings.output_heads_subheads):
    processor = GeminiQnAProcessor(api_key=settings.api_key)

    # input_file = "./prompts/questions-ui-mockups1.csv"
    # output_file = "./outputs/answers-ui-mockups1.csv"

    # fetch the table of content 
    extractor.extract_pdf_toc(input_pdf_path, settings.output_heads_subheads)

    #reset prompt questions-headings1.csv
    processor.reset_prompts(settings.Resetquestions1_1, settings.questions_extract_headings)  

    #append the table of content in the prompt questions-headings1.csv
    if not utils.is_file_empty_getsize(settings.output_heads_subheads):
        processor.append_result(settings.output_heads_subheads, settings.questions_extract_headings)
    else:
        print(f"The file '{settings.output_heads_subheads}' is empty.")
        return  

    # ask API to use which headings
    processor.run(settings.questions_extract_headings, settings.answers_extracted_headings)

    #fetch the specific heading content
    extractor.extract_from_csv_and_write(input_pdf_path, settings.answers_extracted_headings, settings.output_extracted_heading_content)

    #generate UI mockups summary
    # Step 1: reset and append the heading content into questions_screens_summary1.csv
    processor.reset_prompts(settings.Resetquestions_screen_summary, settings.questions_screen_summary)

    if not utils.is_file_empty_getsize(settings.output_extracted_heading_content):
        processor.append_result(settings.output_extracted_heading_content, settings.questions_screen_summary)
    else:
        print(f"The file '{settings.output_extracted_heading_content}' is empty.")
        return

    #Step 2: input = questions-screen_summary1.csv output = answers-screen_summary1.csv
    processor.run(settings.questions_screen_summary, settings.answers_screen_summary)

    # #Step 3: reset questions-screen_summary1.csv
    # processor.reset_prompts(settings.Resetquestions_screen_summary, settings.questions_screen_summary)

    #generate UI mockups HTML CSS by iterating over the UI mockup summary
    # Step1: reset questions_ui_mockups1.csv and append the screen name and its summary
    processor.reset_prompts(settings.questions4_reset, settings.questions_generate_UI_mockups)

    with open(settings.answers_screen_summary, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter="|")
        next(reader)  # skip header row dynamically
        screen_name_col, summary_col = 0, 1  # assume first col = screenname, second col = summary
        rows = list(reader)
        for idx, row in enumerate(rows):
                screen_name = row[screen_name_col].strip()
                summary = row[summary_col].strip()
                #append the screenname and summary into questions_ui_mockups1.csv 
                if screen_name != "" or summary != "":
                    with open(settings.questions_generate_UI_mockups, "a", encoding="utf-8") as f:
                        content = screen_name + "\n" + summary
                        f.write(content)
                else:
                    print(f"The {row} is empty.")
                    return   

                #Step 2: generate the screen HTML CSS
                run_status = True
                print(f"Creating screen {screen_name}")

                # Step3: run and then reset the questions_ui_mockups1.csv

                run_status = processor.run_stream_to_file(settings.questions_generate_UI_mockups, settings.answers_generated_UI_mockups)

                processor.reset_prompts(settings.questions4_reset, settings.questions_generate_UI_mockups)

                if (run_status == False): #exit if model overloaded or goes into error
                    return
                #Step4: save screenshots of the screen 
                # Get absolute path
                abs_path = pathlib.Path( settings.answers_generated_UI_mockups).resolve()
                # Convert to file URL for Playwright
                file_url = abs_path.as_uri()
                print(f"Capturing screenshots of {file_url}")
                capture_sections_screenshots(file_url, os.path.join(settings.screenshot_output_path,screen_name))
                # print(f"Finished caturring screenshots!")

                #Step5: wait for cooldown time    
                print(f"Sleeping for {cooldown_time} seconds")
                time.sleep(cooldown_time)
                print("RESTARTED!")

    print("Finished!")

if __name__ == "__main__":
    # def main(input_pdf_path: str, output_heads_subheads: str):
    input_pdf_path = "./documents/DIG-ITS FRD_v2.pdf"
    output_heads_subheads = settings.output_heads_subheads
    main(input_pdf_path, output_heads_subheads)
