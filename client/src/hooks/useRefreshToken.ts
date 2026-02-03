import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { setInitialized, setUser } from "../redux/auth/authSlice";
import { API_CONFIG } from "../config/api.config";
import { tokenManager } from "../utils/tokenManager";

/**
 * Custom hook to initialize authentication state on app load
 * Attempts to refresh the access token using the HttpOnly cookie
 */
export const useRefreshToken = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const initAuth = async () => {
      try {
        // Try to refresh token on app load (uses HttpOnly cookie)
        const response = await fetch(
          `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH.REFRESH_TOKEN}`,
          {
            method: "POST",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          // Store access token and update user state
          if (data?.data?.accessToken) {
            tokenManager.setAccessToken(data.data.accessToken);

            // Update Redux state with user data
            if (data?.data?.user) {
              dispatch(setUser(data.data.user));
            }

            console.log("Auth restored from refresh token");
          }
        } else {
          console.log("No valid refresh token found");
        }
      } catch (error) {
        console.log("Auth initialization failed:", error);
      } finally {
        // Mark auth as initialized regardless of success/failure
        dispatch(setInitialized());
      }
    };

    initAuth();
  }, [dispatch]);
};
