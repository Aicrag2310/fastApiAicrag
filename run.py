import uvicorn
from dotenv import load_dotenv

from piro_api import create_app

load_dotenv()
app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
