import os
import re
from abc import ABC
from enum import Enum
from math import floor, ceil
from typing import Type, cast, List

from pydantic import BaseModel, Field
from pymultirole_plugins.util import timed_lru_cache
from pymultirole_plugins.v1.formatter import FormatterParameters
from pymultirole_plugins.v1.processor import ProcessorBase, ProcessorParameters
from pymultirole_plugins.v1.schema import Document, AltText
from transformers import pipeline, SummarizationPipeline, AutoTokenizer

_home = os.path.expanduser("~")
xdg_cache_home = os.environ.get("XDG_CACHE_HOME") or os.path.join(_home, ".cache")


class TrfModel(str, Enum):
    #    t5_base = 't5-base'
    distilbart_xsum_12_6 = "sshleifer/distilbart-xsum-12-6"
    # distilbart_cnn_12_6 = 'sshleifer/distilbart-cnn-12-6'
    pegasus_xsum = "google/pegasus-xsum"
    # pegasus_multi_news = 'google/pegasus-multi_news'
    pegasus_pubmed = "google/pegasus-pubmed"
    mt5_multilingual_xlsum = "csebuetnlp/mT5_multilingual_XLSum"
    # bigbird_pegasus_large_pubmed = 'google/bigbird-pegasus-large-pubmed'
    camembert2camembert_shared_finetuned_french_summarization = (
        "mrm8488/camembert2camembert_shared-finetuned-french-summarization"
    )


class SummarizerParameters(ProcessorParameters):
    as_altText: str = Field(
        None,
        description="""If defined generate the summary as an alternative text of the input document,
    if not replace the text of the input document.""",
    )
    model: TrfModel = Field(
        TrfModel.mt5_multilingual_xlsum,
        description="""Which [Transformers model](
                            https://huggingface.co/models?pipeline_tag=zero-shot-classification) fine-tuned
                            for Summarization to use, can be one of:<br/>
                            <li>`sshleifer/distilbart-xsum-12-6`: The BART Model with a language modeling head finetuned on the [XSum](https://github.com/EdinburghNLP/XSum/tree/master/XSum-Dataset) dataset.
                            <li>`google/pegasus-xsum`: pegasus model fine-tune pegasus on the [XSum](https://github.com/EdinburghNLP/XSum/tree/master/XSum-Dataset) dataset.
                            <li>`google/pegasus-pubmed`: pegasus model fine-tune pegasus on the Pubmed dataset.
                            <li>`csebuetnlp/mT5_multilingual_XLSum`:  mT5 checkpoint finetuned on the 45 languages of [XL-Sum](https://github.com/csebuetnlp/xl-sum) dataset.
                            <li>`camembert2camembert_shared-finetuned-french-summarization`: French RoBERTa2RoBERTa (shared) fine-tuned on MLSUM FR for summarization.""",
    )
    min_length: float = Field(
        0.1,
        description="""Minimum number of tokens of the summary:<br/>
        <li>If int, then consider min_length as the minimum number.
        <li>If float in the range [0.0, 1.0], then consider min_length as a percentage
         of the original text length in tokens.""",
    )
    max_length: float = Field(
        0.25,
        description="""Maximum number of tokens of the summary:<br/>
        <li>If int, then consider max_length as the maximum number.
        <li>If float in the range [0.0, 1.0], then consider max_length as a percentage
         of the original text length in tokens.""",
    )

    do_sample: bool = Field(
        False,
        description="""Whether or not to use sampling; use greedy decoding otherwise""",
    )
    num_beams: int = Field(
        1,
        description="""Number of beams for beam search. 1 means no beam search.br/>
    Specifying this parameter will lead the model to use beam search instead of greedy search, setting num_beams to 4,
    will allow the model to lookahead for four possible words (1 in the case of greedy search),
    to keep the most likely 4 of hypotheses at each time step,
    and choosing the one that has the overall highest probability.""",
    )
    length_penalty: float = Field(
        1.0,
        description="""Exponential penalty to the length. 1.0 means no penalty.
    Set to values < 1.0 in order to encourage the model to generate shorter sequences,
    to a value > 1.0 in order to encourage the model to produce longer sequences.""",
    )
    no_repeat_ngram_size: int = Field(
        0, description="If set to int > 0, all ngrams of that size can only occur once."
    )
    early_stopping: bool = Field(
        False,
        description="""Whether to stop the beam search when at least `num_beams`
        sentences are finished per batch or not.""",
    )
    temperature: float = Field(
        1.0,
        description="""The value used to module the next token probabilities.""",
    )
    top_k: int = Field(
        50,
        description="""The number of highest probability vocabulary tokens to keep for top-k-filtering.""",
    )
    top_p: float = Field(
        1.0,
        description="""If set to float < 1, only the most probable tokens with probabilities that add up to `top_p` or higher
                are kept for generation.""",
    )
    num_return_sequences: int = Field(
        1,
        description="""The number of independently computed returned sequences for each element in the batch.""",
    )


