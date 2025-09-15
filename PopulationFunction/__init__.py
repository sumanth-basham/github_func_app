import azure.functions as func
import json
from model import population_growth

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if req.method == "POST":
            data = req.get_json()
        else:
            data = req.params
        P0 = float(data.get("P0", 1000))
        r = float(data.get("r", 0.05))
        t = float(data.get("t", 10))
        result = population_growth(P0, r, t)
        return func.HttpResponse(
            json.dumps({"population": result}),
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
