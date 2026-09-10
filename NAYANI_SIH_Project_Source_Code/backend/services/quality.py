import cv2

def quality_check(path):
    image=cv2.imread(str(path))
    if image is None:
        return {"passed":False,"score":0,"message":"Image could not be read."}
    h,w=image.shape[:2]
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    sharpness=float(cv2.Laplacian(gray,cv2.CV_64F).var())
    resolution_score=min(1.0,(w*h)/(1000*1000))
    sharp_score=min(1.0,sharpness/250.0)
    score=round((0.45*resolution_score+0.55*sharp_score)*100,1)
    passed=score>=35 and w>=300 and h>=300
    return {
        "passed":passed,"score":score,"width":w,"height":h,
        "sharpness":round(sharpness,2),
        "message":"Image quality is suitable for prototype screening." if passed
        else "Image quality may be insufficient. Please capture a clearer retinal image."
    }
