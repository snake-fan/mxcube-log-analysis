# MXCuBE Fault Diagnosis

This context describes the language for equipment fault diagnosis in protein static crystal diffraction operations. It keeps the domain vocabulary stable across error intake, diagnosis, follow-up questions, and audit history.

## Language

**Error Event**:
A single equipment abnormality notification sent by the central control platform. It is the source event that starts one **Diagnosis**.
_Avoid_: Error message, alert, alarm

**Diagnosis**:
The fault investigation created from one **Error Event**. A **Diagnosis** collects the relevant equipment context, observed evidence, possible causes, recommendations, follow-up questions, and audit history for the same fault.
_Avoid_: Diagnostic Task, task, session

**Initial Diagnosis**:
The first diagnostic result produced for a **Diagnosis** from the triggering **Error Event**. It includes the first set of possible causes, evidence, recommendations, and risk notes before any follow-up questions are asked.
_Avoid_: First step diagnosis, first pass, preliminary task

**Log Evidence**:
The relevant log excerpts used as evidence in a **Diagnosis**. **Log Evidence** is selected from device logs for a specific time window and may be truncated or redacted before it is used.
_Avoid_: Raw logs, log dump, full log

**Device**:
A stable piece of equipment identified by a `device_id`. The project does not distinguish device model or device type as separate domain concepts unless the equipment set changes.
_Avoid_: Device Profile, Device Model, Device Type

**Manual Version**:
A versioned product manual associated with a **Device**. A new manual upload creates a new **Manual Version** instead of replacing the previous one.
_Avoid_: Current manual, overwritten manual

**Knowledge Source**:
Any source material that a **Diagnosis** can retrieve and cite, including product manuals, SOPs, FAQs, historical cases, and fault-code references.
_Avoid_: Knowledge document, document type, corpus item

**Follow-up Question**:
A user's later question about the same **Diagnosis** after the **Initial Diagnosis** has been produced. A **Follow-up Question** uses the existing diagnosis context unless the user explicitly asks for fresh log collection.
_Avoid_: New diagnosis, new task, chat session

## Example Dialogue

Dev: "When the central control platform reports an error, do we create a task?"

Domain expert: "Call it a Diagnosis. The Error Event is just the trigger; the Diagnosis is the whole investigation around that fault."

Dev: "If the user asks another question about the same fault later, is that a new Diagnosis?"

Domain expert: "No. It belongs to the same Diagnosis unless there is a new Error Event."

Dev: "What do we call the answer generated right after the Error Event arrives?"

Domain expert: "That is the Initial Diagnosis. Later questions may refine it, but they do not replace the Diagnosis."

Dev: "Should we attach the complete equipment log to the Diagnosis?"

Domain expert: "No. A Diagnosis uses Log Evidence: the relevant excerpts after time-window filtering and redaction."

Dev: "Do we need to model device type or model?"

Domain expert: "No. There are only about ten stable devices, so the Device ID is enough."

Dev: "What happens when a manual is updated?"

Domain expert: "Create a new Manual Version. Do not overwrite the old one."

Dev: "Should manuals, SOPs, FAQs, cases, and fault-code files each have separate ingestion models?"

Domain expert: "No. Treat them as Knowledge Sources with different source types."

Dev: "If the user asks why the system recommended a shutdown, is that another Diagnosis?"

Domain expert: "No. That is a Follow-up Question in the same Diagnosis."
