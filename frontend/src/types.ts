export type SourceType = "manual" | "sop" | "faq" | "case" | "fault_code" | "log";
export type Confidence = "low" | "medium" | "high";
export type Priority = "low" | "medium" | "high";

export interface ErrorEventRequest {
  external_event_id?: string;
  device_id: string;
  error_code: string;
  message: string;
  occurred_at?: string;
  log_window_minutes: number;
}

export interface ErrorEvent extends ErrorEventRequest {
  id: string;
  received_at: string;
}

export interface Device {
  device_id: string;
  display_name?: string;
}

export interface LogEvidence {
  id: string;
  excerpt: string;
  matched_terms: string[];
  source_path?: string;
}

export interface Citation {
  source_type: SourceType;
  source_id: string;
  title: string;
  excerpt: string;
}

export interface PossibleCause {
  cause: string;
  confidence: Confidence;
  evidence_refs: string[];
  reasoning: string;
}

export interface RecommendedAction {
  action: string;
  priority: Priority;
  requires_shutdown: boolean;
  risk_note?: string;
}

export interface InitialDiagnosisResult {
  summary: string;
  possible_causes: PossibleCause[];
  recommended_actions: RecommendedAction[];
  citations: Citation[];
  safety_notes: string[];
}

export interface FollowUpExchange {
  id: string;
  question: string;
  answer: string;
  citations: Citation[];
  created_at: string;
}

export interface Diagnosis {
  id: string;
  error_event: ErrorEvent;
  device: Device;
  log_evidence: LogEvidence[];
  initial_diagnosis: InitialDiagnosisResult;
  follow_up_questions: FollowUpExchange[];
  created_at: string;
  updated_at: string;
}

