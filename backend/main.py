
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crew_db = []
schedule_db = []
monitoring_db = []

class Crew(BaseModel):
    id: int
    name: str
    role: str
    station: List[str]
    is_awol: bool = False
    is_trainee: bool = False

class Shift(BaseModel):
    crew_id: int
    date: str
    shift: str
    man_hours: float
    break_hours: float = 1.0

class MonitoringEntry(BaseModel):
    crew_id: int
    date: str
    shift: str
    is_awol: bool

@app.get("/api/crew")
def get_crew():
    return [crew for crew in crew_db if not crew['is_awol']]

@app.post("/api/crew")
def add_crew(crew: Crew):
    crew_db.append(crew.dict())
    return {"message": "Crew added"}

@app.get("/api/schedule")
def get_schedule():
    return schedule_db

@app.post("/api/schedule")
def add_schedule(shift: Shift):
    crew = next((c for c in crew_db if c['id'] == shift.crew_id), None)
    if not crew or crew['is_awol']:
        raise HTTPException(status_code=400, detail="Crew is AWOL or not found")

    past_shifts = [s for s in schedule_db if s['crew_id'] == shift.crew_id]
    dates = [datetime.datetime.strptime(s['date'], "%Y-%m-%d") for s in past_shifts]
    dates = sorted(dates)
    if len(dates) >= 6:
        delta_days = (datetime.datetime.strptime(shift.date, "%Y-%m-%d") - dates[-6]).days
        if delta_days < 6:
            raise HTTPException(status_code=400, detail="Max 6 consecutive duty days exceeded")

    schedule_db.append(shift.dict())
    return {"message": "Schedule added"}

@app.get("/api/monitoring")
def get_monitoring():
    return monitoring_db

@app.post("/api/monitoring")
def add_monitoring(entry: MonitoringEntry):
    monitoring_db.append(entry.dict())
    return {"message": "Monitoring updated"}

@app.get("/api/dailies")
def get_dailies(target_sales: float):
    total_mh = sum([s['man_hours'] for s in schedule_db if not any(role in crew_db[s['crew_id']]['role'] for role in ["UM", "CNC", "UM/Kitchen"])])
    result = (total_mh * 75 / target_sales) * 100
    return {"dailies": round(result, 2)}
