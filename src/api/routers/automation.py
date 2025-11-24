import os
from fastapi import APIRouter, HTTPException, status
from src.api.models.automation_model import AutomationRequest, AutomationResponse, ErrorResponse
from src.tasks.automation_task import LLMMCPAutomation
from typing import List

router = APIRouter()

@router.post(
    "/run-automation",
    response_model=List[AutomationResponse],
    responses={
        200: {
            "description": "Automation task executed successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "tool": "goto",
                            "params": {"url": "https://automationexercise.com"},
                            "reasoning": "Navigating to Automation Exercise website to find jeans"
                        },
                        {
                            "tool": "click",
                            "params": {"selector": "a[href='/products']"},
                            "reasoning": "Clicking on Products category to browse available items"
                        }
                    ]
                }
            }
        },
        400: {
            "description": "Bad Request - Invalid input parameters",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "Invalid user query provided",
                        "detail": "Query must be between 10 and 2000 characters",
                        "code": "VALIDATION_ERROR"
                    }
                }
            }
        }
    },
    summary="Find the cheapest jeans for men and add to the cart",
    description="""
    Execute an automation task to find the cheapest jeans for men on Automation Exercise and add them to the cart.

    This endpoint uses AI-powered reasoning to navigate the website, filter products by category,
    compare prices, and automatically add the cheapest jeans to your shopping cart.

    **Target Website:** https://automationexercise.com
    **Login Credentials:** therobotdriver@gmail.com / therobotdriver

    **How it works:**
    1. Navigate to Automation Exercise website
    2. Browse to the products section
    3. Filter for men's jeans category
    4. Extract and compare prices of available jeans
    5. Select the cheapest option
    6. Add it to the shopping cart
    7. Return detailed log of all actions taken

    **Example Request:**
    "Find the cheapest jeans for men and add to the cart."
    """
)
async def run_automation(request: AutomationRequest) -> List[AutomationResponse]:
    try:
        # Execute the automation task
        automation = LLMMCPAutomation(user_query=request.user_query)
        response = await automation.execute()

        # Convert to response model and return
        return [AutomationResponse(**resp) for resp in response]
    except Exception as e:
        # Handle exceptions and return error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="Automation task failed",
                detail=str(e),
                code="AUTOMATION_ERROR"
            ).dict()
        )