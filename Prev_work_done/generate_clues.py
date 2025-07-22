import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import PyPDF2
import openpyxl
import sys
import io

# 修改标准输出的编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Define your model path
model_path = r"C:\Users\admin\glm-4-9b-chat-1m"

# Load tokenizer and model once
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).to(device).eval()

# Define base prompt text for the PDFs
base_prompt = (
    "You are provided with a very long tender document. Your task is to read the entire document carefully—from the beginning to the end—"
    "ensuring you capture every detail and all key points (including, but not limited to, project scope, contract terms, technical requirements, evaluation criteria, etc.)."
)

def load_pdf_text(file_path: str, base_text: str) -> str:
    """Load PDF text and append a trailing instruction."""
    text = base_text
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # safeguard against pages with no text
                text += page_text
    text += "While reading, identify and extract all passages, clauses, or statements that directly address the following question: "
    return text

# Load texts from both PDFs
text1 = load_pdf_text(r'c:/users/admin/desktop/tender/ops1.pdf', base_prompt)
text2 = load_pdf_text(r'c:/users/admin/desktop/tender/ops2.pdf', base_prompt)
text3 = load_pdf_text(r'c:/users/admin/desktop/tender/ops3.pdf', base_prompt)
text4 = load_pdf_text(r'c:/users/admin/desktop/tender/ops4.pdf', base_prompt)
text5 = load_pdf_text(r'c:/users/admin/desktop/tender/ops5.pdf', base_prompt)
text6 = load_pdf_text(r'c:/users/admin/desktop/tender/ops6.pdf', base_prompt)
text7 = load_pdf_text(r'c:/users/admin/desktop/tender/ops7.pdf', base_prompt)
text8 = load_pdf_text(r'c:/users/admin/desktop/tender/ops8.pdf', base_prompt)
text9 = load_pdf_text(r'c:/users/admin/desktop/tender/ops9.pdf', base_prompt)
# Load Excel file and extract questions from column B (skip header)
excel_file_path = r'C:\Users\admin\Desktop\tender\final_output.xlsx'
workbook = openpyxl.load_workbook(excel_file_path)
sheet = workbook.active

questions = []
for row in sheet.iter_rows(min_col=2, max_col=2, min_row=2):
    for cell in row:
        if cell.value and '?' in cell.value:
            questions.append(cell.value)

# Generation parameters (you can adjust max_length if needed)
gen_kwargs = {
    "max_new_tokens": 256,
    "do_sample": False,
    "num_beams": 1
}

def generate_response(query: str) -> str:
    """Generate a response from the model given a query."""
    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": query}],
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True
    ).to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        # Remove the input portion from the output
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded

# Define the prompt that is common to both queries
response_instructions = (
    "Your response should consist solely of exact citations (verbatim excerpts with clear references to the relevant sections) "
    "from the original text that provide clues or information pertinent to the question. "
    "Do not summarize, paraphrase, or provide any analysis—only list the original cited text and its exact location."
)

# Output file path
output_file = r'c:/users/admin/desktop/tender/clues.TXT'

# Process each question
for idx, question in enumerate(questions[21:], start=1):
    # Build queries for both documents
    query1 = f"{text1}{question}{response_instructions}"
    query2 = f"{text2}{question}{response_instructions}"
    query3 = f"{text3}{question}{response_instructions}"
    query4 = f"{text4}{question}{response_instructions}"
    query5 = f"{text5}{question}{response_instructions}"
    query6 = f"{text6}{question}{response_instructions}"
    query7 = f"{text7}{question}{response_instructions}"
    query8 = f"{text8}{question}{response_instructions}"
    query9 = f"{text9}{question}{response_instructions}"

    print(f"\nProcessing Question {idx}: {question}\n")
    
    # Generate and process response for the first document
    response1 = generate_response(query1)
    print(f"Response for Document 1:\n{response1}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write("\n" + question + "\n")
        f.write(response1)
        f.write("\n")
    
    # Generate and process response for the second document
    response2 = generate_response(query2)
    print(f"Response for Document 2:\n{response2}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response2)
        
    
    response3 = generate_response(query3)
    print(f"Response for Document 3:\n{response3}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response3)
        
    
    response4 = generate_response(query4)
    print(f"Response for Document 4:\n{response4}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response4)
       
    
    response5 = generate_response(query5)
    print(f"Response for Document 5:\n{response5}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response5)
       
    
    response6 = generate_response(query6)
    print(f"Response for Document 6:\n{response6}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response6)
       
    
    response7 = generate_response(query7)
    print(f"Response for Document 7:\n{response7}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response7)
        
    
    response8 = generate_response(query8)
    print(f"Response for Document 8:\n{response8}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response8)
      
    
    response9 = generate_response(query9)
    print(f"Response for Document 9:\n{response9}\n")
    with open(output_file, 'a', encoding='utf-8', errors='ignore') as f:
        f.write(response9)
        f.write("\nSPRTION\n")
    
    
    print(f"Question {idx} responses saved to '{output_file}'.")
