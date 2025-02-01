from vllm import LLM, SamplingParams
from typing import List, Optional
import asyncio
from functools import lru_cache

class LLMManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.llm = LLM(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            trust_remote_code=True,
            dtype="bfloat16",
            tensor_parallel_size=1,  # Adjust based on number of GPUs
            gpu_memory_utilization=0.90,
            max_num_batched_tokens=4096,
        )

        self.sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.95,
            top_k=50,
            max_tokens=2048,
        )

    async def generate_response(self, prompt: str) -> str:
            try:
                # Convert the synchronous LLM call to async
                loop = asyncio.get_event_loop()
                outputs = await loop.run_in_executor(
                    None, 
                    lambda: self.llm.generate(prompt, self.sampling_params)
                )
                
                # Extract the generated text from the output
                if outputs and len(outputs) > 0:
                    generated_text = outputs[0].outputs[0].text.strip()
                    return generated_text.strip()
                return "No response generated"
                
            except Exception as e:
                raise Exception(f"Error generating response: {str(e)}")

    async def generate_batch_responses(self, prompts: List[str]) -> List[str]:
        try:
            # Convert the synchronous LLM call to async
            loop = asyncio.get_event_loop()
            outputs = await loop.run_in_executor(
                None,
                lambda: self.llm.generate(prompts, temperature=0.7, max_tokens=512)
            )
            
            # Extract all generated texts
            responses = []
            for output in outputs:
                if output.outputs:
                    responses.append(output.outputs[0].text.strip())
                else:
                    responses.append("No response generated")
            return responses
            
        except Exception as e:
            raise Exception(f"Error generating batch responses: {str(e)}")

def get_llm_manager():
    return LLMManager()