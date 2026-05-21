import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app, get_video_info
    url = "https://www.youtube.com/watch?v=v8LANbqV8e8"
    result = get_video_info(url)
    
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("Success! Result saved to result.json")
except Exception as e:
    import traceback
    print("Error occurred:")
    traceback.print_exc()
