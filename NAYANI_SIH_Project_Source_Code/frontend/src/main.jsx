import React from "react";
import {createRoot} from "react-dom/client";
import "./styles.css";

const API="http://127.0.0.1:8000";

function Step({n,title,active}) {
  return <div className={"step "+(active?"active":"")}>
    <div className="stepno">{String(n).padStart(2,"0")}</div>{title}
  </div>
}

function App(){
  const [file,setFile]=React.useState(null),[preview,setPreview]=React.useState("");
  const [result,setResult]=React.useState(null),[loading,setLoading]=React.useState(false);
  const [error,setError]=React.useState("");

  function choose(e){
    const f=e.target.files?.[0]; if(!f)return;
    setFile(f); setPreview(URL.createObjectURL(f)); setResult(null); setError("");
  }
  async function screen(){
    if(!file)return;
    setLoading(true);setError("");
    try{
      const fd=new FormData();fd.append("file",file);
      const r=await fetch(`${API}/api/screen`,{method:"POST",body:fd});
      const d=await r.json();if(!r.ok)throw new Error(d.detail||"Screening failed");
      setResult(d);
    }catch(e){setError(e.message+". Make sure the FastAPI backend is running.");}
    finally{setLoading(false);}
  }
  const completed=result?.screening_status==="COMPLETED";
  return <div className="page">
    <header><div className="brand"><div className="logo">N</div><div>
      <h1>NAYANI</h1><span>AI-assisted screening for diabetic retinopathy</span>
    </div></div><div className="badge">SMART INDIA HACKATHON 2026</div></header>
    <section className="hero"><p className="eyebrow">LOW-BANDWIDTH • EXPLAINABLE • HUMAN-IN-THE-LOOP</p>
      <h2>Retinal screening, simplified.</h2>
      <p className="sub">Upload a retinal image and run the complete prototype screening pipeline.</p>
    </section>
    <div className="pipeline">
      <Step n={1} title="Image Upload" active={!!file}/><Step n={2} title="Quality Check" active={!!result}/>
      <Step n={3} title="AI Model" active={completed}/><Step n={4} title="XAI Heatmap" active={!!result?.xai_heatmap}/>
      <Step n={5} title="Severity Report" active={!!result?.report}/><Step n={6} title="Referral Priority" active={!!result?.report}/>
    </div>
    <main><section className="card upload"><h3>01 · Upload retinal image</h3>
      <label className="drop"><input type="file" accept="image/png,image/jpeg,image/webp" onChange={choose}/>
        {preview?<img src={preview} alt="Selected retinal image"/>:<div><strong>Choose retinal image</strong><p>JPG, PNG or WEBP</p></div>}
      </label><button disabled={!file||loading} onClick={screen}>{loading?"Running screening...":"Run AI Screening"}</button>
      {error&&<div className="error">{error}</div>}</section>
      {result&&<section className="results"><div className={"status "+(completed?"ok":"warn")}>
        <strong>{completed?"Screening completed":"Recapture required"}</strong><span>{result.quality_check.message}</span></div>
        <div className="grid"><div className="card"><h3>02 · Quality Check</h3>
          <div className="score">{result.quality_check.score}<small>/100</small></div>
          <p>{result.quality_check.width} × {result.quality_check.height}px</p></div>
        {completed&&<><div className="card"><h3>03 · AI Model</h3><div className="severity">{result.prediction.label}</div>
          <p>Prototype confidence: {(result.prediction.confidence*100).toFixed(1)}%</p></div>
          <div className="card heat"><h3>04 · XAI Heatmap</h3><img src={API+result.xai_heatmap} alt="Explainability heatmap"/>
          <p>Highlighted regions show the prototype explanation.</p></div>
          <div className="card"><h3>05 · Severity Report</h3><div className="severity">{result.report.severity}</div>
          <p>{result.report.recommendation}</p></div>
          <div className="card priority"><h3>06 · Referral Priority</h3><div className="severity">{result.report.referral_priority}</div>
          <p>Human review: <strong>{result.report.human_review?"Required":"Not required"}</strong></p></div></>}</div>
      </section>}
      <section className="notice"><strong>Prototype notice:</strong> This demo is for hackathon/software demonstration only and is not a medical diagnosis. Clinical deployment requires validated data, model validation, privacy/security controls and qualified clinician review.</section>
    </main>
  </div>
}
createRoot(document.getElementById("root")).render(<App/>);
