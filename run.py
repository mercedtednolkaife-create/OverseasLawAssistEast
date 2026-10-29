import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "lawagent.api.main:app",
        host="127.0.0.1",
        port=port,
        reload=True,
        reload_dirs=["lawagent"],
        reload_includes=["*.py"],
        reload_excludes=["FrontEnd", "data", "dist", ".git", ".gemini", "node_modules"],
    )
