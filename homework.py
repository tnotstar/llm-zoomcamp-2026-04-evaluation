import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from gitsource import GithubRepositoryDataReader

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# Define the expected structured output schema
class Questions(BaseModel):
    questions: list[str]

# 1. Load the dataset using the specified commit
from gitsource import GithubRepositoryDataReader

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [file.parse() for file in reader.read()]

# Filter for the specific first 3 target lesson pages
target_lessons = {
    "01-agentic-rag/lessons/01-intro.md",
    "01-agentic-rag/lessons/02-environment.md",
    "01-agentic-rag/lessons/03-rag.md"
}

sample_pages = [doc for doc in documents if doc.filename in target_lessons]

print(f"Number of loaded documents: {len(sample_pages)}")
import sys
sys.exit(0)


# 2. Define prompt system instructions
data_gen_instructions = """
You emulate a student who is taking our LLM course.
You are given one lesson page from the course.
Formulate 5 questions this student might ask that are answered by this page.

Rules:
- The page should contain the answer to each question.
- Make the questions complete and not too short.
- Use as few words as possible from the page; don't copy its phrasing.
- The questions should resemble how people actually ask things online:
  not too formal, not too short, not too long.
- Ask about the content of the lesson, not about its formatting or filename.
""".strip()

total_input_tokens = 0

# 3. Request completions and aggregate token metrics
for page in sample_pages:
    user_prompt = f"Filename: {page.filename}\nContent: {page.content}"
    
    response = client.beta.chat.completions.parse(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": data_gen_instructions},
            {"role": "user", "content": user_prompt}
        ],
        response_format=Questions,
    )
    
    # Extract prompt tokens from the response usage object
    input_tokens = response.usage.prompt_tokens
    total_input_tokens += input_tokens
    print(f"Page: {page.filename} -> Input Tokens: {input_tokens}")

# 4. Calculate and output the arithmetic mean
average_input_tokens = total_input_tokens / len(sample_pages)
print(f"\nAverage Input Tokens: {average_input_tokens:.2f}")