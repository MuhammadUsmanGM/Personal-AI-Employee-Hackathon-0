"""
Task Recommendation Engine for Gold Tier Personal AI Employee System
Implements personalized recommendations for tasks, resources, and strategic planning
"""
import os
import json
import pickle
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF, TruncatedSVD
from sklearn.preprocessing import MinMaxScaler
import joblib

from ...utils.logger import log_activity


class TaskRecommendationEngine:
    """
    Advanced task recommendation engine for Gold Tier AI capabilities
    """

    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)

        self.content_model = None
        self.collaborative_model = None
        self.hybrid_model = None
        self.tfidf_vectorizer = None

        self.user_profiles = {}
        self.task_features = {}
        self.interaction_history = []

        self.logger = logging.getLogger(__name__)

    def build_content_based_model(self, tasks_df: pd.DataFrame) -> bool:
        """
        Build content-based recommendation model using task features

        Args:
            tasks_df: DataFrame with task information

        Returns:
            True if model built successfully, False otherwise
        """
        self.logger.info("Building content-based recommendation model...")

        try:
            # Combine text features for TF-IDF
            text_features = []
            for idx, row in tasks_df.iterrows():
                text = f"{row.get('title', '')} {row.get('description', '')} {row.get('category', '')} {row.get('source', '')}"
                text_features.append(text)

            # Create TF-IDF vectors
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )

            tfidf_matrix = self.tfidf_vectorizer.fit_transform(text_features)

            # Store the TF-IDF matrix for later use
            self.content_model = tfidf_matrix

            # Save the vectorizer
            vectorizer_path = self.model_dir / "tfidf_vectorizer.pkl"
            joblib.dump(self.tfidf_vectorizer, vectorizer_path)

            self.logger.info(f"Content-based model built with {tfidf_matrix.shape[1]} features")
            log_activity("RECOMMENDER_BUILD", f"Built content model with {tfidf_matrix.shape[1]} features", "obsidian_vault")

            return True

        except Exception as e:
            self.logger.error(f"Error building content-based model: {e}")
            return False

    def build_collaborative_filtering_model(self, interactions_df: pd.DataFrame) -> bool:
        """
        Build collaborative filtering model using user-task interactions

        Args:
            interactions_df: DataFrame with user-task interaction data

        Returns:
            True if model built successfully, False otherwise
        """
        self.logger.info("Building collaborative filtering model...")

        try:
            # Create user-item matrix
            user_item_matrix = interactions_df.pivot_table(
                index='user_id',
                columns='task_id',
                values='rating',
                fill_value=0
            )

            # Apply matrix factorization
            n_components = min(50, min(user_item_matrix.shape) - 1)
            model = NMF(n_components=n_components, random_state=42, max_iter=200)

            user_features = model.fit_transform(user_item_matrix.values)
            item_features = model.components_

            # Store model components
            self.collaborative_model = {
                'user_features': user_features,
                'item_features': item_features,
                'user_item_matrix': user_item_matrix,
                'model': model,
                'n_components': n_components
            }

            # Save model
            model_path = self.model_dir / "collaborative_model.pkl"
            joblib.dump(self.collaborative_model, model_path)

            self.logger.info(f"Collaborative filtering model built with {n_components} components")
            log_activity("RECOMMENDER_BUILD", f"Built collaborative model with {n_components} components", "obsidian_vault")

            return True

        except Exception as e:
            self.logger.error(f"Error building collaborative filtering model: {e}")
            return False

    def build_hybrid_model(self, tasks_df: pd.DataFrame, interactions_df: pd.DataFrame) -> bool:
        """
        Build hybrid recommendation model combining content and collaborative filtering

        Args:
            tasks_df: DataFrame with task information
            interactions_df: DataFrame with user-task interaction data

        Returns:
            True if model built successfully, False otherwise
        """
        self.logger.info("Building hybrid recommendation model...")

        try:
            # Build content-based model if not already built
            if self.content_model is None:
                self.build_content_based_model(tasks_df)

            # Build collaborative model if not already built
            if self.collaborative_model is None:
                self.build_collaborative_filtering_model(interactions_df)

            # Create hybrid weights
            self.hybrid_model = {
                'content_weight': 0.6,
                'collaborative_weight': 0.4,
                'content_model': self.content_model,
                'collaborative_model': self.collaborative_model
            }

            # Save hybrid model
            model_path = self.model_dir / "hybrid_model.pkl"
            joblib.dump(self.hybrid_model, model_path)

            self.logger.info("Hybrid model built successfully")
            log_activity("RECOMMENDER_BUILD", "Built hybrid recommendation model", "obsidian_vault")

            return True

        except Exception as e:
            self.logger.error(f"Error building hybrid model: {e}")
            return False

    def load_model(self, model_type: str) -> bool:
        """
        Load a trained recommendation model from disk

        Args:
            model_type: Type of model to load ('content', 'collaborative', 'hybrid')

        Returns:
            True if model loaded successfully, False otherwise
        """
        model_path = self.model_dir / f"{model_type}_model.pkl"

        if not model_path.exists():
            self.logger.warning(f"Model {model_type} not found at {model_path}")
            return False

        try:
            model_data = joblib.load(model_path)

            if model_type == 'content':
                # For content model, we need to load the vectorizer separately
                vectorizer_path = self.model_dir / "tfidf_vectorizer.pkl"
                if vectorizer_path.exists():
                    self.tfidf_vectorizer = joblib.load(vectorizer_path)
                self.content_model = model_data
            elif model_type == 'collaborative':
                self.collaborative_model = model_data
            elif model_type == 'hybrid':
                self.hybrid_model = model_data

            self.logger.info(f"Loaded {model_type} model from {model_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading {model_type} model: {e}")
            return False

    def recommend_tasks_content_based(self, user_profile: Dict[str, Any],
                                   tasks_df: pd.DataFrame,
                                   top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend tasks using content-based filtering

        Args:
            user_profile: Dictionary with user preferences
            tasks_df: DataFrame with task information
            top_k: Number of recommendations to return

        Returns:
            List of recommended tasks with scores
        """
        if self.content_model is None:
            self.load_model('content')

        if self.content_model is None or self.tfidf_vectorizer is None:
            # Return popular tasks if model not available
            return self._get_popular_tasks(tasks_df, top_k)

        try:
            # Create user preference vector based on user profile
            user_text = f"{user_profile.get('preferred_categories', [])} {user_profile.get('interests', [])} {user_profile.get('skills', [])}"

            # Transform user preferences using the fitted vectorizer
            user_vector = self.tfidf_vectorizer.transform([user_text])

            # Transform task features using the same vectorizer
            task_texts = []
            for idx, row in tasks_df.iterrows():
                text = f"{row.get('title', '')} {row.get('description', '')} {row.get('category', '')} {row.get('source', '')}"
                task_texts.append(text)

            task_vectors = self.tfidf_vectorizer.transform(task_texts)

            # Calculate similarities
            similarities = cosine_similarity(user_vector, task_vectors).flatten()

            # Get top-k recommendations
            top_indices = similarities.argsort()[-top_k:][::-1]

            recommendations = []
            for idx in top_indices:
                if idx < len(tasks_df):
                    task_row = tasks_df.iloc[idx]
                    recommendations.append({
                        'task_id': task_row.get('id', idx),
                        'title': task_row.get('title', ''),
                        'description': task_row.get('description', ''),
                        'category': task_row.get('category', ''),
                        'similarity_score': float(similarities[idx]),
                        'recommended_by': 'content_based'
                    })

            return recommendations

        except Exception as e:
            self.logger.error(f"Error in content-based recommendation: {e}")
            return self._get_popular_tasks(tasks_df, top_k)

    def recommend_tasks_collaborative(self, user_id: str,
                                   tasks_df: pd.DataFrame,
                                   top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend tasks using collaborative filtering

        Args:
            user_id: User ID for whom to make recommendations
            tasks_df: DataFrame with task information
            top_k: Number of recommendations to return

        Returns:
            List of recommended tasks with scores
        """
        if self.collaborative_model is None:
            self.load_model('collaborative')

        if self.collaborative_model is None:
            # Return popular tasks if model not available
            return self._get_popular_tasks(tasks_df, top_k)

        try:
            user_item_matrix = self.collaborative_model['user_item_matrix']
            user_features = self.collaborative_model['user_features']
            item_features = self.collaborative_model['item_features']

            # Check if user exists in the model
            if user_id not in user_item_matrix.index:
                # If new user, return popular tasks
                return self._get_popular_tasks(tasks_df, top_k)

            # Get user index
            user_idx = user_item_matrix.index.get_loc(user_id)

            # Calculate user-task scores
            user_vector = user_features[user_idx].reshape(1, -1)
            scores = np.dot(user_vector, item_features)[0]

            # Get top-k task indices
            top_indices = scores.argsort()[-top_k:][::-1]

            recommendations = []
            for idx in top_indices:
                if idx < len(tasks_df):
                    task_row = tasks_df.iloc[idx]
                    recommendations.append({
                        'task_id': task_row.get('id', user_item_matrix.columns[idx]),
                        'title': task_row.get('title', ''),
                        'description': task_row.get('description', ''),
                        'category': task_row.get('category', ''),
                        'collaborative_score': float(scores[idx]),
                        'recommended_by': 'collaborative_filtering'
                    })

            return recommendations

        except Exception as e:
            self.logger.error(f"Error in collaborative filtering recommendation: {e}")
            return self._get_popular_tasks(tasks_df, top_k)

    def recommend_tasks_hybrid(self, user_id: str,
                             user_profile: Dict[str, Any],
                             tasks_df: pd.DataFrame,
                             top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend tasks using hybrid approach combining content and collaborative filtering

        Args:
            user_id: User ID for whom to make recommendations
            user_profile: Dictionary with user preferences
            tasks_df: DataFrame with task information
            top_k: Number of recommendations to return

        Returns:
            List of recommended tasks with scores
        """
        if self.hybrid_model is None:
            self.load_model('hybrid')

        if self.hybrid_model is None:
            # Fall back to content-based if hybrid model not available
            return self.recommend_tasks_content_based(user_profile, tasks_df, top_k)

        try:
            # Get content-based recommendations
            content_recs = self.recommend_tasks_content_based(user_profile, tasks_df, top_k * 2)

            # Get collaborative recommendations
            collab_recs = self.recommend_tasks_collaborative(user_id, tasks_df, top_k * 2)

            # Combine recommendations with weights
            all_recs = {}

            # Add content-based scores
            content_weight = self.hybrid_model['content_weight']
            for rec in content_recs:
                task_id = rec['task_id']
                if task_id not in all_recs:
                    all_recs[task_id] = {
                        'task_id': task_id,
                        'title': rec['title'],
                        'description': rec['description'],
                        'category': rec['category'],
                        'content_score': rec['similarity_score'] * content_weight,
                        'collaborative_score': 0.0
                    }
                else:
                    all_recs[task_id]['content_score'] = rec['similarity_score'] * content_weight

            # Add collaborative scores
            collab_weight = self.hybrid_model['collaborative_weight']
            for rec in collab_recs:
                task_id = rec['task_id']
                if task_id not in all_recs:
                    all_recs[task_id] = {
                        'task_id': task_id,
                        'title': rec['title'],
                        'description': rec['description'],
                        'category': rec['category'],
                        'content_score': 0.0,
                        'collaborative_score': rec['collaborative_score'] * collab_weight
                    }
                else:
                    all_recs[task_id]['collaborative_score'] = rec['collaborative_score'] * collab_weight

            # Calculate hybrid scores
            for task_id, rec in all_recs.items():
                rec['hybrid_score'] = rec['content_score'] + rec['collaborative_score']
                rec['recommended_by'] = 'hybrid'

            # Sort by hybrid score and return top-k
            sorted_recs = sorted(all_recs.values(), key=lambda x: x['hybrid_score'], reverse=True)
            top_recs = sorted_recs[:top_k]

            return top_recs

        except Exception as e:
            self.logger.error(f"Error in hybrid recommendation: {e}")
            # Fall back to content-based recommendation
            return self.recommend_tasks_content_based(user_profile, tasks_df, top_k)

    def _get_popular_tasks(self, tasks_df: pd.DataFrame, top_k: int) -> List[Dict[str, Any]]:
        """
        Get popular tasks as fallback when models are not available

        Args:
            tasks_df: DataFrame with task information
            top_k: Number of tasks to return

        Returns:
            List of popular tasks
        """
        # Sort by some popularity metric (in a real system, this would be based on actual usage data)
        if 'popularity_score' in tasks_df.columns:
            sorted_tasks = tasks_df.sort_values('popularity_score', ascending=False)
        elif 'created_at' in tasks_df.columns:
            # Recent tasks as proxy for popularity
            sorted_tasks = tasks_df.sort_values('created_at', ascending=False)
        else:
            # Just return first few tasks
            sorted_tasks = tasks_df.head(top_k)

        recommendations = []
        for idx, row in sorted_tasks.head(top_k).iterrows():
            recommendations.append({
                'task_id': row.get('id', idx),
                'title': row.get('title', ''),
                'description': row.get('description', ''),
                'category': row.get('category', ''),
                'hybrid_score': 0.5,  # Default score
                'recommended_by': 'fallback_popular'
            })

        return recommendations

    def update_user_profile(self, user_id: str, interaction: Dict[str, Any]):
        """
        Update user profile based on interaction

        Args:
            user_id: User ID
            interaction: Interaction data containing feedback
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'preferred_categories': [],
                'interests': [],
                'skills': [],
                'interaction_history': []
            }

        # Update profile based on interaction
        if 'category' in interaction:
            category = interaction['category']
            if category not in self.user_profiles[user_id]['preferred_categories']:
                self.user_profiles[user_id]['preferred_categories'].append(category)

        if 'feedback' in interaction and interaction['feedback'] == 'positive':
            # Add positive feedback to interests
            if 'task_description' in interaction:
                # Simple keyword extraction
                keywords = interaction['task_description'].split()[:5]  # First 5 words
                for keyword in keywords:
                    if keyword.lower() not in self.user_profiles[user_id]['interests']:
                        self.user_profiles[user_id]['interests'].append(keyword.lower())

        # Add interaction to history
        self.user_profiles[user_id]['interaction_history'].append(interaction)

        # Log the update
        log_activity("USER_PROFILE_UPDATE", f"Updated profile for user {user_id}", "obsidian_vault")

    def recommend_strategic_objectives(self, user_profile: Dict[str, Any],
                                    objectives_df: pd.DataFrame,
                                    top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend strategic objectives based on user profile and preferences

        Args:
            user_profile: Dictionary with user preferences
            objectives_df: DataFrame with strategic objectives
            top_k: Number of recommendations to return

        Returns:
            List of recommended strategic objectives
        """
        try:
            recommendations = []

            # Simple keyword matching approach for strategic objectives
            for idx, row in objectives_df.iterrows():
                objective_text = f"{row.get('title', '')} {row.get('description', '')} {row.get('category', '')}"

                # Calculate relevance score based on user profile
                relevance_score = 0.0

                # Match preferred categories
                if 'preferred_categories' in user_profile:
                    for cat in user_profile['preferred_categories']:
                        if cat.lower() in objective_text.lower():
                            relevance_score += 0.3

                # Match interests
                if 'interests' in user_profile:
                    for interest in user_profile['interests']:
                        if interest.lower() in objective_text.lower():
                            relevance_score += 0.2

                # Normalize score
                relevance_score = min(1.0, relevance_score)

                if relevance_score > 0:
                    recommendations.append({
                        'objective_id': row.get('id', idx),
                        'title': row.get('title', ''),
                        'description': row.get('description', ''),
                        'priority': row.get('priority', 'medium'),
                        'relevance_score': relevance_score,
                        'recommended_by': 'strategic_objective_matcher'
                    })

            # Sort by relevance and return top-k
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            return recommendations[:top_k]

        except Exception as e:
            self.logger.error(f"Error in strategic objective recommendation: {e}")
            return []

    def recommend_resources(self, user_profile: Dict[str, Any],
                          resource_pool: List[Dict[str, Any]],
                          task_requirements: Dict[str, Any],
                          top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend resources based on user profile and task requirements

        Args:
            user_profile: Dictionary with user preferences
            resource_pool: List of available resources
            task_requirements: Dictionary with task requirements
            top_k: Number of recommendations to return

        Returns:
            List of recommended resources
        """
        try:
            recommendations = []

            for resource in resource_pool:
                # Calculate compatibility score
                compatibility_score = 0.0

                # Match skills
                user_skills = user_profile.get('skills', [])
                resource_skills = resource.get('skills', [])

                if isinstance(resource_skills, str):
                    resource_skills = [resource_skills]

                if isinstance(user_skills, str):
                    user_skills = [user_skills]

                # Calculate skill overlap
                skill_overlap = len(set(user_skills) & set(resource_skills))
                if skill_overlap > 0:
                    compatibility_score += 0.4 * (skill_overlap / len(set(user_skills) | set(resource_skills)))

                # Match availability
                if 'availability' in resource and resource['availability'] == 'available':
                    compatibility_score += 0.3

                # Match expertise level
                if ('expertise_level' in resource and
                    'required_expertise' in task_requirements and
                    resource['expertise_level'] >= task_requirements['required_expertise']):
                    compatibility_score += 0.3

                # Ensure score is between 0 and 1
                compatibility_score = min(1.0, compatibility_score)

                if compatibility_score > 0:
                    recommendations.append({
                        'resource_id': resource.get('id'),
                        'resource_name': resource.get('name', ''),
                        'resource_type': resource.get('type', ''),
                        'compatibility_score': compatibility_score,
                        'recommended_by': 'resource_matcher'
                    })

            # Sort by compatibility and return top-k
            recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
            return recommendations[:top_k]

        except Exception as e:
            self.logger.error(f"Error in resource recommendation: {e}")
            return []

    def recommend_risk_mitigation(self, risk_assessment: Dict[str, Any],
                                mitigation_strategies: List[Dict[str, Any]],
                                top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend risk mitigation strategies based on risk assessment

        Args:
            risk_assessment: Dictionary with risk assessment data
            mitigation_strategies: List of available mitigation strategies
            top_k: Number of recommendations to return

        Returns:
            List of recommended mitigation strategies
        """
        try:
            recommendations = []

            for strategy in mitigation_strategies:
                # Calculate relevance score
                relevance_score = 0.0

                # Match risk category
                if (risk_assessment.get('risk_category') == strategy.get('applicable_risk_category')):
                    relevance_score += 0.5

                # Match risk level
                risk_level_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
                assessment_level = risk_level_map.get(risk_assessment.get('risk_level'), 0)
                strategy_level = risk_level_map.get(strategy.get('target_risk_level'), 0)

                if assessment_level == strategy_level:
                    relevance_score += 0.3
                elif abs(assessment_level - strategy_level) == 1:
                    relevance_score += 0.1

                # Match impact type
                if (risk_assessment.get('impact_type') == strategy.get('target_impact_type')):
                    relevance_score += 0.2

                # Ensure score is between 0 and 1
                relevance_score = min(1.0, relevance_score)

                if relevance_score > 0:
                    recommendations.append({
                        'strategy_id': strategy.get('id'),
                        'strategy_name': strategy.get('name', ''),
                        'strategy_description': strategy.get('description', ''),
                        'relevance_score': relevance_score,
                        'recommended_by': 'risk_mitigation_matcher'
                    })

            # Sort by relevance and return top-k
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            return recommendations[:top_k]

        except Exception as e:
            self.logger.error(f"Error in risk mitigation recommendation: {e}")
            return []

    def generate_personalized_dashboard_widgets(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized dashboard widgets based on user profile

        Args:
            user_profile: Dictionary with user preferences

        Returns:
            List of recommended dashboard widgets
        """
        try:
            widgets = []

            # Based on user role and preferences, recommend relevant widgets
            role = user_profile.get('role', 'general').lower()
            preferred_categories = user_profile.get('preferred_categories', [])

            # Task-related widgets
            widgets.append({
                'widget_type': 'task_overview',
                'title': 'Task Overview',
                'position': {'row': 0, 'col': 0, 'width': 4, 'height': 3},
                'configuration': {
                    'show_categories': preferred_categories if preferred_categories else ['all'],
                    'show_priorities': ['high', 'critical']
                },
                'relevance_score': 0.9
            })

            # If user has strategic responsibilities
            if 'strategic' in role or 'manager' in role or 'director' in role:
                widgets.append({
                    'widget_type': 'strategic_goals',
                    'title': 'Strategic Objectives',
                    'position': {'row': 0, 'col': 4, 'width': 4, 'height': 3},
                    'configuration': {
                        'show_timeline': True,
                        'show_progress': True
                    },
                    'relevance_score': 0.8
                })

            # If user has analytical responsibilities
            if 'analyst' in role or 'data' in role or 'finance' in role:
                widgets.append({
                    'widget_type': 'analytics',
                    'title': 'Performance Analytics',
                    'position': {'row': 0, 'col': 8, 'width': 4, 'height': 3},
                    'configuration': {
                        'chart_type': 'line',
                        'time_period': 'last_month'
                    },
                    'relevance_score': 0.85
                })

            # Add risk monitoring widget if user has oversight responsibilities
            if 'manager' in role or 'director' in role or 'risk' in role:
                widgets.append({
                    'widget_type': 'risk_monitor',
                    'title': 'Risk Monitor',
                    'position': {'row': 1, 'col': 0, 'width': 6, 'height': 3},
                    'configuration': {
                        'show_levels': ['high', 'critical'],
                        'auto_refresh': True
                    },
                    'relevance_score': 0.75
                })

            # Add compliance monitor if relevant to role
            if 'compliance' in role or 'legal' in role or 'audit' in role:
                widgets.append({
                    'widget_type': 'compliance_tracker',
                    'title': 'Compliance Tracker',
                    'position': {'row': 1, 'col': 6, 'width': 6, 'height': 3},
                    'configuration': {
                        'show_expired': True,
                        'show_due_soon': True
                    },
                    'relevance_score': 0.8
                })

            return widgets

        except Exception as e:
            self.logger.error(f"Error generating dashboard widgets: {e}")
            # Return default widgets
            return [
                {
                    'widget_type': 'task_overview',
                    'title': 'Task Overview',
                    'position': {'row': 0, 'col': 0, 'width': 12, 'height': 3},
                    'configuration': {
                        'show_categories': ['all'],
                        'show_priorities': ['all']
                    },
                    'relevance_score': 0.5
                }
            ]

    def get_recommendation_explanation(self, recommendation: Dict[str, Any]) -> str:
        """
        Generate explanation for a recommendation

        Args:
            recommendation: Recommendation dictionary

        Returns:
            Explanation string
        """
        try:
            if 'recommended_by' in recommendation:
                method = recommendation['recommended_by']

                if method == 'content_based':
                    return f"This task was recommended based on its similarity to tasks you've engaged with before."
                elif method == 'collaborative_filtering':
                    return f"This task was recommended because users with similar profiles found it valuable."
                elif method == 'hybrid':
                    return f"This task was recommended using a combination of content similarity and user behavior patterns."
                elif method == 'strategic_objective_matcher':
                    return f"This strategic objective aligns with your stated interests and professional goals."
                elif method == 'resource_matcher':
                    return f"This resource matches your requirements and skill profile."
                elif method == 'risk_mitigation_matcher':
                    return f"This mitigation strategy is appropriate for the identified risk level and category."
                else:
                    return f"This recommendation was generated using {method.replace('_', ' ').title()} method."
            else:
                return "This recommendation was generated based on your profile and system patterns."
        except Exception:
            return "This recommendation was generated by the AI system."


# Example usage and testing
if __name__ == "__main__":
    # Initialize the recommendation engine
    recommender = TaskRecommendationEngine()

    # Create sample data for testing
    np.random.seed(42)

    # Sample tasks data
    n_tasks = 100
    sample_tasks = {
        'id': [f'task_{i}' for i in range(n_tasks)],
        'title': [f'Task {i} Title' for i in range(n_tasks)],
        'description': [f'Description for task {i} involving various activities' for i in range(n_tasks)],
        'category': np.random.choice(['email', 'file', 'calendar', 'crm', 'strategic', 'compliance'], n_tasks),
        'source': np.random.choice(['gmail', 'whatsapp', 'filesystem', 'calendar', 'api'], n_tasks),
        'priority': np.random.choice(['low', 'medium', 'high', 'critical'], n_tasks),
        'created_at': pd.date_range(start='2023-01-01', periods=n_tasks, freq='D')
    }
    tasks_df = pd.DataFrame(sample_tasks)

    # Sample interactions data
    n_interactions = 50
    sample_interactions = {
        'user_id': np.random.choice(['user1', 'user2', 'user3'], n_interactions),
        'task_id': np.random.choice([f'task_{i}' for i in range(n_tasks)], n_interactions),
        'rating': np.random.randint(1, 6, n_interactions),
        'timestamp': pd.date_range(start='2023-01-01', periods=n_interactions, freq='H')
    }
    interactions_df = pd.DataFrame(sample_interactions)

    print("Building recommendation models...")

    # Build content-based model
    content_success = recommender.build_content_based_model(tasks_df)
    print(f"Content model built: {content_success}")

    # Build collaborative filtering model
    collab_success = recommender.build_collaborative_filtering_model(interactions_df)
    print(f"Collaborative model built: {collab_success}")

    # Build hybrid model
    hybrid_success = recommender.build_hybrid_model(tasks_df, interactions_df)
    print(f"Hybrid model built: {hybrid_success}")

    # Test recommendations
    print("\nTesting recommendations...")

    user_profile = {
        'preferred_categories': ['strategic', 'compliance'],
        'interests': ['planning', 'optimization', 'analysis'],
        'skills': ['strategic', 'analytical', 'leadership'],
        'role': 'manager'
    }

    # Test content-based recommendations
    content_recs = recommender.recommend_tasks_content_based(user_profile, tasks_df, top_k=3)
    print(f"Content-based recommendations: {len(content_recs)} found")
    for rec in content_recs[:2]:
        print(f"  - {rec['title']}: {rec['similarity_score']:.3f}")

    # Test collaborative recommendations
    collab_recs = recommender.recommend_tasks_collaborative('user1', tasks_df, top_k=3)
    print(f"Collaborative recommendations: {len(collab_recs)} found")
    for rec in collab_recs[:2]:
        print(f"  - {rec['title']}: {rec['collaborative_score']:.3f}")

    # Test hybrid recommendations
    hybrid_recs = recommender.recommend_tasks_hybrid('user1', user_profile, tasks_df, top_k=3)
    print(f"Hybrid recommendations: {len(hybrid_recs)} found")
    for rec in hybrid_recs[:2]:
        print(f"  - {rec['title']}: {rec['hybrid_score']:.3f}")

    # Test strategic objective recommendations
    sample_objectives = {
        'id': ['obj_1', 'obj_2', 'obj_3'],
        'title': ['Increase Market Share', 'Improve Operational Efficiency', 'Enhance Customer Satisfaction'],
        'description': ['Expand market presence in key segments', 'Optimize business processes', 'Improve customer experience'],
        'category': ['growth', 'efficiency', 'customer'],
        'priority': ['high', 'medium', 'high']
    }
    objectives_df = pd.DataFrame(sample_objectives)

    strategic_recs = recommender.recommend_strategic_objectives(user_profile, objectives_df, top_k=2)
    print(f"Strategic recommendations: {len(strategic_recs)} found")
    for rec in strategic_recs:
        print(f"  - {rec['title']}: {rec['relevance_score']:.3f}")

    # Test dashboard widget recommendations
    widgets = recommender.generate_personalized_dashboard_widgets(user_profile)
    print(f"Dashboard widgets: {len(widgets)} recommended")
    for widget in widgets:
        print(f"  - {widget['title']} ({widget['widget_type']})")