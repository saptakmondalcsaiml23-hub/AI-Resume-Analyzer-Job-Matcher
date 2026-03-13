const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function parseResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail =
      typeof data.detail === "string"
        ? data.detail
        : Array.isArray(data.detail)
          ? data.detail.map((item) => item.msg).join(", ")
          : "Request failed";

    throw new Error(detail);
  }

  return data;
}

export async function fetchResumes() {
  const response = await fetch(`${API_BASE}/resumes`);
  return parseResponse(response);
}

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload-resume`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(response);
}

export async function analyzeJob(payload) {
  const response = await fetch(`${API_BASE}/match-job`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return parseResponse(response);
}
