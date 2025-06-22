from fastapi import FastAPI

from app.api.v1 import (auth_routes, email_routes, task_list_routes,
                        task_routes, user_routes)

app = FastAPI(title="Crehana App")

app.include_router(task_routes.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(
    task_list_routes.router, prefix="/api/v1/task-lists", tags=["Task Lists"]
)
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(email_routes.router, prefix="/api/v1/email", tags=["Email"])
