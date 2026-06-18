import { useState } from "react";
import { useNavigate } from "react-router-dom"; // Added for navigation
import Markdown from "react-markdown";          // Added for crisp text rendering
import { rewriteResume } from "../services/resumeRewriterService";

function ResumeRewriter() {
    const navigate = useNavigate(); // Navigation hook
    const [resume, setResume] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [result, setResult] = useState(null);
    const [btn, setBtn] = useState("Rewrite Resume")

    const handleAnalyze = async () => {

        if (!resume || !jobDescription.trim()) {
            alert("Upload resume and enter JD");
            return;
        }


        try {
            setBtn("Analyzing...")
            const data = await rewriteResume(resume, jobDescription);
            setResult(data);
            setBtn("Rewrite Resume");
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
                <h1>Resume Rewriter</h1>
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
                    <h2>Rewritten Resume Suggestions</h2>
                    {/* RICH GRAPHIC DISPLAY REPLACING PRE BLOCK */}
                    <div className="markdown-output-card">
                        <Markdown>{result.result}</Markdown>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ResumeRewriter;