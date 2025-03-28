import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# محاولة تحميل المتغيرات البيئية من ملف .env (إذا وجد)
load_dotenv()

# تهيئة المفتاح من متغيرات البيئة (أكثر أمانًا)
openai_api_key = os.environ.get("OPENAI_API_KEY", "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")

# تهيئة العميل
client = OpenAI(api_key=openai_api_key)

# إنشاء تطبيق FastAPI
app = FastAPI(title="شات بوت API", 
              description="واجهة برمجة تطبيقات للتفاعل مع شات بوت ذكي",
              version="1.0.0")

# إضافة CORS ميدلوير للسماح بالطلبات من تطبيق Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في بيئة الإنتاج، حدد أصول محددة بدلاً من "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تعريف نموذج البيانات للطلب
class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"

# تعريف نموذج البيانات للاستجابة
class ChatResponse(BaseModel):
    response: str

def chat_with_gpt(prompt, model="gpt-3.5-turbo"):
    """
    دالة للتواصل مع نموذج GPT
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "أنت مساعد مفيد وودود."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ في OpenAI API: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "مرحبًا بك في شات بوت API!"}

@app.post("/chat", response_model=ChatResponse)
def create_chat(request: ChatRequest):
    """
    نقطة نهاية API لإرسال رسائل إلى الشات بوت والحصول على استجابة
    """
    response_text = chat_with_gpt(request.message, request.model)
    return ChatResponse(response=response_text)

# تشغيل التطبيق مع Uvicorn إذا تم تنفيذ هذا الملف مباشرة
if __name__ == "__main__":
    import uvicorn
    # الحصول على المنفذ من متغيرات البيئة للتوافق مع خدمات الاستضافة
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)