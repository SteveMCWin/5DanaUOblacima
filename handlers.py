from fastapi import FastAPI, Response, status, HTTPException, Header
import datetime as dt
from models import database, student, reservation
from models.canteen import Canteen


app = FastAPI()
db = database.DB()


@app.get("/")
async def home():
    return {"message": "Haiii"}


@app.post("/students", response_model=student.Student, status_code=status.HTTP_201_CREATED)
async def handle_post_students(s: student.Student, response: Response):
    try:
        db.store_student(s)
    except ValueError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    return s


@app.get("/students/{id}", response_model=student.Student, status_code=status.HTTP_200_OK)
async def handle_get_students(id: int):
    try:
        s = db.retrieve_student(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    return s


@app.post("/canteens", response_model=Canteen, status_code=status.HTTP_201_CREATED)
async def handle_post_canteens(c: Canteen, response: Response, studentId: int = Header()):
    try:
        s = db.retrieve_student(studentId)
    except ValueError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")

    try:
        db.store_canteen(c, s)
    except ValueError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    return c


@app.get("/canteens", response_model=list[Canteen], status_code=status.HTTP_200_OK)
async def handle_get_canteens():
    return db.retrieve_all_canteens()


@app.get("/canteens/{id}")
async def handle_get_canteen(id: int):
    return {"message": "Haiii"}


@app.put("/canteens/{id}")
async def handle_put_canteen(id: int):
    return {"message": "Haiii"}


@app.delete("/canteens/{id}")
async def handle_delete_canteen(id: int):
    return {"message": "Haiii"}


# @app.get("/canteens/status")
# def canteen_status(
#     startDate: dt,
#     endDate: dt,
#     startTime: t,
#     endTime: t,
#     duration: int
# ):
#     return {"message": "Haiii"}
