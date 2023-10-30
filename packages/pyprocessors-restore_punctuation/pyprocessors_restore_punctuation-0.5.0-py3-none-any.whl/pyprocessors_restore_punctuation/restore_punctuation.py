from enum import Enum
from functools import lru_cache
from typing import Type, List, cast

from punctuators.models import PunctCapSegModelONNX
# from deepmultilingualpunctuation import PunctuationModel
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence


class PunctuationModel(str, Enum):
    # fullstop_punctuation_multilang_large = "oliverguhr/fullstop-punctuation-multilang-large"
    # fullstop_punctuation_multilingual_sonar_base = "oliverguhr/fullstop-punctuation-multilingual-sonar-base"
    # punctuate_all = "kredor/punctuate-all"
    xlm_roberta_punctuation_fullstop_truecase = "1-800-BAD-CODE/xlm-roberta_punctuation_fullstop_truecase"
    punctuation_fullstop_truecase_romance = "1-800-BAD-CODE/punctuation_fullstop_truecase_romance"
    punctuation_fullstop_truecase_english = "1-800-BAD-CODE/punctuation_fullstop_truecase_english"


class RestorePunctuationParameters(ProcessorParameters):
    model: PunctuationModel = Field(
        PunctuationModel.xlm_roberta_punctuation_fullstop_truecase,
        description="""Which [Punctuation & truecasing](https://huggingface.co/1-800-BAD-CODE) model to use, can be one of:<br/>
                            <li>`1-800-BAD-CODE/xlm-roberta_punctuation_fullstop_truecase`: This is an xlm-roberta fine-tuned to restore punctuation, true-case (capitalize), and detect sentence boundaries (full stops) in 47 languages
                            <li>`1-800-BAD-CODE/punctuation_fullstop_truecase_romance`: This model restores punctuation, predicts full stops (sentence boundaries), and predicts true-casing (capitalization) for text in the 6 most popular Romance languages
                            <li>`1-800-BAD-CODE/punctuation_fullstop_truecase_english`: This model accepts as input lower-cased, unpunctuated English text and performs in one pass punctuation restoration, true-casing (capitalization), and sentence boundary detection (segmentation)""")
    sentences: bool = Field(False, description="Force sentence segmentation")


class RestorePunctuationProcessor(ProcessorBase):
    """Performs in one pass punctuation restoration, true-casing (capitalization), and sentence boundary detection (segmentation)"""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: RestorePunctuationParameters = cast(RestorePunctuationParameters, parameters)
        model = get_model(params.model)
        for document in documents:
            results: List[List[str]] = model.infer([document.text])
            sents = results[0]
            start = 0
            sentences = []
            if params.sentences:
                for sent in sents:
                    end = start + len(sent) + 1
                    sentences.append(Sentence(start=start, end=end))
                    start = end
                sentences[-1].end = len(document.text)
            document.sentences = sentences
            document.text = "\n".join(sents)
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return RestorePunctuationParameters


@lru_cache(maxsize=None)
def get_model(model: str):
    # if "1-800-BAD-CODE" in model:
    #     return PunctCapSegModelONNX.from_pretrained("pcs_en")
    # else:
    #     return PunctuationModel(model=model)
    return PunctCapSegModelONNX.from_pretrained(model)
