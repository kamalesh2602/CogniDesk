import apiClient from "./apiClient";
import API_BASE_URL from "../config/api";

const API = `${API_BASE_URL}/workspaces`;

export const getWorkspaces = async () => {
    const response = await apiClient.get(API);
    return response.data;
};

export const createWorkspace = async (workspaceData) => {
    const response = await apiClient.post(API, workspaceData);
    return response.data;
};

export const deleteWorkspace = async (id) => {
    const response = await apiClient.delete(`${API}/${id}`);
    return response.data;
};

export const updateWorkspace = async (
  workspaceId,
  workspaceData
) => {
  const response =
    await apiClient.put(
      `/workspaces/${workspaceId}`,
      workspaceData
    );

  return response.data;
};

export const getWorkspace = async (id) => {
    const response = await apiClient.get(`${API}/${id}`);
    return response.data;
};

export const getWorkspaceDocuments = async (workspaceId) => {
    const response = await apiClient.get(
        `${API_BASE_URL}/documents/workspace/${workspaceId}`
    );

    return response.data;
};

export const uploadDocument = async (
    workspaceId,
    file
) => {

    const formData = new FormData();

    formData.append(
        "workspace_id",
        workspaceId
    );

    formData.append(
        "file",
        file
    );

    const response = await apiClient.post(
        `${API_BASE_URL}/documents/upload`,
        formData,
        {
            headers: {
                "Content-Type":
                    "multipart/form-data",
            },
        }
    );

    return response.data;
};

export const deleteDocument = async (documentId) => {
    const response = await apiClient.delete(
        `${API_BASE_URL}/documents/${documentId}`
    );

    return response.data;
};

export const getRecentWorkspaces =
  async () => {

    const response =
      await apiClient.get(
        `${API}/recent`
      );

    return response.data;
};