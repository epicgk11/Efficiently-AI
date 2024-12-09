from pydantic import BaseModel,Field
class Step(BaseModel):
    name: str = Field(description="A brief title summarizing the step to be completed.")
    due_date: str = Field(description="The due date for completing this step, strictly formatted as MM-DD-YYYY.")
    completed:bool = Field(description="Whether the particular step has been completed infer the same from user prompt")

class Tag(BaseModel):
    name: str = Field(description="A tag or keyword to categorize and identify the task.")

class Task(BaseModel):
    name: str = Field(description="The name of the task, providing a concise summary of its purpose.")
    due_date:str = Field(description="The due date of completion of the task ")
    description: str = Field(description="A detailed explanation of the task, including its goals and requirements.")
    resources: str = Field(description="A list of resources required to complete the task and its steps, mentioned separately and clearly. Also if possible mention the task no for the resource ")
    tags: list[Tag] = Field(description="A list of tags categorizing the task for easier identification.")
    steps: list[Step] = Field(description="A list of steps involved in completing the task, with each step including its name and due date.")