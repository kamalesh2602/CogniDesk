import { useState } from "react";
import { rewriteResume } from "../services/resumeRewriterService";

function ResumeRewriter() {

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
          await rewriteResume(
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
        Resume Rewriter
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

      <button
        onClick={handleAnalyze}
      >
        Rewrite Resume
      </button>

      {
        result && (

          <div>

            <h2>
              Rewritten Resume Suggestions
            </h2>

            <pre>
              {result.result}
            </pre>

          </div>

        )
      }

    </div>
  );
}

export default ResumeRewriter;