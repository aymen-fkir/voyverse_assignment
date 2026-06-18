from ollama import AsyncClient
import httpx
import asyncio
from typing import Union
from utils.schemas import GatheredData, InpuToLlm, LlmOutputList
from utils.helper import load_prompt

from utils.logger import VoyverseLogger


logger = VoyverseLogger.get("LLMClassification")
class LLMClassification:
    def __init__(self, model_name: str, chunk_size: int = 10):
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.system_prompt = load_prompt("llm_classification")
        client_limits = httpx.Limits(
            max_connections=20,          # Total maximum allowed connections
            max_keepalive_connections=5, # How many idle connections to keep open in the pool
            keepalive_expiry=20.0          # Time in seconds to keep idle connections alive
        )

        self.client = AsyncClient(
            timeout=None,
            limits=client_limits          # Apply the optimized connection pool
        )


    async def classify(self, texts: list[InpuToLlm]) -> Union[LlmOutputList,list]:
        lines = [f"\n- Description: '{text.description.strip()}'" for text in texts]
        prompt = "### Text to Classify:\n" + "\n".join(lines)

        response = await self.client.generate(
            model=self.model_name,
            prompt=prompt,
            system=self.system_prompt,
            format=LlmOutputList.model_json_schema(),
            options={"temperature": 0.0},
        )
        try:
            raw_response = response.response
            logger.info("finish classifying batch ", response=len(texts))

            if not raw_response:
                logger.error("Received empty response from the model.")
                return [None]*self.chunk_size

            return LlmOutputList.model_validate_json(raw_response)
        
        except Exception as e:
            logger.error("Error parsing model response", exc=e)
            return [None]*self.chunk_size    
        

    def postprocess(self, results: list[Union[LlmOutputList,list]],data:list[InpuToLlm]) -> GatheredData:
         gathered_results = []
         for i,result in enumerate(results):
            if isinstance(result, LlmOutputList):
                for j in range(i*self.chunk_size, (i+1)*self.chunk_size):
                    result.root[j%self.chunk_size].id = data[j].id
                gathered_results.extend(result.root)
            else:
                logger.warning(f"Unexpected result type received from the model. Expected LlmOutputList but got a different type.{type(result)}")
         
         return GatheredData(root=gathered_results)

    async def run(self, input_to_llm: list[InpuToLlm]) -> GatheredData:

            chunks = [
                input_to_llm[i : i + self.chunk_size]
                for i in range(0, len(input_to_llm), self.chunk_size)
            ][:5]

            # 1. Initialize a semaphore to cap concurrent requests to Ollama
            # Adjust '3' based on your server's OLLAMA_NUM_PARALLEL configuration
            sem = asyncio.Semaphore(10)

            # 2. Define an internal worker that honors the semaphore capacity
            async def semaphored_classify(chunk,number):
                async with sem:
                    logger.info("starting to Classify  chunk", chunk_number=number)
                    return await self.classify(chunk)

            # 3. Schedule all chunks using the semaphored worker instead
            results: list[Union[LlmOutputList,list]] = await asyncio.gather(
                *[semaphored_classify(chunk,i+1) for i,chunk in enumerate(chunks)]
            )

            # merge all chunks into a single LlmOutputList
            merged = self.postprocess(results,input_to_llm)
            logger.info("Completed all classification tasks", results=merged.root)

            return merged