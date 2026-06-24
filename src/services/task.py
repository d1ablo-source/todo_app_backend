# from sqlalchemy.orm import Session
# from src.repositories.task import TaskRepository
# from src.schemas.task import Task_Create, TaskSchema, TaskUpdate


# class TaskService:
#     def __init__(self, db: Session):
#         self.db = db
#         self.task_repository = TaskRepository(db)

#     def list_tasks(self) -> list[TaskSchema]:
#         task_orm = self.task_repository.get_all()
#         return [TaskSchema.model_validate(task) for task in task_orm]
    
#     def create_task(self, task_create: Task_Create) -> TaskSchema:
#         task = self.task_repository.create(title=task_create.title)
#         self.db.commit()
#         return task
    
#     def update_task(self, task_update: TaskUpdate) -> TaskSchema:
#         ...
    