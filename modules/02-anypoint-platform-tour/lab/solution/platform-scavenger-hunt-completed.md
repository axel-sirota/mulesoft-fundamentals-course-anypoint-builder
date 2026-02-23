# Platform Scavenger Hunt — Completed

Model answers for the instructor. Actual values may vary depending on platform version.

---

## Task 1: Exchange — Find the Salesforce Connector

Navigate to Exchange and search for the Salesforce Connector.

- What is the latest version? **Check Exchange for current version** (e.g., 10.20.0 — version updates frequently)
- What is the Group ID? **com.mulesoft.connectors**
- Name one operation listed in the documentation: **Query** (other valid answers: Create, Update, Upsert, Delete, Get Updated Objects)

---

## Task 2: Exchange — Find a Template

Search Exchange for "template". Find one that relates to Salesforce.

- Template name: **Salesforce to Salesforce Account Migration**
- What does it do (one sentence)? **Migrates Account records from one Salesforce org to another using batch processing.**

---

## Task 3: Design Center — Create a Spec

Go to Design Center and create a new API Specification.

- Choose RAML 1.0
- Name it: "My First API"
- Type this header:
  ```yaml
  #%RAML 1.0
  title: My First API
  version: v1
  ```
- Does it validate (green checkmark)? **Yes** — a valid RAML header with title and version will validate successfully.
- Delete the spec when done.

---

## Task 4: ACB — Create a Project

Open Anypoint Code Builder (cloud IDE or local VS Code extension).

- Create a new Mule project named "hello-mule"
- Can you see the canvas view? **Yes** — the visual flow canvas opens by default or via the canvas icon
- Can you see the XML view? **Yes** — toggle between canvas and XML using the editor tabs
- Can you see the connector palette on the left? **Yes** — the MuleSoft panel on the left shows available connectors and components
- Delete the project when done.

---

## Task 5: Runtime Manager

Navigate to Runtime Manager.

- How many applications are deployed? **0** (no apps deployed yet on a fresh trial account)
- What environments are available? **Sandbox** and **Design** (default environments on a trial account)

---

## Task 6: Connected Apps

Navigate to Access Management → Connected Apps (or Setup in your SF org).

- Can you find where Connected Apps are configured? **Yes** — in Anypoint Platform: Access Management → Connected Apps. In Salesforce: Setup → App Manager.
- (Don't create one yet — we'll do this in Module 6)
