"""
ML Model Training Pipeline for Gold Tier Personal AI Employee System
Handles model training, evaluation, and deployment for advanced AI capabilities
"""
import os
import json
import pickle
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer

from ..utils.logger import log_activity


class ModelTrainingPipeline:
    """
    Comprehensive training pipeline for Gold Tier ML models
    """

    def __init__(self, model_dir: str = "models", experiment_dir: str = "experiments"):
        self.model_dir = Path(model_dir)
        self.experiment_dir = Path(experiment_dir)
        self.model_dir.mkdir(exist_ok=True)
        self.experiment_dir.mkdir(exist_ok=True)

        # Initialize logging
        self.logger = logging.getLogger(__name__)

    def download_pretrained_models(self):
        """
        Download and cache pretrained models for various tasks
        """
        self.logger.info("Downloading pretrained models...")

        models_to_download = {
            "sentence_transformer": "all-MiniLM-L6-v2",
            "nlp_classifier": "distilbert-base-uncased",
            "multilingual": "distilbert-base-multilingual-cased"
        }

        model_paths = {}

        for model_name, model_id in models_to_download.items():
            try:
                if "sentence" in model_name:
                    model = SentenceTransformer(model_id)
                    model_path = self.model_dir / f"{model_name}_model"
                    model.save(str(model_path))
                    model_paths[model_name] = str(model_path)
                else:
                    tokenizer = AutoTokenizer.from_pretrained(model_id)
                    model = AutoModel.from_pretrained(model_id)

                    model_path = self.model_dir / f"{model_name}_model"
                    model_path.mkdir(exist_ok=True)

                    tokenizer.save_pretrained(model_path)
                    model.save_pretrained(model_path)
                    model_paths[model_name] = str(model_path)

                self.logger.info(f"Downloaded {model_name} model")
                log_activity("MODEL_DOWNLOAD", f"Downloaded {model_name} model", "obsidian_vault")

            except Exception as e:
                self.logger.error(f"Failed to download {model_name}: {e}")

        return model_paths

    def train_sentiment_analyzer(self, training_data: List[Dict[str, Any]],
                               model_name: str = "sentiment-analyzer") -> str:
        """
        Train a sentiment analysis model

        Args:
            training_data: List of dictionaries with 'text' and 'label' keys
            model_name: Name for the trained model

        Returns:
            Path to saved model
        """
        self.logger.info(f"Training sentiment analyzer: {model_name}")

        # Prepare data
        texts = [item['text'] for item in training_data]
        labels = [item['label'] for item in training_data]

        # Convert labels to numeric
        label_map = {'negative': 0, 'neutral': 1, 'positive': 2}
        numeric_labels = [label_map.get(label, 1) for label in labels]  # Default to neutral

        # Load pre-trained model and tokenizer
        model_path = self.model_dir / f"distilbert-base-uncased_model"
        if not model_path.exists():
            self.download_pretrained_models()

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_path, num_labels=3
        )

        # Tokenize data
        encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)

        # Convert to tensors
        input_ids = torch.tensor(encodings['input_ids'])
        attention_mask = torch.tensor(encodings['attention_mask'])
        labels_tensor = torch.tensor(numeric_labels)

        # Split data
        train_inputs, val_inputs, train_labels, val_labels = train_test_split(
            input_ids, labels_tensor, test_size=0.2, random_state=42
        )
        train_masks, val_masks = train_test_split(
            attention_mask, test_size=0.2, random_state=42
        )

        # Fine-tune the model
        model.train()
        optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

        # Simple training loop (in practice, you'd want a more sophisticated approach)
        for epoch in range(3):  # Small number for demo
            optimizer.zero_grad()
            outputs = model(train_inputs, attention_mask=train_masks)
            loss = nn.CrossEntropyLoss()(outputs.logits, train_labels)
            loss.backward()
            optimizer.step()

            self.logger.info(f"Epoch {epoch + 1}, Loss: {loss.item():.4f}")

        # Evaluate
        model.eval()
        with torch.no_grad():
            val_outputs = model(val_inputs, attention_mask=val_masks)
            val_predictions = torch.argmax(val_outputs.logits, dim=1)
            accuracy = accuracy_score(val_labels.numpy(), val_predictions.numpy())

        self.logger.info(f"Validation Accuracy: {accuracy:.4f}")

        # Save model
        final_model_path = self.model_dir / f"{model_name}_final"
        final_model_path.mkdir(exist_ok=True)
        model.save_pretrained(final_model_path)
        tokenizer.save_pretrained(final_model_path)

        # Save training metadata
        metadata = {
            "model_name": model_name,
            "training_date": datetime.now().isoformat(),
            "accuracy": accuracy,
            "num_samples": len(training_data)
        }

        with open(final_model_path / "metadata.json", "w") as f:
            json.dump(metadata, f)

        log_activity("MODEL_TRAINING", f"Trained sentiment analyzer with {accuracy:.2f} accuracy", "obsidian_vault")

        return str(final_model_path)

    def train_risk_prediction_model(self, training_data: pd.DataFrame,
                                  model_name: str = "risk-predictor") -> str:
        """
        Train a risk prediction model using traditional ML

        Args:
            training_data: DataFrame with features and risk labels
            model_name: Name for the trained model

        Returns:
            Path to saved model
        """
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler

        self.logger.info(f"Training risk prediction model: {model_name}")

        # Prepare features and labels
        feature_columns = [col for col in training_data.columns if col != 'risk_label']
        X = training_data[feature_columns]
        y = training_data['risk_label']

        # Handle categorical variables
        X_encoded = pd.get_dummies(X, drop_first=True)

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_encoded)

        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_val, y_pred, average='weighted')

        self.logger.info(f"Risk Prediction Model - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")

        # Save model and scaler
        final_model_path = self.model_dir / f"{model_name}_final"
        final_model_path.mkdir(exist_ok=True)

        model_path = final_model_path / "model.pkl"
        scaler_path = final_model_path / "scaler.pkl"

        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)

        # Save feature names for inference
        feature_names_path = final_model_path / "feature_names.json"
        with open(feature_names_path, 'w') as f:
            json.dump(X_encoded.columns.tolist(), f)

        # Save training metadata
        metadata = {
            "model_name": model_name,
            "training_date": datetime.now().isoformat(),
            "accuracy": accuracy,
            "f1_score": f1,
            "precision": precision,
            "recall": recall,
            "num_samples": len(training_data)
        }

        metadata_path = final_model_path / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

        log_activity("MODEL_TRAINING", f"Trained risk predictor with {accuracy:.2f} accuracy", "obsidian_vault")

        return str(final_model_path)

    def train_recommendation_model(self, user_item_matrix: np.ndarray,
                                 model_name: str = "recommendation-engine") -> str:
        """
        Train a recommendation model using matrix factorization

        Args:
            user_item_matrix: Matrix of user-item interactions
            model_name: Name for the trained model

        Returns:
            Path to saved model
        """
        from sklearn.decomposition import NMF

        self.logger.info(f"Training recommendation model: {model_name}")

        # Use Non-negative Matrix Factorization for recommendations
        n_components = min(50, min(user_item_matrix.shape) - 1)  # Number of latent factors
        model = NMF(n_components=n_components, random_state=42, max_iter=200)

        # Fit the model
        user_features = model.fit_transform(user_item_matrix)
        item_features = model.components_

        # Save model components
        final_model_path = self.model_dir / f"{model_name}_final"
        final_model_path.mkdir(exist_ok=True)

        # Save components
        np.save(final_model_path / "user_features.npy", user_features)
        np.save(final_model_path / "item_features.npy", item_features)

        # Save model parameters
        params = {
            "n_components": n_components,
            "shape": user_item_matrix.shape,
            "training_date": datetime.now().isoformat()
        }

        with open(final_model_path / "params.json", "w") as f:
            json.dump(params, f)

        log_activity("MODEL_TRAINING", f"Trained recommendation engine with {n_components} factors", "obsidian_vault")

        return str(final_model_path)

    def evaluate_model(self, model_path: str, test_data: Any, model_type: str = "classification"):
        """
        Evaluate a trained model on test data

        Args:
            model_path: Path to the saved model
            test_data: Test data for evaluation
            model_type: Type of model for appropriate evaluation

        Returns:
            Evaluation metrics
        """
        model_path = Path(model_path)

        if model_type == "sentiment":
            # Load sentiment model
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSequenceClassification.from_pretrained(model_path)

            # Evaluate
            model.eval()
            # Implementation would go here based on specific test data format
            pass

        elif model_type == "risk":
            # Load risk prediction model
            with open(model_path / "model.pkl", 'rb') as f:
                model = pickle.load(f)
            with open(model_path / "scaler.pkl", 'rb') as f:
                scaler = pickle.load(f)

            # Evaluate on test data
            # Implementation would go here based on specific test data format
            pass

        elif model_type == "recommendation":
            # Load recommendation model
            user_features = np.load(model_path / "user_features.npy")
            item_features = np.load(model_path / "item_features.npy")

            # Evaluate recommendations
            # Implementation would go here based on specific test data format
            pass

        # Return evaluation metrics
        return {"placeholder": "evaluation_result"}

    def deploy_model(self, model_path: str, model_name: str, version: str = "1.0.0"):
        """
        Deploy a trained model to production

        Args:
            model_path: Path to the trained model
            model_name: Name of the model
            version: Version of the model
        """
        deploy_path = self.model_dir / "production" / model_name / version
        deploy_path.mkdir(parents=True, exist_ok=True)

        # In a real system, this would involve copying model files to a production location
        # and possibly updating model registries or deployment configurations
        self.logger.info(f"Deployed model {model_name} version {version} to {deploy_path}")

        log_activity("MODEL_DEPLOYMENT", f"Deployed {model_name} v{version}", "obsidian_vault")


def download_pretrained_models():
    """
    Convenience function to download pretrained models
    """
    pipeline = ModelTrainingPipeline()
    return pipeline.download_pretrained_models()


if __name__ == "__main__":
    # Example usage
    pipeline = ModelTrainingPipeline()

    # Download pretrained models
    print("Downloading pretrained models...")
    models = pipeline.download_pretrained_models()
    print(f"Downloaded models: {list(models.keys())}")