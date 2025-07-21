# main.py
from dotenv import load_dotenv
import os # Ensure os is imported
load_dotenv()
import time
from fastapi import FastAPI, status, Depends, HTTPException
from schemas.users import UserSignup, UserSignin, SignUpResponse, SignInResponse, ForgotPasswordRequest, ResetPasswordRequest, MessageResponse
from schemas.transpose import TransposeRequest
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from crud import user_signup, user_sign, add_user_transpose, get_transpose, create_password_reset_token, reset_user_password
from logic import HindustaniTransposer
from JWTtoken import get_current_user
from models import User, PasswordResetToken

# For email sending
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# --- Add this at the very top to load .env variables ---


# --------------------------------------------------------

# --- Replace hardcoded values with os.getenv() ---
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587)) # Default to 587 if not set
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# --------------------------------------------------

def send_password_reset_email(to_email: str, token: str):
    """
    Sends a password reset email to the specified recipient.
    Configuration details are now fetched from environment variables.
    """
    subject = "Password Reset Request for your Music Transpose Account"
    body = f"""\
    <html>
      <body>
        <p>Dear User,</p>
        <p>You have requested a password reset for your Music Transpose account.</p>
        <p>Your password reset token is: <strong>{token}</strong></p>
        <p>This token is valid for 1 hour. Please use it to set a new password.</p>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>Thank you,</p>
        <p>The Music Transpose Team</p>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL # type: ignore
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server: # type: ignore
            server.starttls() # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD) # type: ignore
            server.send_message(msg)
        print(f"Password reset email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        # Consider more robust error handling or logging in production
        return False


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

@app.post("/forgot-password", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = create_password_reset_token(request.email, db)
    if token:
        if not send_password_reset_email(to_email=request.email, token=token):
            print(f"Error sending email to {request.email}. Check SMTP configuration and environment variables.")
        return {"message": "If an account with that email exists, a password reset link has been sent."}
    else:
        return {"message": "If an account with that email exists, a password reset link has been sent."}

@app.post("/reset-password", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        reset_user_password(request.token, request.new_password, db)
        return {"message": "Your password has been reset successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

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