import axios from "axios";
import API_BASE_URL from "../config/api";

const API = `${API_BASE_URL}/chat`;

export const askQuestion = async (
    workspaceId,
    question
) => {

    const response = await axios.post(
        `${API}/ask`,
        {
            workspace_id: workspaceId,
            question: question
        }
    );

    return response.data;
};

export const getChatHistory = async (
    workspaceId
) => {

    const response = await axios.get(
        `${API}/history/${workspaceId}`
    );

    return response.data;
};
