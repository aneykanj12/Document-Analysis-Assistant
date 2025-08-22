from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers.utils.logging import set_verbosity_error
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForQuestionAnswering

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
USE_TOKENIZER = False
DEVICE_INDEX = 0 if DEVICE == "cuda" else -1

set_verbosity_error()

# general processing of pipelines: summary -> refinement
def summarization():
    if USE_TOKENIZER:
        tok = AutoTokenizer.from_pretrained("facebook/bart-large-cnn", use_fast=True)
        mod = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        summarization_pipeline = pipeline(
            "summarization",
            model=mod,
            tokenizer=tok,
            device=DEVICE_INDEX
        )
    else:
        summarization_pipeline = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=DEVICE_INDEX
        )
    summarizer = HuggingFacePipeline(pipeline=summarization_pipeline)
    return summarizer

def refinement():
    if USE_TOKENIZER:
        tok = AutoTokenizer.from_pretrained("facebook/bart-large", use_fast=True)
        mod = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")
        refinement_pipeline = pipeline(
            "summarization",
            model=mod,
            tokenizer=tok,
            device=DEVICE_INDEX
        )
    else:
        refinement_pipeline = pipeline(
            "summarization",
            model="facebook/bart-large",
            device=DEVICE_INDEX
        )
    refiner = HuggingFacePipeline(pipeline=refinement_pipeline)
    return refiner

def question_and_answers():
    if USE_TOKENIZER:
        tok = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2", use_fast=True)
        mod = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
        qa_pipeline = pipeline(
            "question-answering",
            model=mod,
            tokenizer=tok,
            device=DEVICE_INDEX,
        )
    else:
        qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            device=DEVICE_INDEX,
        )
    return qa_pipeline

def prompt_template_loader(actual_text, desired_length):
    summary_template = PromptTemplate.from_template("You will give a {desired_length} length summary of the text below. Summarize only what appears and do not add facts.\n\n TEXT START\n{actual_text}\nTEXT END")
    chain = summary_template | summarization() | refinement()
    final_summary = chain.invoke({"actual_text": actual_text, "desired_length": desired_length})
    
    return final_summary

def question_and_answers_responder(actual_question, actual_summary):
    qa_pipe = question_and_answers()
    qa_res = qa_pipe(question = actual_question, context = actual_summary)
    return qa_res
