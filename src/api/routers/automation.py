from fastapi import APIRouter
from src.api.models.automation_model import AutomationRequest, AutomationResponse
from src.tasks.automation_task import LLMMCPAutomation

router = APIRouter()

@router.post("/run-automation", response_model=list[AutomationResponse])
async def run_automation(request: AutomationRequest):
    try:
        automation = LLMMCPAutomation(user_query=request.user_query)
        
        response = await automation.execute()
        
        return [AutomationResponse(**resp) for resp in response]
    
    except Exception as e:
        return {"error": str(e)}