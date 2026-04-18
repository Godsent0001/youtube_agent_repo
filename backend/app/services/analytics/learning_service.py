import json
from app.core.logger import logger
from app.db.session import metrics_collection
from app.services.ai.llm_client import llm_client


class LearningService:
    """
    AI learning engine that improves agent performance over time
    """

    def __init__(self):
        self.logger = logger

    def analyze_agent_performance(self, agent_id: str):

        """
        Step 1: pull historical metrics
        """

        history = list(metrics_collection.find({"agent_id": agent_id}))

        if not history:
            return {
                "insights": [],
                "recommendations": []
            }

        """
        Step 2: send to LLM for pattern analysis
        """

        messages = [
            {
                "role": "system",
                "content": """
You are an AI performance analyst for a YouTube automation system.

Your job:
- Analyze video performance data
- Identify patterns that lead to high retention and virality
- Detect weak points in content strategy
- Suggest improvements for future content generation

Return ONLY valid JSON:
{
  "insights": ["..."],
  "best_patterns": ["..."],
  "mistakes_to_avoid": ["..."],
  "recommendations": ["..."]
}
"""
            },
            {
                "role": "user",
                "content": f"""
Agent Performance Data:

{json.dumps(history, default=str, indent=2)}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            result = json.loads(response)

            self.logger.info(f"Learning analysis completed for agent {agent_id}")

            return result

        except Exception as e:
            self.logger.error(f"Learning analysis failed: {e}")

            return {
                "insights": [],
                "best_patterns": [],
                "mistakes_to_avoid": [],
                "recommendations": []
            }

    def get_best_performing_topics(self, agent_id: str):

        """
        Extract high-performing topics for future biasing
        """

        history = list(metrics_collection.find({"agent_id": agent_id}))

        topics = []

        for item in history:
            if item.get("retention_rate", 0) > 0.6:
                topics.append(item.get("topic", "unknown"))

        return list(set(topics))


learning_service = LearningService()