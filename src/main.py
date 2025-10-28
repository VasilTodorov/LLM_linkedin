from google import genai
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class FileData:
    header: str
    content: str

def read_from_file(path: Path | str)-> Optional[FileData]:    
    file_path = Path(path)       
    if file_path.exists() and file_path.is_file(follow_symlinks=False):        
        with file_path.open('r', encoding='utf-8') as file:
            content = file.read()
            header = file_path.name
            return FileData(header, content) 
    return None                                      
    
def write_to_file(file_path: Path | str, content: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
            

def summarize(job_description: str) -> str:
    base_prompt = read_from_file(r"D:\\workspace\\Python\\Training\\LLM_linkedin\\prompts\\JobPrompt_1.md")
    if not base_prompt:
        raise ValueError("Base prompt couldn't be read.")
    
    prompt = base_prompt.content.replace("[LINKEDIN_DATA]", job_description.strip())

    client = genai.Client(api_key="AIzaSyBbXcPnaht_l7PvbbBiONK12fO--ipArAw")
    response = client.models.generate_content(  # type: ignore
        model="gemini-2.5-flash",
        contents=prompt               
    )  
    if not response.text:
        raise ValueError("API key not provided. Set GOOGLE_API_KEY in your environment.")  
    return response.text 

def summarize_files_in_folder(input_folder: str, output_folder: str):
    input_folder_path = Path(input_folder)
    output_folder_path = Path(output_folder)
    #data: List[str] = []
    if not input_folder_path.exists():
        print(f"❌ Input folder does not exist: {input_folder}")
        return
    
    output_folder_path.mkdir(parents=True, exist_ok=True)

    for file_path in input_folder_path.iterdir():
        if file_path.is_file():
            data = read_from_file(file_path)
            if not data:
                print(f"⚠️ Skipping unreadable file: {file_path}")
                continue

            print(f"🧠 Summarizing: {data.header} ...")
            summary = summarize(data.content)

            output_path = output_folder_path / data.header
            write_to_file(output_path, summary)
            print(f"✅ Written to {output_path}")

    print("✨ All files summarized successfully!")


summarize_files_in_folder(r"D:\\workspace\\Python\\Training\\LLM_linkedin\\input", r"D:\\workspace\\Python\\Training\\LLM_linkedin\\output")