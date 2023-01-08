import axios, {AxiosHeaders, AxiosInstance, AxiosRequestConfig} from "axios";
import jwtDecode from "jwt-decode";
import dayjs from "dayjs";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import {bufferEqual} from "../crypto/masterKeyFunctions";

// The base URL for the Django backend API
const baseURL = "http://127.0.0.1:8000";

// Custom hook that creates an axios instance and automatically
// adds the JWT access token to the headers of each request
const useAxios = (): AxiosInstance => {
    // Get the authTokens and setAuthTokens functions from the AuthContext
    const { authTokens, setAuthTokens, logoutUser, derivedKey } = useContext(AuthContext);

    // Create an axios instance with the baseURL and authorization header set to the JWT access token
    const axiosInstance = axios.create({
        baseURL,
        headers: { Authorization: `JWT ${authTokens?.access}` },
    });

    // Add an interceptor to the request to check if the JWT access token has expired
    axiosInstance.interceptors.request.use(
        async (req: AxiosRequestConfig): Promise<AxiosRequestConfig> => {
            // Decode the user from the JWT access token to check its expiration
            if (!authTokens || !authTokens.access) {
                logoutUser()
                return req;
            }

            let user:{exp:number};
            try {
                user = jwtDecode(authTokens.access);
            } catch (error) {
                console.error(error);
                return Promise.reject(error);
            }

            // Check if the derivedKey is still in state

            if (bufferEqual(derivedKey, new ArrayBuffer(32))){
                logoutUser()
                return req
            }else {
                // Check if the token has expired
                const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
                if (!isExpired) {
                    // If the token has not expired, and there is no derivedKey stored, logout user
                    return req;
                } else {
                    // If the token has expired, try to refresh it using the JWT refresh token
                    try {
                        const response = await axios.post(`${baseURL}/jwt/refresh/`, {
                            refresh: authTokens.refresh,
                        });

                        // Update the authTokens in local storage and the AuthContext
                        localStorage.setItem("authTokens", JSON.stringify(response.data));
                        setAuthTokens(response.data);

                        // Set the authorization header for the request to the new JWT access token
                        req.headers = {...req.headers} as AxiosHeaders
                        req.headers.set('Authorization', `JWT ${response.data.access}`)
                        return req;
                    } catch (error) {
                        console.error(error);
                        return Promise.reject(error);
                    }
                }
            }

        }
    );

    return axiosInstance;
};

export default useAxios;
