
from google import genai
from config import GEMINI_API_KEY
from database import get_schema

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"

def load_prompt(version):
    with open(f"prompts/{version}.txt", "r") as file:
        return file.read()

def run_experiment(version, question):

    template = load_prompt(version)

    prompt = template.replace(
        "{schema}", get_schema()
    ).replace(
        "{question}", question
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":

    question = input("Enter your test question: ")

    for version in ["v1", "v2", "v3"]:

        print(f"\n========== {version.upper()} ==========")

        try:
            result = run_experiment(version, question)
            print(result)

        except Exception as error:
            print("ERROR:", error)
