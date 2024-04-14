from ._base import app, BASE_ROUTE

ROUTE = f"{BASE_ROUTE}/protection-system"


@app.get("/api/protection-system/{id}")
def get_protection_system(id: int):
    return {"id": id}
