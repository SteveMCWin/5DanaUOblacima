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
        return s
    except ValueError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.get("/students/{id}", response_model=student.Student, status_code=status.HTTP_200_OK)
async def handle_get_students(id: int):
    try:
        s = db.retrieve_student(id)
        return s
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.post("/canteens", response_model=Canteen, status_code=status.HTTP_201_CREATED)
async def handle_post_canteens(c: Canteen, response: Response, studentId: int = Header()):
    try:
        db.store_canteen(c, studentId)
        return c
    except ValueError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.get("/canteens", response_model=list[Canteen], status_code=status.HTTP_200_OK)
async def handle_get_canteens():
    return db.retrieve_all_canteens()


@app.get("/canteens/{id}", response_model=Canteen, status_code=status.HTTP_200_OK)
async def handle_get_canteen(id: int):
    try:
        ct = db.retrieve_canteen(id)
        return ct
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.put("/canteens/{id}", response_model=Canteen, status_code=status.HTTP_200_OK)
async def handle_put_canteen(c: Canteen, id: int, response: Response, studentId: int = Header()):
    try:
        existing = db.retrieve_canteen(id)

        if c.name is not None:
            existing.name = c.name
        if c.location is not None:
            existing.location = c.location
        if c.capacity is not None:
            existing.capacity = c.capacity
        if c.workingHours is not None:
            existing.workingHours = c.workingHours

        db.update_canteen(existing, studentId)
        return existing
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.delete("/canteens/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def handle_delete_canteen(id: int, studentId: int = Header()):
    try:
        db.delete_canteen(id, studentId)
        return {}
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.post("/reservations", response_model=reservation.Reservation, status_code=status.HTTP_201_CREATED)
async def handle_post_reservations(r: reservation.Reservation, response: Response):
    try:
        db.store_reservation(r)
        return r
    except ValueError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")


@app.delete("/reservations/{id}", response_model=reservation.Reservation, status_code=status.HTTP_200_OK)
async def handle_delete_reservations(id: int, response: Response, studentId: int = Header()):
    try:
        r = db.delete_reservation(id, studentId)
        return r
    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
    except PermissionError:
        raise HTTPException(status_code=418, detail="Invalid input")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")

# @app.get("/canteens/status")
# def canteen_status(
#     startDate: dt,
#     endDate: dt,
#     startTime: t,
#     endTime: t,
#     duration: int
# ):
#     return {"message": "Haiii"}
