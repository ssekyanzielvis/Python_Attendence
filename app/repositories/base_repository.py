from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..config.database import Base

class BaseRepository(ABC):
    def __init__(self, db: Session, model: Base):
        self.db = db
        self.model = model
    
    def create(self, obj_data: Dict[str, Any]) -> Base:
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, obj_id: str) -> Optional[Base]:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Base]:
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, obj_id: str, obj_data: Dict[str, Any]) -> Optional[Base]:
        db_obj = self.get_by_id(obj_id)
        if db_obj:
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, obj_id: str) -> bool:
        db_obj = self.get_by_id(obj_id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        return self.db.query(self.model).count()
    
    def exists(self, **filters) -> bool:
        query = self.db.query(self.model)
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None
