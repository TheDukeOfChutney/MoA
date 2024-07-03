# Mixture-of-Agents in 50 lines of code
import asyncio
from ollama import AsyncClient

user_prompt = "What are some fun things to do in SF?"
reference_models = [
    "phi",  # Replace with actual Ollama models
    "phi",
    "phi",
    "phi",
]
aggregator_model = "phi"  # Replace with the actual Ollama aggregator model

aggregator_system_prompt = """You have been provided with a set of responses from various models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. 
It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but 
should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""

async def run_llm(client, model, prompt):
    """Run a single LLM call with a reference model."""
    response = await client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "options":{"temperature":0.7,"num_ctx":512}}],
    )
    print(model)
    
    #print(response['message']['content'])
    return response['message']['content']


async def main():
    client = AsyncClient()
    tasks = [run_llm(client, model, user_prompt) for model in reference_models]
    results = await asyncio.gather(*tasks)

    final_prompt = f"{aggregator_system_prompt}\n\n{','.join(results)}"
    final_response = await client.chat(
        model=aggregator_model,
        messages=[
            {"role": "system", "content": aggregator_system_prompt, "options":{"temperature":0.7,"num_ctx":512}},
            {"role": "user", "content": final_prompt, "options":{"temperature":0.7,"num_ctx":512}}
        ],
    )
    print(final_response['message']['content'])

asyncio.run(main())
