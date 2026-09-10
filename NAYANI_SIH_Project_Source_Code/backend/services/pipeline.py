from pathlib import Path
from .quality import quality_check
from .model import predict
from .xai import make_heatmap
from .report import build_report

def run_pipeline(path:Path):
    quality=quality_check(path)
    if not quality["passed"]:
        return {
            "quality_check":quality,
            "screening_status":"RECAPTURE_REQUIRED",
            "message":quality["message"],
            "xai_heatmap":None,"prediction":None,"report":None
        }
    prediction=predict(path)
    heatmap_name=f"{path.stem}_heatmap.jpg"
    make_heatmap(path,path.parent/heatmap_name)
    return {
        "quality_check":quality,
        "screening_status":"COMPLETED",
        "prediction":prediction,
        "xai_heatmap":f"/uploads/{heatmap_name}",
        "report":build_report(prediction)
    }
