import {
  Activity,
  AlertTriangle,
  BookOpen,
  ClipboardList,
  FileText,
  LoaderCircle,
  MessageSquare,
  Send
} from "lucide-react";
import { FormEvent, useMemo, useState } from "react";

import { createDiagnosis, sendFollowUpQuestion } from "./api";
import type { Citation, Diagnosis } from "./types";

const nowForInput = () => new Date().toISOString().slice(0, 16);

function sourceLabel(sourceType: Citation["source_type"]) {
  const labels: Record<Citation["source_type"], string> = {
    manual: "Manual",
    sop: "SOP",
    faq: "FAQ",
    case: "Case",
    fault_code: "Fault Code",
    log: "Log"
  };
  return labels[sourceType];
}

function App() {
  const [deviceId, setDeviceId] = useState("device-01");
  const [errorCode, setErrorCode] = useState("E_TIMEOUT");
  const [message, setMessage] = useState("controller timeout");
  const [occurredAt, setOccurredAt] = useState(nowForInput());
  const [logWindowMinutes, setLogWindowMinutes] = useState(10);
  const [diagnosis, setDiagnosis] = useState<Diagnosis | null>(null);
  const [question, setQuestion] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const citationCount = diagnosis?.initial_diagnosis.citations.length ?? 0;
  const evidenceCount = diagnosis?.log_evidence.length ?? 0;

  const statusLabel = useMemo(() => {
    if (isSubmitting) return "Diagnosing";
    if (diagnosis) return "Ready";
    return "Idle";
  }, [diagnosis, isSubmitting]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const nextDiagnosis = await createDiagnosis({
        device_id: deviceId,
        error_code: errorCode,
        message,
        occurred_at: new Date(occurredAt).toISOString(),
        log_window_minutes: logWindowMinutes
      });
      setDiagnosis(nextDiagnosis);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Diagnosis request failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleFollowUp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!diagnosis || !question.trim()) return;

    setIsAsking(true);
    setError(null);
    try {
      const exchange = await sendFollowUpQuestion(diagnosis.id, question.trim());
      setDiagnosis({
        ...diagnosis,
        follow_up_questions: [...diagnosis.follow_up_questions, exchange]
      });
      setQuestion("");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Follow-up request failed.");
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">MXCuBE</p>
          <h1>Fault Diagnosis</h1>
        </div>
        <div className={`status-pill status-${statusLabel.toLowerCase()}`}>
          {isSubmitting ? <LoaderCircle className="spin" size={16} /> : <Activity size={16} />}
          <span>{statusLabel}</span>
        </div>
      </header>

      <div className="workspace">
        <aside className="tool-pane">
          <div className="section-heading">
            <ClipboardList size={18} />
            <h2>Error Event</h2>
          </div>
          <form onSubmit={handleSubmit} className="event-form">
            <label>
              Device ID
              <input value={deviceId} onChange={(event) => setDeviceId(event.target.value)} />
            </label>
            <label>
              Error Code
              <input value={errorCode} onChange={(event) => setErrorCode(event.target.value)} />
            </label>
            <label>
              Message
              <textarea value={message} onChange={(event) => setMessage(event.target.value)} />
            </label>
            <label>
              Occurred At
              <input
                type="datetime-local"
                value={occurredAt}
                onChange={(event) => setOccurredAt(event.target.value)}
              />
            </label>
            <label>
              Log Window
              <input
                type="number"
                min={1}
                max={120}
                value={logWindowMinutes}
                onChange={(event) => setLogWindowMinutes(Number(event.target.value))}
              />
            </label>
            <button type="submit" disabled={isSubmitting} title="Run initial diagnosis">
              {isSubmitting ? <LoaderCircle className="spin" size={18} /> : <Send size={18} />}
              <span>Diagnose</span>
            </button>
          </form>
        </aside>

        <section className="result-pane">
          {error ? (
            <div className="notice error-notice">
              <AlertTriangle size={18} />
              <span>{error}</span>
            </div>
          ) : null}

          {!diagnosis ? (
            <div className="empty-state">
              <Activity size={40} />
              <p>No diagnosis selected.</p>
            </div>
          ) : (
            <>
              <div className="diagnosis-header">
                <div>
                  <p className="eyebrow">Diagnosis</p>
                  <h2>{diagnosis.error_event.error_code}</h2>
                  <p>{diagnosis.initial_diagnosis.summary}</p>
                </div>
                <div className="metrics">
                  <div>
                    <strong>{evidenceCount}</strong>
                    <span>Log Evidence</span>
                  </div>
                  <div>
                    <strong>{citationCount}</strong>
                    <span>Citations</span>
                  </div>
                </div>
              </div>

              <div className="content-grid">
                <section className="content-section">
                  <div className="section-heading">
                    <AlertTriangle size={18} />
                    <h3>Possible Causes</h3>
                  </div>
                  <div className="rows">
                    {diagnosis.initial_diagnosis.possible_causes.map((cause) => (
                      <article className="row-item" key={cause.cause}>
                        <div>
                          <strong>{cause.cause}</strong>
                          <p>{cause.reasoning}</p>
                        </div>
                        <span className={`tag tag-${cause.confidence}`}>{cause.confidence}</span>
                      </article>
                    ))}
                  </div>
                </section>

                <section className="content-section">
                  <div className="section-heading">
                    <ClipboardList size={18} />
                    <h3>Recommended Actions</h3>
                  </div>
                  <div className="rows">
                    {diagnosis.initial_diagnosis.recommended_actions.map((action) => (
                      <article className="row-item" key={action.action}>
                        <div>
                          <strong>{action.action}</strong>
                          {action.risk_note ? <p>{action.risk_note}</p> : null}
                        </div>
                        <span className={`tag tag-${action.priority}`}>{action.priority}</span>
                      </article>
                    ))}
                  </div>
                </section>
              </div>

              <section className="content-section evidence-section">
                <div className="section-heading">
                  <FileText size={18} />
                  <h3>Evidence</h3>
                </div>
                <div className="evidence-list">
                  {diagnosis.initial_diagnosis.citations.map((citation) => (
                    <article className="evidence-item" key={`${citation.source_type}-${citation.source_id}`}>
                      <span>{sourceLabel(citation.source_type)}</span>
                      <strong>{citation.title}</strong>
                      <p>{citation.excerpt}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className="content-section follow-up">
                <div className="section-heading">
                  <MessageSquare size={18} />
                  <h3>Follow-up Questions</h3>
                </div>
                <form className="follow-up-form" onSubmit={handleFollowUp}>
                  <input
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    placeholder="Ask about this diagnosis"
                  />
                  <button type="submit" disabled={isAsking || !question.trim()} title="Send follow-up question">
                    {isAsking ? <LoaderCircle className="spin" size={18} /> : <Send size={18} />}
                  </button>
                </form>
                <div className="conversation">
                  {diagnosis.follow_up_questions.map((exchange) => (
                    <article className="exchange" key={exchange.id}>
                      <strong>{exchange.question}</strong>
                      <p>{exchange.answer}</p>
                      {exchange.citations.length ? (
                        <div className="mini-citations">
                          <BookOpen size={15} />
                          <span>{exchange.citations.map((citation) => citation.title).join(", ")}</span>
                        </div>
                      ) : null}
                    </article>
                  ))}
                </div>
              </section>
            </>
          )}
        </section>
      </div>
    </main>
  );
}

export default App;

