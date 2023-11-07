//create axios instance
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8912/",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

export default axiosInstance;