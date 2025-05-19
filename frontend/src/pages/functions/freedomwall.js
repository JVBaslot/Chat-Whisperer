import { ref } from 'vue';
import axios from 'axios';

export function useFreedomWall() {
  const loading = ref(false);
  const error = ref(null);
  const posts = ref([]);

  // Fetch all posts
  const fetchPosts = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('http://127.0.0.1:8000/freedom-wall/api/posts/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      });
      posts.value = response.data || [];
      return posts.value;
    } catch (err) {
      console.error('Error fetching freedom wall posts:', err.message);
      error.value = 'Failed to load posts. Please try again later.';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Fetch user's posts
  const fetchUserPosts = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get('http://127.0.0.1:8000/freedom-wall/api/posts/my-posts/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      });
      return response.data || [];
    } catch (err) {
      console.error('Error fetching user posts:', err.message);
      error.value = 'Failed to load your posts. Please try again later.';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Create a new post
  const createPost = async (postData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/freedom-wall/api/posts/', 
        postData,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        }
      );
      return response.data;
    } catch (err) {
      console.error('Error creating post:', err.message);
      error.value = 'Failed to create post. Please try again later.';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Delete a post
  const deletePost = async (postId) => {
    loading.value = true;
    error.value = null;
    try {
      await axios.delete(`http://127.0.0.1:8000/freedom-wall/api/posts/${postId}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      });
      return true;
    } catch (err) {
      console.error('Error deleting post:', err.message);
      error.value = 'Failed to delete post. Please try again later.';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    posts,
    fetchPosts,
    fetchUserPosts,
    createPost,
    deletePost
  };
}
