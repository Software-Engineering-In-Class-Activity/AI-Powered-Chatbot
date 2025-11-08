# Context: bundles the conversation, user, analysis, and service layer for handlers.
from typing import Any
from src.models.conversation import Conversation
from src.models.user import User
from src.models.analysis_result import AnalysisResult
from src.services.service_layer import ServiceLayer


class Context:
    # Contains conversation, user info, NLP result, and service access for handlers.

    def __init__(self, conversation: Conversation, user: User, 
                 analysis: AnalysisResult, services: ServiceLayer):
        # Store the objects handlers need to make decisions and call services.
        self.conversation: Conversation = conversation
        self.user: User = user
        self.analysis: AnalysisResult = analysis
        self.services: ServiceLayer = services
