import cv2

LABELS=["No DR","Mild NPDR","Moderate NPDR","Severe NPDR","Proliferative DR"]

def predict(path):
    # Prototype fallback. Replace with a trained/validated model for real deployment.
    image=cv2.imread(str(path))
    if image is None: raise ValueError("Invalid image")
    rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    red_mean=float(rgb[:,:,0].mean())
    contrast=float(gray.std())
    darkness=float((gray<45).mean())
    score=(0.45*min(1.0,red_mean/180.0)+
           0.35*min(1.0,contrast/80.0)+
           0.20*min(1.0,darkness/0.35))
    index=min(4,int(score*5))
    confidence=round(0.60+0.08*abs(score-0.5),3)
    return {
        "label":LABELS[index],
        "severity_index":index,
        "confidence":confidence,
        "model":"NAYANI-Demo-Inference",
        "note":"Prototype result only; not a clinical diagnosis."
    }
