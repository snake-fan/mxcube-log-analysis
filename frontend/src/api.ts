import type { Diagnosis, ErrorEventRequest, FollowUpExchange } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers
    },
    ...options
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function createDiagnosis(payload: ErrorEventRequest): Promise<Diagnosis> {
  return request<Diagnosis>("/error-events", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function sendFollowUpQuestion(
  diagnosisId: string,
  question: string
): Promise<FollowUpExchange> {
  return request<FollowUpExchange>(`/diagnoses/${diagnosisId}/messages`, {
    method: "POST",
    body: JSON.stringify({ question })
  });
}

