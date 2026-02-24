from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from dataset import load_data
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = FastAPI()
agent = create_agent()

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Titanic AI Chat Agent is running"}

@app.post("/chat")
def chat(query: Query):
    question = query.question.lower()
    df = load_data()

    try:
        plot_image = None

        # -----------------------------
        # 1️⃣ HANDLE SIMPLE QUERIES (NO LLM)
        # -----------------------------

        # Percentage of males
        if "percentage" in question and "male" in question:
            percentage = (df["Sex"].value_counts(normalize=True)["male"]) * 100
            response_text = f"{percentage:.2f}% of passengers were male."

        # Average fare
        elif "average" in question and "fare" in question:
            avg_fare = df["Fare"].mean()
            response_text = f"The average ticket fare was {avg_fare:.2f}."

        # Embarked counts
        elif "embarked" in question:
            counts = df["Embarked"].value_counts()
            response_text = counts.to_string()

        # Histogram of age
        elif "histogram" in question and "age" in question:
            response_text = "Here is the histogram of passenger ages."

            plt.figure()
            sns.histplot(df["Age"].dropna(), bins=20)
            plt.title("Histogram of Passenger Ages")

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plot_image = base64.b64encode(buffer.read()).decode()
            plt.close()

        # -----------------------------
        # 2️⃣ COMPLEX QUERY → CALL GEMINI
        # -----------------------------
        else:
            response_text = agent.run(query.question)

        return {
            "response": response_text,
            "plot": plot_image
        }

    except Exception as e:
        return {"error": str(e)}