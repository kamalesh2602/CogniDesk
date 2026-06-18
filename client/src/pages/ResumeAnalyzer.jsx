import { useState } from "react";
import { analyzeResume } from "../services/resumeAnalyzerService";


function ResumeAnalyzer() {

    const [resume, setResume] =
        useState(null);

    const [jobDescription, setJobDescription] =
        useState("");
    const [result, setResult] =
        useState(null);

    const handleAnalyze =
  async () => {

    if (
      !resume ||
      !jobDescription.trim()
    ) {
      alert(
        "Upload resume and enter JD"
      );
      return;
    }

    try {

      const data =
        await analyzeResume(
          resume,
          jobDescription
        );

      setResult(data);

    } catch (error) {

      console.error(error);

    }
  };


    return (
        <div>

            <h1>
                Resume ↔ JD Analyzer
            </h1>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) =>
                    setResume(
                        e.target.files[0]
                    )
                }
            />

            <textarea
                rows="10"
                placeholder="Paste Job Description"
                value={jobDescription}
                onChange={(e) =>
                    setJobDescription(
                        e.target.value
                    )
                }
            />

            <button onClick={handleAnalyze}>
                Analyze
            </button>

            {
  result && (

    <div>

      <h2>
        Analysis Result
      </h2>

      <pre>
        {result.analysis}
      </pre>

    </div>

  )
}

        </div>
    );
}

export default ResumeAnalyzer;