from fastapi import HTTPException, UploadFile
import base64

async def handle_file_upload(file: UploadFile, user_id: str) -> str:
    if not file:
        return None

    try:
        content = await file.read()
        
        if not content:
            return None
            
        base64_encoded = base64.b64encode(content).decode("utf-8")
        mime_type = file.content_type or "image/jpeg"
        data_url = f"data:{mime_type};base64,{base64_encoded}"
        
        return data_url
        
    except Exception as e:
        print(f"❌ Error encoding file: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")