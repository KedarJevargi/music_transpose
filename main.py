# main.py
import time
from fastapi import FastAPI, status, Depends, HTTPException
from schemas.users import UserSignup, UserSignin, SignUpResponse, SignInResponse
from schemas.transpose import TransposeRequest
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from crud import user_signup, user_sign, add_user_transpose, get_transpose
from logic import HindustaniTransposer
from JWTtoken import get_current_user
from models import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "Homepage"}

@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    return user_signup(data, db)

@app.post("/signin", status_code=status.HTTP_200_OK, response_model=SignInResponse)
def signin(data: UserSignin, db: Session = Depends(get_db)):
    return user_sign(data, db)

@app.post("/transpose")
async def transpose_notes_api(
    request_data: TransposeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transposer_instance = HindustaniTransposer()
    notes = request_data.notes
    mode = request_data.mode
    semitones_to_apply = 0

    try:
        if mode == "semitone":
            semitones_to_apply = request_data.semitones
            interval_description = f"{semitones_to_apply} semitones"
        elif mode == "scale":
            from_scale = request_data.from_scale
            to_scale = request_data.to_scale
            semitones_to_apply = transposer_instance.calculate_semitone_difference_western(from_scale, to_scale)
            interval_description = f"{semitones_to_apply} semitones (from Sa={from_scale} to Sa={to_scale})"
        else:
            raise HTTPException(status_code=400, detail="Invalid transposition mode provided.")

        original_notes_list = notes.replace(',', ' ').split()
        transposed_notes_list = transposer_instance.transpose_sequence(original_notes_list, semitones_to_apply)

        add_user_transpose(str(current_user.id), " ".join(transposed_notes_list), request_data.notes, db)

        return {
            "originalNotes": " ".join(original_notes_list),
            "transposedNotes": " ".join(transposed_notes_list),
            "interval": interval_description,
            "user_id": current_user.id
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.get("/get_transpose/{user_id}")
def get_user_transpose(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="Unauthorized access to user data")
    return get_transpose(user_id, db)
