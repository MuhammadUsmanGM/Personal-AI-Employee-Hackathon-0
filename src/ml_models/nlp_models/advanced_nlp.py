"""
Advanced NLP Models for Gold Tier Personal AI Employee System
Implements multi-modal processing, entity recognition, and semantic understanding
"""
import os
import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging
import json
from datetime import datetime

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel, pipeline
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForTokenClassification
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

from ...utils.logger import log_activity


class AdvancedNLPProcessor:
    """
    Advanced NLP processing for Gold Tier AI capabilities
    """

    def __init__(self, model_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)

        # Initialize models
        self.sentence_transformer = None
        self.tokenizer = None
        self.model = None
        self.ner_pipeline = None
        self.sentiment_pipeline = None

        # Load models
        self._load_models(model_path)

    def _load_models(self, model_path: Optional[str] = None):
        """
        Load all required NLP models
        """
        try:
            # Load sentence transformer for embeddings
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

            # Load general transformer model
            model_id = "distilbert-base-uncased"
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModel.from_pretrained(model_id)

            # Load NER pipeline
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple"
            )

            # Load sentiment analysis pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )

            self.logger.info("NLP models loaded successfully")
            log_activity("NLP_MODELS_LOADED", "Advanced NLP models loaded", "obsidian_vault")

        except Exception as e:
            self.logger.error(f"Error loading NLP models: {e}")
            # Fallback to basic initialization
            self._init_basic_models()

    def _init_basic_models(self):
        """
        Initialize basic models if advanced models fail to load
        """
        try:
            # Basic sentence transformer
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

            # Basic tokenizer and model
            model_id = "distilbert-base-uncased"
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModel.from_pretrained(model_id)

            self.logger.info("Basic NLP models loaded as fallback")
        except Exception as e:
            self.logger.error(f"Error initializing basic models: {e}")

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from text

        Args:
            text: Input text to extract entities from

        Returns:
            List of extracted entities with their types and positions
        """
        if not self.ner_pipeline:
            return []

        try:
            entities = self.ner_pipeline(text)

            # Format entities
            formatted_entities = []
            for entity in entities:
                formatted_entities.append({
                    'text': entity['word'],
                    'label': entity['entity_group'],
                    'confidence': entity['score'],
                    'start': entity['start'],
                    'end': entity['end']
                })

            log_activity("ENTITY_EXTRACTION", f"Extracted {len(formatted_entities)} entities", "obsidian_vault")
            return formatted_entities

        except Exception as e:
            self.logger.error(f"Error extracting entities: {e}")
            return []

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of the given text

        Args:
            text: Input text to analyze sentiment for

        Returns:
            Sentiment analysis results
        """
        if not self.sentiment_pipeline:
            return {'label': 'NEUTRAL', 'score': 0.5}

        try:
            result = self.sentiment_pipeline(text)[0]

            log_activity("SENTIMENT_ANALYSIS", f"Sentiment: {result['label']}", "obsidian_vault")
            return {
                'label': result['label'],
                'score': result['score'],
                'confidence': result['score']
            }

        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate semantic embeddings for the given texts

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            Array of embeddings
        """
        if not self.sentence_transformer:
            return np.array([])

        try:
            embeddings = self.sentence_transformer.encode(texts)

            log_activity("EMBEDDING_GENERATION", f"Generated embeddings for {len(texts)} texts", "obsidian_vault")
            return embeddings

        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return np.array([])

    def find_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Find semantic similarity between two texts

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        if not self.sentence_transformer:
            return 0.0

        try:
            embeddings = self.sentence_transformer.encode([text1, text2])
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )

            log_activity("SEMANTIC_SIMILARITY", f"Similarity: {similarity:.3f}", "obsidian_vault")
            return float(similarity)

        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0

    def classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify the intent of the given text

        Args:
            text: Input text to classify intent for

        Returns:
            Intent classification results
        """
        # Define common intents for AI employee system
        intent_keywords = {
            'task_creation': ['create', 'make', 'start', 'begin', 'new'],
            'task_update': ['update', 'change', 'modify', 'edit', 'adjust'],
            'task_query': ['what', 'how', 'when', 'where', 'who', 'why'],
            'task_completion': ['complete', 'finish', 'done', 'finished', 'accomplished'],
            'approval_request': ['approve', 'permission', 'allow', 'authorize', 'consent'],
            'information_request': ['information', 'details', 'data', 'report', 'summary'],
            'strategic_planning': ['plan', 'strategy', 'goal', 'objective', 'target'],
            'risk_assessment': ['risk', 'danger', 'threat', 'problem', 'issue'],
            'compliance_check': ['compliance', 'regulation', 'rule', 'policy', 'requirement']
        }

        text_lower = text.lower()
        scores = {}

        for intent, keywords in intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[intent] = score

        # Return the intent with highest score
        if scores:
            best_intent = max(scores, key=scores.get)
            confidence = scores[best_intent] / max(1, sum(scores.values()))

            log_activity("INTENT_CLASSIFICATION", f"Intent: {best_intent}, Confidence: {confidence:.3f}", "obsidian_vault")
            return {
                'intent': best_intent,
                'confidence': confidence,
                'scores': scores
            }

        return {
            'intent': 'unknown',
            'confidence': 0.0,
            'scores': {}
        }

    def extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases from the given text

        Args:
            text: Input text to extract key phrases from

        Returns:
            List of key phrases
        """
        # Simple approach using NLTK-like techniques
        # In a real implementation, this would use more sophisticated NLP techniques

        # Remove punctuation and split into words
        words = re.findall(r'\b[A-Za-z]+\b', text.lower())

        # Filter out stop words
        filtered_words = [word for word in words if word not in STOP_WORDS and len(word) > 2]

        # Get unique words while preserving order
        seen = set()
        unique_words = []
        for word in filtered_words:
            if word not in seen:
                seen.add(word)
                unique_words.append(word)

        # Create phrases from consecutive words
        phrases = []
        if len(unique_words) >= 2:
            for i in range(len(unique_words) - 1):
                phrases.append(f"{unique_words[i]} {unique_words[i+1]}")

        # Add single words as well
        phrases.extend(unique_words)

        log_activity("KEY_PHRASE_EXTRACTION", f"Extracted {len(phrases)} key phrases", "obsidian_vault")
        return phrases[:20]  # Return top 20 phrases

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text

        Args:
            text: Input text to detect language for

        Returns:
            Language detection results
        """
        # Simple language detection based on character frequency
        # In a real implementation, this would use a dedicated library like langdetect

        # This is a simplified approach - a real implementation would be more sophisticated
        english_chars = sum(1 for c in text.lower() if c in 'etaoinshrdlcumwfgypbvkjxqz')
        total_chars = len([c for c in text.lower() if c.isalpha()])

        if total_chars == 0:
            return {'language': 'unknown', 'confidence': 0.0}

        eng_ratio = english_chars / total_chars

        # Very basic heuristic
        if eng_ratio > 0.7:
            language = 'en'
            confidence = eng_ratio
        else:
            language = 'unknown'
            confidence = 1 - eng_ratio

        log_activity("LANGUAGE_DETECTION", f"Language: {language}, Confidence: {confidence:.3f}", "obsidian_vault")
        return {
            'language': language,
            'confidence': confidence
        }

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Generate a summary of the given text

        Args:
            text: Input text to summarize
            max_sentences: Maximum number of sentences in summary

        Returns:
            Summary of the text
        """
        # Simple extractive summarization based on sentence importance
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= max_sentences:
            return '. '.join(sentences) + '.'

        # Calculate sentence importance based on word frequency
        all_words = []
        for sentence in sentences:
            words = re.findall(r'\b[A-Za-z]+\b', sentence.lower())
            all_words.extend([w for w in words if w not in STOP_WORDS])

        # Calculate word frequencies
        word_freq = {}
        for word in all_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Score sentences based on word frequencies
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            words = re.findall(r'\b[A-Za-z]+\b', sentence.lower())
            words = [w for w in words if w not in STOP_WORDS]

            if not words:
                score = 0
            else:
                score = sum(word_freq.get(w, 0) for w in words) / len(words)

            sentence_scores.append((i, score, sentence))

        # Sort by score and take top sentences, preserving original order
        top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:max_sentences]
        top_indices = sorted([idx for idx, _, _ in top_sentences])

        summary_sentences = [sentences[i] for i in top_indices]
        summary = '. '.join(summary_sentences) + '.'

        log_activity("TEXT_SUMMARIZATION", f"Summarized text to {len(summary_sentences)} sentences", "obsidian_vault")
        return summary

    def process_multi_modal_content(self, text: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process multi-modal content (currently text-focused with metadata)

        Args:
            text: Main text content
            metadata: Additional metadata about the content

        Returns:
            Processed multi-modal content analysis
        """
        analysis = {
            'text_summary': self.summarize_text(text),
            'entities': self.extract_entities(text),
            'sentiment': self.analyze_sentiment(text),
            'intent': self.classify_intent(text),
            'key_phrases': self.extract_key_phrases(text),
            'language': self.detect_language(text),
            'embedding': self.generate_embeddings([text])[0] if len(self.generate_embeddings([text])) > 0 else [],
            'content_type': 'text',
            'confidence_scores': {
                'overall': 0.85,  # Placeholder confidence
                'sentiment': self.analyze_sentiment(text)['score'],
                'intent': self.classify_intent(text)['confidence']
            }
        }

        # Add metadata if provided
        if metadata:
            analysis['metadata'] = metadata

        log_activity("MULTI_MODAL_PROCESSING", "Processed multi-modal content", "obsidian_vault")
        return analysis

    def find_related_content(self, text: str, corpus: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find related content from a corpus based on semantic similarity

        Args:
            text: Query text
            corpus: List of candidate texts to compare against
            top_k: Number of top results to return

        Returns:
            List of related content with similarity scores
        """
        if not corpus:
            return []

        # Generate embeddings for query and corpus
        all_texts = [text] + corpus
        embeddings = self.generate_embeddings(all_texts)

        if len(embeddings) < 2:
            return []

        query_embedding = embeddings[0]
        corpus_embeddings = embeddings[1:]

        # Calculate similarities
        similarities = []
        for i, corp_emb in enumerate(corpus_embeddings):
            sim = np.dot(query_embedding, corp_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(corp_emb)
            )
            similarities.append((i, float(sim)))

        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similarities = similarities[:top_k]

        results = []
        for idx, score in top_similarities:
            results.append({
                'index': idx,
                'text': corpus[idx][:200] + "..." if len(corpus[idx]) > 200 else corpus[idx],  # Truncate for readability
                'similarity_score': score
            })

        log_activity("RELATED_CONTENT_SEARCH", f"Found {len(results)} related content items", "obsidian_vault")
        return results


# Example usage and testing
if __name__ == "__main__":
    # Initialize the processor
    nlp = AdvancedNLPProcessor()

    # Test the processor
    test_text = "We need to analyze the quarterly sales report to identify trends and potential risks. The marketing team has proposed a new strategy that could increase revenue by 15%."

    print("Testing Advanced NLP Processor:")
    print(f"Input text: {test_text}\n")

    # Test entity extraction
    entities = nlp.extract_entities(test_text)
    print(f"Entities: {entities}\n")

    # Test sentiment analysis
    sentiment = nlp.analyze_sentiment(test_text)
    print(f"Sentiment: {sentiment}\n")

    # Test intent classification
    intent = nlp.classify_intent(test_text)
    print(f"Intent: {intent}\n")

    # Test key phrase extraction
    key_phrases = nlp.extract_key_phrases(test_text)
    print(f"Key phrases: {key_phrases}\n")

    # Test summarization
    summary = nlp.summarize_text(test_text)
    print(f"Summary: {summary}\n")

    # Test multi-modal processing
    multi_modal_result = nlp.process_multi_modal_content(test_text)
    print(f"Multi-modal result keys: {list(multi_modal_result.keys())}")