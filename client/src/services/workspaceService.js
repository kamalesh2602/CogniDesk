import axios from "axios";
import API_BASE_URL from "../config/api";

const API = `${API_BASE_URL}/workspaces`;

export const getWorkspaces = async () => {
    const response = await axios.get(API);
    return response.data;
};

export const createWorkspace = async (workspaceData) => {
    const response = await axios.post(API, workspaceData);
    return response.data;
};

export const deleteWorkspace = async (id) => {
    const response = await axios.delete(`${API}/${id}`);
    return response.data;
};

export const getWorkspace = async (id) => {
    const response = await axios.get(`${API}/${id}`);
    return response.data;
};

export const getWorkspaceDocuments = async (workspaceId) => {
    const response = await axios.get(
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

    const response = await axios.post(
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
    const response = await axios.delete(
        `${API_BASE_URL}/documents/${documentId}`
    );

    return response.data;
};