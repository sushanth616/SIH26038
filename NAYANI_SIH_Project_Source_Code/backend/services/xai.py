import cv2

def make_heatmap(path,output):
    image=cv2.imread(str(path))
    if image is None: raise ValueError("Invalid image")
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(0,0),15)
    activity=cv2.absdiff(gray,blur)
    activity=cv2.normalize(activity,None,0,255,cv2.NORM_MINMAX)
    heat=cv2.applyColorMap(activity,cv2.COLORMAP_JET)
    overlay=cv2.addWeighted(image,0.60,heat,0.40,0)
    cv2.imwrite(str(output),overlay)
    return output.name
