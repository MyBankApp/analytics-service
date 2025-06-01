from fastapi import APIRouter, Response
from service.generatorReportService import service

reportController = APIRouter()

@reportController.get("/{sender_id}")
async def get_report(sender_id: int):
    result = await service.generate_report(sender_id=sender_id)

    if "error" in result:
        return {"detail": result["error"]}
    
    return Response(
        content=result["content"],
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={result['filename']}",
            "Content-Type": "application/pdf"
        }
    )