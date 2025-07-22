import ollama
import sys
sys.stdout.reconfigure(encoding="utf-8")

def api_generate(prompt: str) -> str:
    """Generate a response from the model using a streaming API."""
    answer = ""
    stream = ollama.generate(
        stream=True,
        model='deepseek-r1:70b',
        prompt=prompt,
    )
    for chunk in stream:
        # Only append if the 'done' flag is False.
        if not chunk.get('done', True):
            answer += chunk.get('response', '')
    # Return text after the </think> tag if it exists.
    tag = "</think>"
    index = answer.find(tag)
    return answer[index + len(tag):] if index != -1 else answer

def read_clues(file_path: str) -> list:
    """Read and split the clues file by the delimiter 'SPRTION'."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove empty entries and leading/trailing spaces.
    return [clue.strip() for clue in content.split('SPRTION') if clue.strip()]

def write_response(file_path: str, response: str):
    """Append the response to the output file with the delimiter."""
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(response + "\nSPRTION\n")

def main():
    clues_file = r'c:/users/admin/desktop/tender/clues.TXT'
    output_file = r'c:/users/admin/desktop/tender/combined_ans.txt'
    clues = read_clues(clues_file)
    
    # Base instructions for constructing the prompt.
    base_prompt = (
        "You will receive a set of detailed citations and clues extracted from a tender document by another model. "
        "Your task is to analyze these citations to construct a clear, comprehensive answer to the following question: "
    )
    additional_instructions = (
         'Bear in mind that this question is the thing you should focus on. Your answer should strictly focus on this specific question. Give a cleared assertion and the answer to this question.'
        "First, repeat the question. Then, based on the provided evidence, synthesize the key points (such as project scope, contract terms, technical requirements, "
        "evaluation criteria, etc.) into a well-structured final answer. Reference the original citations where appropriate to "
        "support your analysis, ensuring your answer integrates all the relevant clues in a coherent and insightful manner. "
        "Ignore the original assertions and focus solely on the evidence provided."
    )
    
    # Process each clue and generate a combined answer.
    for i, clue in enumerate(clues, start=1):
        prompt = f"{base_prompt}{clue} {additional_instructions}"
        response = api_generate(prompt)
        write_response(output_file, response)
        print(f"Result {i} saved to '{output_file}'.")

if __name__ == '__main__':
    main()
