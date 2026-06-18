import apiClient from "./apiClient";

export const generateInterviewQuestions =
  async (
    resumeFile,
    jobDescription
  ) => {

    const formData =
      new FormData();

    formData.append(
      "resume_file",
      resumeFile
    );

    formData.append(
      "job_description",
      jobDescription
    );

    const response =
      await apiClient.post(
        "/interview/generate",
        formData
      );

    return response.data;
  };