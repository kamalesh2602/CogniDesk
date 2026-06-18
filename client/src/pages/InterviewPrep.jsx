import { useState } from "react";

import {
  generateInterviewQuestions
}
from "../services/interviewService";

function InterviewPrep() {

  const [resume, setResume] =
    useState(null);

  const [jobDescription,
    setJobDescription] =
    useState("");

  const [result, setResult] =
    useState(null);

  const handleGenerate =
    async () => {

      const data =
        await generateInterviewQuestions(
          resume,
          jobDescription
        );

      setResult(data);
    };

  return (
    <div>

      <h1>
        Interview Prep
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
        value={jobDescription}
        onChange={(e) =>
          setJobDescription(
            e.target.value
          )
        }
      />

      <button
        onClick={handleGenerate}
      >
        Generate Questions
      </button>

      {
        result && (

          <pre>
            {
              result.questions
            }
          </pre>

        )
      }

    </div>
  );
}

export default InterviewPrep;