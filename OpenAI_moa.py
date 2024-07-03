# Mixture-of-Agents in 50 lines of code
import asyncio
import os
from openai import OpenAI, AsyncOpenAI

client = OpenAI(api_key="your-key")
aclient = AsyncOpenAI(api_key="your-key")

#openai.api_key = os.environ.get("OPENAI_API_KEY")
user_prompt = "What are some fun things to do in SF?"


reference_models = [
    "gpt-3.5-turbo",  # Placeholder for models available via OpenAI API
    "gpt-3.5-turbo",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo",
]
aggregator_model = "gpt-3.5-turbo"  # Placeholder for the aggregator model
aggregator_system_prompt = """You have been provided with a set of responses from various models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. 
It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but 
should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""

async def run_llm(model):
    """Run a single LLM call with a reference model."""
    response = await aclient.chat.completions.create(model=model,
    messages=[{"role": "user", "content": user_prompt}],
    temperature=0.7,
    max_tokens=512)
    print(model)
    return response.choices[0].message.content

async def main():
    results = await asyncio.gather(*[run_llm(model) for model in reference_models])

    finalStream = client.chat.completions.create(model=aggregator_model,
    messages=[
        {"role": "system", "content": aggregator_system_prompt},
        {"role": "user", "content": ",".join(str(element) for element in results)},
    ])


    print(finalStream.choices[0].message.content or "", end="", flush=True)

asyncio.run(main())
