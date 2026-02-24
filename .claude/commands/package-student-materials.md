---
description: Package student materials into a distributable zip file
---

# Package Student Materials Command

Packages student-facing course materials (HTML notebooks, rendered Mermaid diagram PNGs, demos, and labs) into a zip file for distribution.

## Inputs
- **Module numbers**: Comma-separated list (e.g., `1,2,3`)
- **Output filename**: Zip file name (e.g., `day1.zip`)

## Execution Flow

**1. Parse Arguments**
- Extract module numbers and output filename from the user's request.
- Valid modules: 1-7. Output must end in `.zip`.
- All zips go into the gitignored `zips/` directory (e.g., `zips/day1.zip`).

**2. Verify Student HTML Files Exist**
- For each requested module, check that `module-{NN}-student.html` exists.
- If missing, regenerate it:
  ```bash
  .venv/bin/python3 shared/scripts/generate-student-html.py modules/{module-dir}/module-{NN}.html
  ```

**3. Run Packaging Script**
```bash
.venv/bin/python3 shared/scripts/package-student-materials.py --modules {modules} --output zips/{output}
```

**4. Report Results**
- Show the zip file size and contents summary.
- List any warnings (missing files, failed diagram renders).
- Run `unzip -l zips/{output}` to show the zip contents.

**5. Upload to S3**
- Upload the zip to the S3 bucket `courses.axel.net` under the `Mulesoft Development Course/` folder.
- Each zip must be publicly accessible (`--acl public-read`).
```bash
aws s3 cp zips/{output} "s3://courses.axel.net/Mulesoft Development Course/{output}" --acl public-read
```
- Confirm the upload succeeded and show the public URL.

## Zip Contents Per Module

Each module folder in the zip contains:
- `module-{NN}-student.html` — Student-facing HTML notebook (no instructor notes)
- `diagrams/` — Rendered PNG of every Mermaid diagram in the notebook
- `demos/` — Demo artifacts: completed versions of instructor demos (e.g., `demo-coupled.py`, `demo-customer-api.raml`). These are the instructor's safety net and the student's take-home reference.
- `lab/` — Lab starter and solution directories. When the demo builds the same thing as the lab, `lab/solution/` IS the demo artifact — no separate file in demos/.
- `lab-modular/` — Bonus lab if present
- Student guide markdown if present in `docs/`

## Usage

`/package-student-materials 1,2,3 day1.zip` -> Packages modules 1-3 into day1.zip
`/package-student-materials 4 day2.zip` -> Packages module 4 into day2.zip
`/package-student-materials 5,6,7 day3.zip` -> Packages modules 5-7 into day3.zip

## Prerequisites
- `mmdc` (mermaid-cli) installed for diagram rendering: `npm install -g @mermaid-js/mermaid-cli`
- Student HTML files generated (script will warn if missing)
- AWS CLI configured with access to the `courses.axel.net` S3 bucket
