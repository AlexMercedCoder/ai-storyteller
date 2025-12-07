import os
from typing import Optional, List, Dict, Any
import json
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AIGateway:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self._setup_clients()

    def _setup_clients(self):
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)

        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = Anthropic(api_key=anthropic_key)

        # Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)

    def generate_response(
        self, 
        prompt: str, 
        system_instruction: str = "",
        provider: str = "openai", 
        model: str = "gpt-4o",
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Any:
        
        full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt

        try:
            if provider == "openai":
                return self._generate_openai(prompt, system_instruction, model, tools)
            elif provider == "anthropic":
                return self._generate_anthropic(prompt, system_instruction, model, tools)
            elif provider == "gemini":
                return self._generate_gemini(prompt, system_instruction, model, tools)
            else:
                return f"Error: Unknown provider '{provider}'"
        except Exception as e:
            return f"Error generating response with {provider}: {str(e)}"

    def _generate_openai(self, prompt: str, system_instruction: str, model: str, tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        if not self.openai_client:
            return "Error: OpenAI API key not found."
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        kwargs = {}
        if tools:
            # Convert internal tool format to OpenAI format
            openai_tools = []
            for tool in tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {"type": "object", "properties": {}})
                    }
                })
            kwargs["tools"] = openai_tools

        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        
        message = response.choices[0].message
        if message.tool_calls:
            return message.tool_calls
        return message.content

    def _generate_anthropic(self, prompt: str, system_instruction: str, model: str, tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        if not self.anthropic_client:
            return "Error: Anthropic API key not found."

        kwargs = {}
        if tools:
            anthropic_tools = []
            for tool in tools:
                anthropic_tools.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "input_schema": tool.get("parameters", {"type": "object", "properties": {}})
                })
            kwargs["tools"] = anthropic_tools

        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            system=system_instruction,
            messages=[
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )
        
        # Check for tool use
        for content in response.content:
            if content.type == "tool_use":
                return [{"type": "function", "function": {"name": content.name, "arguments": json.dumps(content.input)}, "id": content.id}]
        
        return response.content[0].text

    def _generate_gemini(self, prompt: str, system_instruction: str, model: str, tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        if not os.getenv("GEMINI_API_KEY"):
            return "Error: Gemini API key not found."
        
        # Gemini handling might vary slightly by model version
        # For simplicity, we are not implementing native tool calling for Gemini in this iteration
        # as it requires more complex setup with FunctionDeclaration objects
        
        model_instance = genai.GenerativeModel(model)
        if system_instruction:
             model_instance = genai.GenerativeModel(model, system_instruction=system_instruction)

        response = model_instance.generate_content(prompt)
        return response.text
