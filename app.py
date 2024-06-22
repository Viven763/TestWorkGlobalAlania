from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import login_router
from users.router import users_router
from equipment.router import equipment_router
from terminal.router import terminal_router

app = FastAPI(title="TestWorkGlobalAlania",
              description="Тестовое задание",
              version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(login_router)
app.include_router(users_router)
app.include_router(equipment_router)
app.include_router(terminal_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)