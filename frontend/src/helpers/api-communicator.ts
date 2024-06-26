import axios from "axios";

export const loginUser = async (email: string, password: string) => {
  const res = await axios.post("/user/login", { email, password });
  if (res.status !== 200) {
    throw new Error("Unable to login");
  }
  const data = await res.data;
  return data;
};

export const signupUser = async (
  name: string,
  email: string,
  password: string
) => {
  const res = await axios.post("/user/signup", { name, email, password });
  if (res.status !== 201) {
    throw new Error("Unable to Signup");
  }
  const data = await res.data;
  return data;
};

export const checkAuthStatus = async () => {
  const res = await axios.get("/user/auth-status");
  if (res.status !== 200) {
    throw new Error("Unable to authenticate");
  }
  const data = await res.data;
  return data;
};

export const sendChatRequest = async (message: string, tenant_id: string | undefined) => {
  console.log("tenant_id", tenant_id);
  const formData = new FormData();
  formData.append('tenant_id', tenant_id);
  formData.append('question', message);

  // Make the API request
  const res = await axios.post('/start-chat/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  // Check for a successful response
  if (res.status !== 200) {
    throw new Error('Unable to send chat');
  }
  const data = await res.data;
  return data;
};

export const getUserChats = async () => {
  const res = await axios.get("/chat/all-chats");
  if (res.status !== 200) {
    throw new Error("Unable to send chat");
  }
  const data = await res.data;
  return data;
};

export const deleteUserChats = async () => {
  const res = await axios.delete("/chat/delete");
  if (res.status !== 200) {
    throw new Error("Unable to delete chats");
  }
  const data = await res.data;
  return data;
};

export const logoutUser = async () => {
  const res = await axios.get("/user/logout");
  if (res.status !== 200) {
    throw new Error("Unable to delete chats");
  }
  const data = await res.data;
  return data;
};

export const uploadDocument = async (file: File, tenant_id: string | undefined) => {
  const formData = new FormData();
  formData.append('tenant_id', tenant_id);
  formData.append('file', file);

  const res = await axios.post('/load-document/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  if (res.status !== 200) {
    throw new Error('Unable to upload document');
  }
  const data = await res.data;
  return data;
};
