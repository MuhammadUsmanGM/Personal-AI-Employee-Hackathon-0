"""
Base service class for Silver Tier Personal AI Employee System
Provides common functionality for all services
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime
import traceback

T = TypeVar('T')  # Type variable for the entity
ID = TypeVar('ID')  # Type variable for the ID

class BaseService(ABC, Generic[T]):
    """
    Abstract base service class that provides common CRUD operations
    and error handling for all services in the Silver Tier system
    """

    def __init__(self, db_session: Session, entity_class: type):
        """
        Initialize the base service

        Args:
            db_session: SQLAlchemy database session
            entity_class: The SQLAlchemy model class for this service
        """
        self.db = db_session
        self.entity_class = entity_class
        self.logger = logging.getLogger(self.__class__.__name__)

    def create(self, obj: T) -> T:
        """
        Create a new entity

        Args:
            obj: The entity to create

        Returns:
            The created entity
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            self.logger.info(f"Created {self.entity_class.__name__} with ID: {getattr(obj, 'id', 'unknown')}")
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Error creating {self.entity_class.__name__}: {str(e)}")
            raise

    def get_by_id(self, obj_id: ID) -> Optional[T]:
        """
        Get an entity by its ID

        Args:
            obj_id: The ID of the entity to retrieve

        Returns:
            The entity if found, None otherwise
        """
        try:
            obj = self.db.query(self.entity_class).filter(self.entity_class.id == obj_id).first()
            return obj
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting {self.entity_class.__name__} by ID {obj_id}: {str(e)}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all entities with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of entities
        """
        try:
            objs = self.db.query(self.entity_class).offset(skip).limit(limit).all()
            return objs
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting all {self.entity_class.__name__}: {str(e)}")
            raise

    def update(self, obj_id: ID, update_data: Dict[str, Any]) -> Optional[T]:
        """
        Update an entity

        Args:
            obj_id: The ID of the entity to update
            update_data: Dictionary of fields to update

        Returns:
            The updated entity if successful, None otherwise
        """
        try:
            obj = self.get_by_id(obj_id)
            if obj is None:
                return None

            # Update the object attributes
            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            # Update the 'updated_at' field if it exists
            if hasattr(obj, 'updated_at'):
                setattr(obj, 'updated_at', datetime.utcnow())

            self.db.commit()
            self.db.refresh(obj)
            self.logger.info(f"Updated {self.entity_class.__name__} with ID: {obj_id}")
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Error updating {self.entity_class.__name__} with ID {obj_id}: {str(e)}")
            raise

    def delete(self, obj_id: ID) -> bool:
        """
        Delete an entity

        Args:
            obj_id: The ID of the entity to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            obj = self.get_by_id(obj_id)
            if obj is None:
                return False

            self.db.delete(obj)
            self.db.commit()
            self.logger.info(f"Deleted {self.entity_class.__name__} with ID: {obj_id}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Error deleting {self.entity_class.__name__} with ID {obj_id}: {str(e)}")
            raise

    def get_by_filter(self, **filters) -> List[T]:
        """
        Get entities by filter criteria

        Args:
            **filters: Filter criteria as keyword arguments

        Returns:
            List of entities matching the criteria
        """
        try:
            query = self.db.query(self.entity_class)
            for key, value in filters.items():
                if hasattr(self.entity_class, key):
                    query = query.filter(getattr(self.entity_class, key) == value)
            return query.all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error filtering {self.entity_class.__name__}: {str(e)}")
            raise

    def exists(self, **criteria) -> bool:
        """
        Check if an entity exists based on criteria

        Args:
            **criteria: Criteria to check existence

        Returns:
            True if entity exists, False otherwise
        """
        try:
            query = self.db.query(self.entity_class)
            for key, value in criteria.items():
                if hasattr(self.entity_class, key):
                    query = query.filter(getattr(self.entity_class, key) == value)
            return query.first() is not None
        except SQLAlchemyError as e:
            self.logger.error(f"Error checking existence of {self.entity_class.__name__}: {str(e)}")
            raise

    def count(self, **filters) -> int:
        """
        Count entities based on optional filters

        Args:
            **filters: Optional filter criteria

        Returns:
            Number of entities matching the criteria
        """
        try:
            query = self.db.query(self.entity_class)
            for key, value in filters.items():
                if hasattr(self.entity_class, key):
                    query = query.filter(getattr(self.entity_class, key) == value)
            return query.count()
        except SQLAlchemyError as e:
            self.logger.error(f"Error counting {self.entity_class.__name__}: {str(e)}")
            raise

class ServiceError(Exception):
    """
    Custom exception class for service errors
    """
    def __init__(self, message: str, error_code: str = "SERVICE_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(ServiceError):
    """
    Exception raised for validation errors
    """
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")

class NotFoundError(ServiceError):
    """
    Exception raised when an entity is not found
    """
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"{entity_type} with ID {entity_id} not found", "NOT_FOUND_ERROR")

class DatabaseError(ServiceError):
    """
    Exception raised for database errors
    """
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")