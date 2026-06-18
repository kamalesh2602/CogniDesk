import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Markdown from "react-markdown";
import { generateInterviewQuestions } from "../services/interviewService";

function InterviewPrep() {
    const navigate = useNavigate(); // Properly initialized hook

    const [resume, setResume] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [result, setResult] = useState(null);
    const [btn, setBtn] = useState("Generate Questions")

    const handleGenerate = async () => {
        if (!resume || !jobDescription.trim()) {
            alert("Upload resume and enter JD");
            return;
        }

        try {
            setBtn("Generating...")
            const data = await generateInterviewQuestions(
                resume,
                jobDescription
            );
            setResult(data);
            setBtn("Generate Questions")
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
                <h1>Interview Prep</h1>
            </div>

            {/* FORM FIELD WRAPPER */}
            <div className="tool-form-layout">
                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setResume(e.target.files[0])}
                />

                <textarea
                    rows="10"
                    placeholder="Paste Job Description / Target Role Parameters..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                />

                <button onClick={handleGenerate} className="action-submit-btn">
                    {btn}
                </button>
            </div>

            {/* BEAUTIFIED MARKDOWN RENDER BLOCK */}
            {result && (
                <div className="analysis-result-section">
                    <h2>Generated Interview Roadmap</h2>
                    <div className="markdown-output-card">
                        <Markdown>{result.questions}</Markdown>
                    </div>
                </div>
            )}
        </div>
    );
}

export default InterviewPrep;