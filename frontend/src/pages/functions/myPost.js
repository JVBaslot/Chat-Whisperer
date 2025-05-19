import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Function to fetch all posts
export const fetchAllPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/freedom-wall/api/posts/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    return { success: true, data: response.data };
  } catch (error) {
    console.error('Error fetching all posts:', error);
    return { success: false, error: error.message || 'Failed to fetch posts' };
  }
};

// Function to fetch current user's posts
export const fetchUserPosts = async () => {
  try {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      return { success: false, error: 'User ID not found' };
    }
    
    const response = await axios.get(`http://127.0.0.1:8000/freedom-wall/api/posts/user_posts/?user_id=${userId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    return { success: true, data: response.data };
  } catch (error) {
    console.error('Error fetching user posts:', error);
    return { success: false, error: error.message || 'Failed to fetch user posts' };
  }
};

// Function to delete a post
export const deletePost = async (postId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/freedom-wall/api/posts/${postId}/delete/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    });
    return { success: true };
  } catch (error) {
    console.error('Error deleting post:', error);
    return { success: false, error: error.message || 'Failed to delete post' };
  }
};

// Function to update a post
export const updatePost = async (postId, postData) => {
  try {
    const accessToken = localStorage.getItem('accessToken');
    
    if (!accessToken) {
      return {
        success: false,
        error: 'Authentication required'
      };
    }
    
    const response = await axios.patch(`http://127.0.0.1:8000/freedom-wall/api/posts/${postId}/update_post/`, 
      postData,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        }
      }
    );
    
    return {
      success: true,
      data: response.data
    };
  } catch (error) {
    console.error('Error updating post:', error);
    return {
      success: false,
      error: error.response?.data?.detail || 'An error occurred while updating the post'
    };
  }
};
