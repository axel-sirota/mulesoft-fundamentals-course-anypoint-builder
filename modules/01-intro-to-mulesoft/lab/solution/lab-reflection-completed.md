# Lab Reflection — Module 1: Why MuleSoft?

After running both approaches (demo-coupled.py and the Mule flow), answer these questions:

---

## 1. What happens when the source API is unavailable in each approach?

**Python script:**
The script crashes with a `ConnectionError` exception. No structured error message, no logging, no alerting. If this runs in production, nobody knows it failed until a downstream consumer reports missing data.

**Mule flow:**
The Mule flow catches the connectivity error in the Try scope's `on-error-continue` handler and returns a structured JSON response with HTTP 503 status: `{"error": "Source API unavailable", "detail": "...", "timestamp": "..."}`. The flow stays running and can serve subsequent requests. In production, Runtime Manager would log this event and could trigger alerts.

---

## 2. If you needed to add a second data source, what would you change in each approach?

**Python script:**
You'd duplicate the entire script (or add another `requests.get()` call with a new hardcoded URL). The transform logic gets duplicated again. Now you have two scripts to maintain, and if the field mapping changes, you fix both.

**Mule flow:**
Add another HTTP Request connector (or use Scatter-Gather for parallel calls). The DataWeave transform can merge results from both sources. URLs come from configuration properties — no code changes needed to point at a different host. The Scatter-Gather pattern (Module 4) makes this clean and parallel.

---

## 3. Which would you trust running at 3am? Why?

**Your answer:**
The Mule flow — because it has structured error handling (the Try scope catches connectivity failures and returns a proper error response instead of crashing), monitoring (Runtime Manager provides logs, dashboards, and alerts), auto-restart capability, and configuration-driven URLs (no hardcoded values that require code changes). If something fails, you get notified and can diagnose the issue from the dashboard. The Python script just silently crashes.
