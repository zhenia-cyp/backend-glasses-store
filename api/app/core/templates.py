from fastapi.templating import Jinja2Templates
from pathlib import Path

# Налаштування шаблонів
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

