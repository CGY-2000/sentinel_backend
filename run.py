import os

import uvicorn

# PLATFORM = os.environ.get("PLATFORM")

# if PLATFORM.lower() == 'cuda':
#     cmd = "ffmpeg -hwacc cuda"
# else:
#     cmd = "ffmpeg -hwacc vappid"


if __name__ == "__main__":
    uvicorn.run("app:create_app", host="192.168.1.53", port=8001, reload=True, loop="uvloop", factory=True, log_level="info")

