import apiClient from "./apiClient";

export const rewriteResume =
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
        "/resume-rewriter/rewrite",
        formData
      );

    return response.data;
  };