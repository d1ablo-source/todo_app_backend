# from sqlalchemy.orm import Session
# from sqlalchemy import select

# from src.models.category import CategoryORM

# class CategoryRepository:
#     def __init__(self, db: Session) -> None:
#         self.db = db

#     def get_all(self) -> list[CategoryORM]:
#         return self.db.scalars(select(CategoryORM)).all()
    
#     def get_by_id(self, id: str) -> CategoryORM:
#         return self.db.get(CategoryORM, id)
    
#     def create(self, name: str) -> CategoryORM:    
#         new_category = CategoryORM(name=name)
#         self.db.add(new_category)
#         self.db.commit()

#     def delete(self, category: CategoryORM) -> None:
#         self.db.delete(category)