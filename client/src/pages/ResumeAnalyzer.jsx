import { useState } from "react";
import { useNavigate } from "react-router-dom"; // Added for navigation
import Markdown from "react-markdown";          // Added for crisp text rendering
import { analyzeResume } from "../services/resumeAnalyzerService";

function ResumeAnalyzer() {
    const navigate = useNavigate(); // Navigation hook
    const [resume, setResume] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [result, setResult] = useState(null);
    const [btn, setBtn] = useState("Analyze")

    const handleAnalyze = async () => {
        if (!resume || !jobDescription.trim()) {
            alert("Upload resume and enter JD");
            return;
        }

        try {
            setBtn("Analyzing...")
            const data = await analyzeResume(resume, jobDescription);
            setResult(data);
            setBtn("Analyze")
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="tool-view-container">
            {/* TACTICAL NAVIGATION HEADER */}
            <div className="tool-view-header">
                <button className="back-btn" onClick={() => navigate("/")}>
                    ← Dashboard
                </button>
                <h1>Resume ↔ JD Analyzer</h1>
            </div>

            <div className="tool-form-layout">
                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setResume(e.target.files[0])}
                />

                <textarea
                    rows="10"
                    placeholder="Paste Job Description"
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                />

                <button onClick={handleAnalyze} className="action-submit-btn">
                    {btn}
                </button>
            </div>

            {result && (
                <div className="analysis-result-section">
                    <h2>Analysis Result</h2>
                    {/* RICH GRAPHIC DISPLAY REPLACING PRE BLOCK */}
                    <div className="markdown-output-card">
                        <Markdown>{result.analysis}</Markdown>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResumeAnalyzer;