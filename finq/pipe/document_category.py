import time

from loguru import logger

from finq.actions.space import ActionSpace, SpaceCategory
from finq.browser.context import Context
from finq.llms.engine import StructuredContent
from finq.llms.service import LLMService


class DocumentCategoryPipe:

    def __init__(self, llmserve: LLMService | None = None) -> None:
        self.llmserve: LLMService = llmserve or LLMService()

    def forward(self, context: Context, space: ActionSpace) -> SpaceCategory:
        description = f"""
- URL: {context.snapshot.metadata.url}
- Title: {context.snapshot.metadata.title}
- Description: {space.description or "No description available"}
""".strip()

        start_time = time.time()
        response = self.llmserve.completion(
            prompt_id="document-category/optim",
            variables={"document": description},
        )
        end_time = time.time()

        sc = StructuredContent(outer_tag="document-category")
        category = sc.extract(response.choices[0].message.content)  # type: ignore

        logger.info(f"🏷️ Page categorisation: {category} (took {end_time - start_time:.2f} seconds)")
        return SpaceCategory(category)
