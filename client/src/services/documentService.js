import axios from "axios";
import API_BASE_URL from "../config/api";

const API = `${API_BASE_URL}/chat`;


export const processDocument =
    async (documentId) => {

        const response =
            await axios.post(
                `${API_BASE_URL}/documents/process/${documentId}`
            );

        return response.data;
    };

export const embedDocument =
    async (documentId) => {

        const response =
            await axios.post(
                `${API_BASE_URL}/documents/embed/${documentId}`
            );

        return response.data;
    };