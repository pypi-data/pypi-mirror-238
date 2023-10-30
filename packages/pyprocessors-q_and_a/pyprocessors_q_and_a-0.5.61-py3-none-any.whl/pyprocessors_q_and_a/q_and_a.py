import os
from enum import Enum
from functools import lru_cache
from typing import Type, List, cast
import pandas as pd
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence, AltText, Annotation
from transformers import pipeline, QuestionAnsweringPipeline

_home = os.path.expanduser("~")
xdg_cache_home = os.environ.get("XDG_CACHE_HOME") or os.path.join(_home, ".cache")


class TrfModel(str, Enum):
    distilbert_base_uncased_distilled_squad = "distilbert-base-uncased-distilled-squad"
    camembert_base_squadFR_fquad_piaf = "etalab-ia/camembert-base-squadFR-fquad-piaf"


class ProcessingUnit(str, Enum):
    document = "document"
    segment = "segment"


class QandAParameters(ProcessorParameters):
    model: TrfModel = Field(
        TrfModel.distilbert_base_uncased_distilled_squad,
        description="""Which [Transformers model)(
                            https://huggingface.co/models?pipeline_tag=zero-shot-classification) fine-tuned
                            for Q&A to use, can be one of:<br/>
                            <li>`distilbert_base_uncased_distilled_squad`: This is the uncased DistilBERT model
                            fine-tuned on Multi-Genre Natural Language Inference (MNLI) dataset for the
                            zero-shot classification task. The model is not case-sensitive, i.e., it does not
                            make a difference between "english" and "English".
                            <li>`etalab-ia/camembert-base-squadFR-fquad-piaf`: Question-answering French model,
                            using base CamemBERT fine-tuned on a combo of three French Q&A datasets:
                              - PIAFv1.1
                              - FQuADv1.0
                              - SQuAD-FR (SQuAD automatically translated to French).""",
    )
    processing_unit: ProcessingUnit = Field(
        ProcessingUnit.document,
        description="""The processing unit to apply the Q&A in the input
                                            documents, can be one of:<br/>
                                            <li>`document`
                                            <li>`segment`""",
    )
    questions: List[str] = Field(None, description="The set of possible questions")
    threshold: float = Field(
        0.5, description="Minimum score for an answer to be considered"
    )
    nbest: int = Field(1, description="Number of answers to keep")


class QandAProcessor(ProcessorBase):
    """[🤗 Transformers](https://huggingface.co/transformers/index.html) Q&A."""

    # cache_dir = os.path.join(xdg_cache_home, 'trankit')

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: QandAParameters = cast(QandAParameters, parameters)
        # Create cached pipeline context with model
        p: QuestionAnsweringPipeline = get_pipeline(params.model)

        for document in documents:
            questions = document.altTexts or []
            document.annotations = document.annotations or []
            if params.processing_unit == ProcessingUnit.document:
                if questions:
                    for question in questions:
                        annotations = compute_answers(
                            p,
                            question,
                            params.threshold,
                            params.nbest,
                            document.text,
                            [Sentence(start=0, end=len(document.text))],
                        )
                        document.annotations.extend(annotations)
            elif params.processing_unit == ProcessingUnit.segment:
                if questions and document.sentences:
                    for question in questions:
                        annotations = compute_answers(
                            p,
                            question,
                            params.threshold,
                            params.nbest,
                            document.text,
                            document.sentences,
                        )
                        document.annotations.extend(annotations)
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return QandAParameters


def compute_answers(
    p: QuestionAnsweringPipeline,
    question: AltText,
    threshold: float,
    nbest: int,
    text: str,
    sentences: List[Sentence],
):
    annotations = []
    contexts = [text[s.start : s.end] for s in sentences]
    questions = [question.text] * len(contexts)
    sents = [{"sstart": s.start, "send": s.end} for s in sentences]
    result = p(question=questions, context=contexts, padding=True)
    if result:
        if isinstance(result, dict) and len(sents) == 1:
            result = [result]
        if isinstance(result, list) and len(result) == len(sents):
            df = pd.DataFrame.from_records(
                [{**answer, **sent} for answer, sent in zip(result, sents)]
            )
            df_best = df.sort_values("score", ascending=False).head(nbest)
            for index, answer in df_best.iterrows():
                if answer["score"] > threshold:
                    annotations.append(
                        Annotation(
                            label=question.name,
                            start=answer["sstart"] + answer["start"],
                            end=answer["sstart"] + answer["end"],
                            text=answer["answer"],
                            score=answer["score"],
                        )
                    )
    return annotations


@lru_cache(maxsize=None)
def get_pipeline(model):
    p = pipeline("question-answering", model=model.value)
    return p
