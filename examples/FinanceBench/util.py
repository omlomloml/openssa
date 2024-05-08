from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from loguru import logger
from pandas import DataFrame, read_csv
from tqdm import tqdm

from data import FbId, Answer, FB_ID_COL_NAME, META_DF, FB_IDS, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID, OUTPUT_FILE_PATH
from eval import eval_correctness


type QAFunc = Callable[[FbId], Answer]


def enable_batch_qa(qa_func: QAFunc) -> QAFunc:
    @wraps(wrapped=qa_func)
    def decorated_qa_func(fb_id: FbId) -> Answer:
        if 'all' in fb_id.lower():
            for _fb_id in tqdm(FB_IDS):
                qa_func(_fb_id)

            return None

        return qa_func(fb_id)

    return decorated_qa_func


@dataclass
class log_qa_and_eval_correctness_and_update_output_file:  # noqa: N801
    output_name: str

    def __post_init__(self):
        self.correctness_eval_col_name: str = f'{self.output_name}: CORRECT?'

    def __call__(self, qa_func: QAFunc) -> QAFunc:
        @wraps(wrapped=qa_func)
        def decorated_qa_func(fb_id: FbId) -> Answer:
            logger.info(f'\n{fb_id}\n{DOC_NAMES_BY_FB_ID[fb_id]}:\n{QS_BY_FB_ID[fb_id]}\n'
                        f'\n{self.output_name.upper()}:\n'
                        f'{(answer := qa_func(fb_id)).replace('{', '{{').replace('}', '}}')}\n',
                        depth=1)

            if OUTPUT_FILE_PATH.is_file():
                output_df: DataFrame = read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME)

            else:
                output_df: DataFrame = META_DF[['doc_name', 'question', 'evidence_text', 'page_number', 'answer']]
                output_df.loc[:, self.output_name]: str | None = None
                output_df.loc[:, self.correctness_eval_col_name]: bool | None = None

            output_df.loc[fb_id, self.output_name]: str = answer
            output_df.loc[fb_id, self.correctness_eval_col_name]: bool = eval_correctness(fb_id=fb_id, answer=answer)

            output_df.to_csv(OUTPUT_FILE_PATH, index=True)

            return answer

        return decorated_qa_func
