from .base import BaseTool, ToolInput, ToolOutput
from typing import Dict, Any, Optional
from pydantic import BaseModel
import aiofiles
import os
import json

class FileReadInput(ToolInput):
    file_path: str
    encoding: str = "utf-8"

class FileWriteInput(ToolInput):
    file_path: str
    content: str
    encoding: str = "utf-8"
    mode: str = "w"  # "w" for write, "a" for append

class FileTool(BaseTool):
    """Tool for file operations"""
    
    def __init__(self):
        super().__init__(
            name="file_operations",
            description="Read from and write to files"
        )
        self.allowed_extensions = {".txt", ".json", ".csv", ".md", ".log"}
        self.base_path = os.getenv("FILE_TOOL_BASE_PATH", "/tmp/ai-agent-files")
        os.makedirs(self.base_path, exist_ok=True)
    
    async def execute(self, input_data: Dict[str, Any]) -> ToolOutput:
        """Execute file operation"""
        try:
            operation = input_data.get("operation")
            
            if operation == "read":
                return await self._read_file(FileReadInput(**input_data))
            elif operation == "write":
                return await self._write_file(FileWriteInput(**input_data))
            elif operation == "list":
                return await self._list_files(input_data.get("directory", ""))
            else:
                return ToolOutput(success=False, error="Invalid operation. Use 'read', 'write', or 'list'")
                
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
    
    async def _read_file(self, input_data: FileReadInput) -> ToolOutput:
        """Read file content"""
        file_path = self._get_safe_path(input_data.file_path)
        
        if not os.path.exists(file_path):
            return ToolOutput(success=False, error="File not found")
        
        if not self._is_allowed_file(file_path):
            return ToolOutput(success=False, error="File type not allowed")
        
        try:
            async with aiofiles.open(file_path, 'r', encoding=input_data.encoding) as f:
                content = await f.read()
            
            return ToolOutput(success=True, data={"content": content, "file_path": file_path})
        
        except Exception as e:
            return ToolOutput(success=False, error=f"Failed to read file: {str(e)}")
    
    async def _write_file(self, input_data: FileWriteInput) -> ToolOutput:
        """Write content to file"""
        file_path = self._get_safe_path(input_data.file_path)
        
        if not self._is_allowed_file(file_path):
            return ToolOutput(success=False, error="File type not allowed")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            async with aiofiles.open(file_path, input_data.mode, encoding=input_data.encoding) as f:
                await f.write(input_data.content)
            
            return ToolOutput(success=True, data={"file_path": file_path, "bytes_written": len(input_data.content.encode())})
        
        except Exception as e:
            return ToolOutput(success=False, error=f"Failed to write file: {str(e)}")
    
    async def _list_files(self, directory: str) -> ToolOutput:
        """List files in directory"""
        dir_path = self._get_safe_path(directory) if directory else self.base_path
        
        if not os.path.exists(dir_path):
            return ToolOutput(success=False, error="Directory not found")
        
        try:
            files = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                files.append({
                    "name": item,
                    "path": item_path,
                    "is_file": os.path.isfile(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                })
            
            return ToolOutput(success=True, data={"files": files, "directory": dir_path})
        
        except Exception as e:
            return ToolOutput(success=False, error=f"Failed to list files: {str(e)}")
    
    def _get_safe_path(self, file_path: str) -> str:
        """Get safe file path within base directory"""
        # Remove any path traversal attempts
        safe_path = os.path.normpath(file_path).lstrip('/')
        return os.path.join(self.base_path, safe_path)
    
    def _is_allowed_file(self, file_path: str) -> bool:
        """Check if file extension is allowed"""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.allowed_extensions
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema"""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["read", "write", "list"],
                    "description": "File operation to perform"
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the file (for read/write operations)"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write (for write operation)"
                },
                "directory": {
                    "type": "string",
                    "description": "Directory to list (for list operation)"
                },
                "encoding": {
                    "type": "string",
                    "default": "utf-8",
                    "description": "File encoding"
                },
                "mode": {
                    "type": "string",
                    "enum": ["w", "a"],
                    "default": "w",
                    "description": "Write mode: 'w' for overwrite, 'a' for append"
                }
            },
            "required": ["operation"]
        }