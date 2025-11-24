import os
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from enum import Enum


class AutomationRequest(BaseModel):
    user_query: str = Field(
        ...,
        description="Natural language description of the automation task to perform",
        examples=[
            "Find the cheapest jeans for men and add to the cart."
        ]
    )


class AutomationResponse(BaseModel):
    tool: str = Field(
        ...,
        description="The automation tool/action that was executed",
        examples=[
            "goto",
            "click",
            "fill"
        ]
    )
    params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Parameters used for the tool execution. Structure depends on the tool type.",
        examples=[
            {"url": "https://automationexercise.com"},
            {"selector": "a[href='/products']", "text": "Products"},
            {"selector": ".productinfo p", "text": "Extract prices"}
        ]
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why this specific action was chosen and what it accomplishes",
        examples=[
            "Navigating to Automation Exercise to find men's jeans",
            "Clicking on Products category to browse available items"
        ]
    )


class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="Error message describing what went wrong",
        examples=[
            "Failed to navigate to the specified URL"
        ]
    )
    detail: Optional[str] = Field(
        default=None,
        description="Additional details about the error for debugging purposes"
    )
    code: str = Field(
        default="AUTOMATION_ERROR",
        description="Error code for programmatic error handling",
        examples=["NAVIGATION_ERROR", "ELEMENT_NOT_FOUND", "TIMEOUT_ERROR", "VALIDATION_ERROR"]
    )