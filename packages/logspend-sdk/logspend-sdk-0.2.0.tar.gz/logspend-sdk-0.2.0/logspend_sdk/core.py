import time
import uuid
import asyncio
import httpx

from logspend_sdk.constants import SDK_VERSION


class LogBuilder:
    def __init__(self, input_data):
        self.data = {
            "input": input_data,
            "output": None,
            "custom_properties": None,
            "start_time_ms": int(time.time() * 1000),
            "end_time_ms": None,
            "request_id": str(uuid.uuid4()),
        }

    def set_output(self, output_data):
        if not self.data["output"]:
            self.data["output"] = output_data
            self.data["end_time_ms"] = int(time.time() * 1000)
        return self

    def set_custom_properties(self, custom_properties_data):
        self.data["custom_properties"] = custom_properties_data
        return self

    def build(self):
        return self.data


class LogSpendLogger:
    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id

    async def send(self, data):
        # Check if input and output are defined
        if not data.get("input") or not data.get("output"):
            print("Error: Input or Output data missing. Will skip sending the log.")
            return
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "LogSpend-SDK-Version": SDK_VERSION,
            "LogSpend-Project-ID": self.project_id,
            "LogSpend-Request-ID": data["request_id"]
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("https://api.logspend.com/llm/v1/log", headers=headers, json=data)
                return data["request_id"]
            except Exception as e:
                print(f"Error sending data: {e}")