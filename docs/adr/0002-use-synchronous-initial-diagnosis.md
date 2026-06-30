# Use Synchronous Initial Diagnosis

The backend generates the Initial Diagnosis within the request that receives an Error Event instead of placing the work on a background queue. This matches the intended product scope: the frontend can show a loading state while the backend performs one compact diagnosis pass, and the system avoids queueing infrastructure until diagnosis latency or reliability requirements prove that it is needed.
