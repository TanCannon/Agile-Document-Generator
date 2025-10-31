from pydantic import BaseModel
from dotenv import load_dotenv
import yaml
import os

# Load .env file from the same directory
from pathlib import Path
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Path to config.yaml
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# Load YAML config
with open(CONFIG_PATH) as f:
    yaml_config = yaml.safe_load(f)

class Settings(BaseModel):
    # prompt input output paths & parameters
    input_file1: str
    input_file1_1: str
    output_file1_1: str
    output_file1: str
    output_file1_xlsx: str

    input_file2: str
    output_file2: str
    output_file2_xlsx: str

    input_file3: str
    output_file3: str
    output_file3_xlsx: str
    
    # ---- prompt reset settings ---------
    questions1_reset: str
    questions2_reset: str
    questions3_reset: str
    questions4_reset: str
    Resetquestions1_1: str
    Resetquestions_screen_summary: str
    # pdfreader input output paths & parameters
    pdfreader_output_path: str

    ## ----extract headings input output settings ---------
    output_heads_subheads: str
    questions_extract_headings: str
    answers_extracted_headings: str
    output_extracted_heading_content: str
    extract_output_file1_1: str

    ## ----UI mockups input output settings ---------
    questions_screen_summary: str
    answers_screen_summary: str
    questions_generate_UI_mockups: str
    answers_generated_UI_mockups: str
    screenshot_output_path: str
    
    # Secrets
    api_key: str

# Merge YAML config with environment variables
settings = Settings(
    **yaml_config,
    api_key=os.getenv("API_KEY")
)

if __name__ == "__main__":
    # Example usage
    print(settings.input_file1)
    print(settings.api_key)  # secret from .env