def WHITESPACE_HANDLER(text):
    return re.sub(r"\s+", " ", re.sub(r"[\n\r]+", "<n>", text.strip()))
    # return re.sub(r"[\n\r]+", "<n>", text.strip())


MAX_LENGTH_BUG = int(floor(10 ** 30 + 1))


class SummarizerProcessor(ProcessorBase, ABC):
    """[🤗 Transformers](https://huggingface.co/transformers/index.html) Q&A."""

    # cache_dir = os.path.join(xdg_cache_home, 'trankit')

    def _summarize(self, document: Document, parameters: FormatterParameters) -> str:
        def int_float(v: float):
            if 0.0 <= v <= 1.0:
                return v
            return int(abs(v))

        params: SummarizerParameters = cast(SummarizerParameters, parameters)
        # Create cached pipeline context with model
        p: SummarizationPipeline = get_pipeline(params.model)

        clean_text = WHITESPACE_HANDLER(document.text)
        summary = ""
        try:
            model_max_length = (
                p.tokenizer.model_max_length
                if (p.tokenizer.model_max_length
                    and p.tokenizer.model_max_length < MAX_LENGTH_BUG
                    )
                else 512
            )
            inputs = p.tokenizer(
                [clean_text],
                padding=False,
                truncation=True,
                max_length=model_max_length,
                return_tensors="pt",
                return_length=True,
            )
            input_ids = inputs.input_ids
            attention_mask = inputs.attention_mask
            input_length = int(inputs.length)
            min_length = int_float(params.min_length)
            max_length = int_float(params.max_length)
            if isinstance(min_length, float):
                if 0 <= min_length <= 1.0:
                    min_length = floor(input_length * min_length)
                else:
                    min_length = 0
            if isinstance(max_length, float):
                if 0 <= max_length <= 1.0:
                    max_length = ceil(input_length * max_length)
                else:
                    max_length = input_length
            output = p.model.generate(
                input_ids,
                attention_mask=attention_mask,
                min_length=min_length,
                max_length=max_length,
                num_beams=params.num_beams,
                do_sample=params.do_sample,
                length_penalty=params.length_penalty,
                no_repeat_ngram_size=params.no_repeat_ngram_size,
                early_stopping=params.early_stopping,
                temperature=params.temperature,
                top_k=params.top_k,
                top_p=params.top_p,
                num_return_sequences=params.num_return_sequences
            )
            summary = p.tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            print(e)

        return summary.replace("<n>", " ")

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: SummarizerParameters = cast(SummarizerParameters, parameters)
        for document in documents:
            summary = self._summarize(document, parameters)
            if params.as_altText is not None and len(params.as_altText):
                document.altTexts = document.altTexts or []
                altTexts = [
                    alt for alt in document.altTexts if alt.name != params.as_altText
                ]
                altTexts.append(AltText(name=params.as_altText, text=summary))
                document.altTexts = altTexts
            else:
                document.text = summary
                document.annotations = None
                document.sentences = None
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SummarizerParameters


# Huggingface models are dropped after 1 hour
@timed_lru_cache(seconds=3600, maxsize=None)
def get_pipeline(model):
    p = pipeline(
        "summarization",
        model=model.value,
        tokenizer=AutoTokenizer.from_pretrained(model.value),
    )
    return p
