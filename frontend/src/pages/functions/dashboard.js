import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// User-related API functions
export const fetchUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/users/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    
    // Check for the specific response format where users are in data.users
    if (response.data && response.data.data && Array.isArray(response.data.data.users)) {
      return response.data.data.users.map((user) => ({
        id: user.id,
        username: user.name,
        name: user.name,
        email: user.email,
        status: "active",
        is_superuser: user.is_superuser,
        is_staff: user.is_staff,
      }));
    } else if (response.data && Array.isArray(response.data)) {
      // Fallback for direct array response
      return response.data.map((user) => ({
        id: user.id,
        username: user.name,
        name: user.name,
        email: user.email,
        status: "active",
        is_superuser: user.is_superuser,
        is_staff: user.is_staff,
      }));
    } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
      // Fallback for paginated response
      return response.data.results.map((user) => ({
        id: user.id,
        username: user.name,
        name: user.name,
        email: user.email,
        status: "active",
        is_superuser: user.is_superuser,
        is_staff: user.is_staff,
      }));
    } else {
      // If response.data is not as expected, log it and return an empty array
      console.error("Unexpected API response format:", response.data);
      return [];
    }
  } catch (err) {
    console.error("Error fetching users:", err.message);
    throw err;
  }
};

export const fetchUserCounts = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/user-counts/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    return {
      totalUsers: response.data.total_users,
      totalAdmins: response.data.total_admins
    };
  } catch (err) {
    console.error("Error fetching user counts:", err.message);
    throw err;
  }
};

export const createUser = async (userData) => {
  try {
    const response = await axios.post(
      `${API_URL}/api/users/create/`,
      userData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      }
    );
    return response.data;
  } catch (err) {
    console.error("Error creating user:", err.message);
    throw err;
  }
};

export const updateUser = async (userId, userData) => {
  try {
    // Only send allowed fields to the backend
    const updateData = {
      is_superuser: userData.is_superuser,
      is_staff: userData.is_staff
    };

    const response = await axios.put(
      `${API_URL}/api/users/${userId}/update/`,
      updateData,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      }
    );
    return response.data;
  } catch (err) {
    console.error("Error updating user:", err.message);
    throw err;
  }
};

export const deleteUser = async (userId) => {
  try {
    await axios.delete(`${API_URL}/api/users/${userId}/delete/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    return true;
  } catch (err) {
    console.error("Error deleting user:", err.message);
    throw err;
  }
};

// Message-related API functions
export const fetchMessages = async () => {
  try {
    const response = await axios.get(
      `${API_URL}/chat/api/messages/`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      }
    );
    console.log("API Response:", response);
    return response?.data || [];
  } catch (err) {
    console.error("Error fetching messages:", err.message);
    throw err;
  }
};