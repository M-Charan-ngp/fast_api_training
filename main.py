from fastapi import FastAPI
from Routes import course_route, student_route, auth_routes
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from Middlewares.process_time import ProcessTimeMiddleware

app = FastAPI(
    title="Student Course Enrollment",
)

app.include_router(course_route.router)
app.include_router(student_route.router)
app.include_router(auth_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ProcessTimeMiddleware)

@app.get("/")
async def root():
    return {"message": "Fast API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )