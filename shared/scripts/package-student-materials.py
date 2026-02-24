#!/usr/bin/env python3
"""
Package student materials into a distributable zip file.

Collects student HTML notebooks, rendered Mermaid diagram PNGs, demo scripts,
and lab starters/solutions into a clean zip for distribution.

Usage:
    python3 shared/scripts/package-student-materials.py --modules 1,2,3 --output day1.zip
    python3 shared/scripts/package-student-materials.py --modules 4 --output day2.zip
    python3 shared/scripts/package-student-materials.py --modules 5,6,7 --output day3.zip
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


# Module number -> directory name mapping
MODULE_DIRS = {
    1: "01-intro-to-mulesoft",
    2: "02-anypoint-platform-tour",
    3: "03-api-design",
    4: "04-integrations-rest-soap-db",
    5: "05-dataweave",
    6: "06-salesforce-etl-batch",
    7: "07-deploy-manage-llm",
}

# Files/directories to exclude from copies
EXCLUDE_NAMES = {
    "__pycache__",
    ".DS_Store",
    ".git",
    ".gitignore",
    "Thumbs.db",
    ".mule",
    ".tooling-project",
    ".vscode",
    "target",
}

# File extensions to exclude
EXCLUDE_EXTENSIONS = {".pyc", ".class"}

# Directory name prefixes to exclude (e.g., embedded-dw_ ACB playground cache)
EXCLUDE_DIR_PREFIXES = ("embedded-dw_",)


def find_project_root() -> Path:
    """Find the project root by looking for CLAUDE.md."""
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "CLAUDE.md").exists():
            return parent
    print("ERROR: Could not find project root (no CLAUDE.md found)")
    sys.exit(1)


def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded from the zip."""
    for part in path.parts:
        if part in EXCLUDE_NAMES:
            return True
        if any(part.startswith(prefix) for prefix in EXCLUDE_DIR_PREFIXES):
            return True
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    return False


def check_mmdc_available() -> bool:
    """Check if mermaid-cli (mmdc) is installed."""
    try:
        result = subprocess.run(
            ["mmdc", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def extract_mermaid_diagrams(html_path: Path) -> list:
    """Extract Mermaid diagram text and captions from an HTML file.

    Returns list of (diagram_text, caption) tuples.
    """
    content = html_path.read_text(encoding="utf-8")

    # Pattern: <pre class="mermaid">DIAGRAM</pre> followed by caption
    # The caption is inside <p class="diagram-caption">
    diagram_pattern = re.compile(
        r'<pre\s+class="mermaid">\s*(.*?)\s*</pre>',
        re.DOTALL,
    )
    caption_pattern = re.compile(
        r'<p\s+class="diagram-caption">(.*?)</p>',
        re.DOTALL,
    )

    diagrams = diagram_pattern.findall(content)
    captions = caption_pattern.findall(content)

    # Pair diagrams with captions (they appear in order)
    results = []
    for i, diagram_text in enumerate(diagrams):
        caption = captions[i] if i < len(captions) else f"Figure {i + 1}"
        # Unescape HTML entities in both
        diagram_text = html.unescape(diagram_text.strip())
        caption = html.unescape(caption.strip())
        results.append((diagram_text, caption))

    return results


def caption_to_filename(caption: str, index: int) -> str:
    """Convert a figure caption to a safe PNG filename.

    "Figure 1: Point-to-point integration with 6 systems" -> "figure-01-point-to-point-integration.png"
    """
    # Try to extract figure number and title
    match = re.match(r"Figure\s+(\d+)\s*[:—\-]\s*(.*)", caption, re.IGNORECASE)
    if match:
        fig_num = int(match.group(1))
        title = match.group(2)
    else:
        fig_num = index + 1
        title = caption

    # Clean title: keep only alphanumeric and spaces, take first 6 words
    title = re.sub(r"[^a-zA-Z0-9\s]", "", title)
    words = title.split()[:6]
    slug = "-".join(w.lower() for w in words if w)

    if not slug:
        slug = "diagram"

    return f"figure-{fig_num:02d}-{slug}.png"


def render_mermaid_to_png(
    diagram_text: str, output_path: Path, config_path: Path
) -> bool:
    """Render a Mermaid diagram to PNG using mmdc."""
    with tempfile.NamedTemporaryFile(
        suffix=".mmd", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(diagram_text)
        mmd_path = f.name

    try:
        result = subprocess.run(
            [
                "mmdc",
                "-i", mmd_path,
                "-o", str(output_path),
                "-c", str(config_path),
                "-b", "#1A1F36",
                "--scale", "2",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"  WARNING: mmdc failed for {output_path.name}: {result.stderr.strip()}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"  WARNING: mmdc timed out for {output_path.name}")
        return False
    finally:
        os.unlink(mmd_path)


def collect_demo_files(module_dir: Path) -> list:
    """Find demo files in a module directory (non-HTML files at root level)."""
    demos = []
    for item in module_dir.iterdir():
        if item.is_file() and not item.name.endswith((".html", ".pyc")):
            if not should_exclude(item):
                demos.append(item)
    return demos


def collect_lab_dirs(module_dir: Path) -> list:
    """Find all lab directories (lab/, lab-modular/, lab-basics/, etc.)."""
    labs = []
    for item in module_dir.iterdir():
        if item.is_dir() and item.name.startswith("lab"):
            labs.append(item)
    return sorted(labs)


def copytree_filtered(src: Path, dst: Path):
    """Copy a directory tree, excluding unwanted files."""
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if should_exclude(item):
            continue
        dest_item = dst / item.name
        if item.is_dir():
            copytree_filtered(item, dest_item)
        elif item.is_file():
            shutil.copy2(item, dest_item)


def find_student_guide(project_root: Path, module_num: int) -> Path | None:
    """Look for a student guide for a specific module."""
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        return None

    # Check various naming patterns
    patterns = [
        f"student-guide-module-{module_num:02d}.md",
        f"student-guide-{module_num:02d}.md",
        f"module-{module_num:02d}-student-guide.md",
    ]
    for pattern in patterns:
        guide = docs_dir / pattern
        if guide.exists():
            return guide
    return None


def package_module(
    module_num: int,
    project_root: Path,
    staging_dir: Path,
    config_path: Path,
    has_mmdc: bool,
) -> dict:
    """Package a single module's student materials. Returns stats dict."""
    dir_name = MODULE_DIRS.get(module_num)
    if not dir_name:
        print(f"ERROR: Unknown module number {module_num}")
        return {"error": True}

    module_dir = project_root / "modules" / dir_name
    if not module_dir.exists():
        print(f"ERROR: Module directory not found: {module_dir}")
        return {"error": True}

    module_staging = staging_dir / dir_name
    module_staging.mkdir(parents=True, exist_ok=True)

    stats = {"diagrams": 0, "demos": 0, "labs": 0, "files": 0, "warnings": []}
    nn = f"{module_num:02d}"

    # 1. Copy student HTML
    student_html = module_dir / f"module-{nn}-student.html"
    if student_html.exists():
        shutil.copy2(student_html, module_staging / student_html.name)
        stats["files"] += 1
        print(f"  Copied {student_html.name}")
    else:
        msg = f"Student HTML not found: {student_html.name} — run generate-student-html.py first"
        stats["warnings"].append(msg)
        print(f"  WARNING: {msg}")
        # Fall back to instructor HTML if available
        instructor_html = module_dir / f"module-{nn}.html"
        if instructor_html.exists():
            shutil.copy2(instructor_html, module_staging / f"module-{nn}.html")
            stats["files"] += 1
            stats["warnings"].append("Fell back to instructor HTML (contains instructor notes)")

    # 2. Extract and render Mermaid diagrams
    source_html = student_html if student_html.exists() else module_dir / f"module-{nn}.html"
    if source_html.exists() and has_mmdc:
        diagrams = extract_mermaid_diagrams(source_html)
        if diagrams:
            diagrams_dir = module_staging / "diagrams"
            diagrams_dir.mkdir(exist_ok=True)
            for i, (diagram_text, caption) in enumerate(diagrams):
                png_name = caption_to_filename(caption, i)
                png_path = diagrams_dir / png_name
                if render_mermaid_to_png(diagram_text, png_path, config_path):
                    stats["diagrams"] += 1
                    stats["files"] += 1
                    print(f"  Rendered {png_name}")
                else:
                    stats["warnings"].append(f"Failed to render: {png_name}")
        else:
            print("  No Mermaid diagrams found")
    elif not has_mmdc:
        print("  Skipping diagram rendering (mmdc not available)")

    # 3. Copy demo files
    demos = collect_demo_files(module_dir)
    if demos:
        demos_dir = module_staging / "demos"
        demos_dir.mkdir(exist_ok=True)
        for demo in demos:
            shutil.copy2(demo, demos_dir / demo.name)
            stats["demos"] += 1
            stats["files"] += 1
            print(f"  Copied demo: {demo.name}")

    # 4. Copy lab directories
    lab_dirs = collect_lab_dirs(module_dir)
    for lab_dir in lab_dirs:
        dest_lab = module_staging / lab_dir.name
        copytree_filtered(lab_dir, dest_lab)
        file_count = sum(1 for _ in dest_lab.rglob("*") if _.is_file())
        stats["labs"] += 1
        stats["files"] += file_count
        print(f"  Copied {lab_dir.name}/ ({file_count} files)")

    # 5. Copy fixtures directory if it exists (Module 5 DataWeave exercises)
    fixtures_dir = module_dir / "fixtures"
    if fixtures_dir.exists() and fixtures_dir.is_dir():
        dest_fixtures = module_staging / "fixtures"
        copytree_filtered(fixtures_dir, dest_fixtures)
        file_count = sum(1 for _ in dest_fixtures.rglob("*") if _.is_file())
        stats["files"] += file_count
        print(f"  Copied fixtures/ ({file_count} files)")

    # 6. Copy student guide if it exists
    guide = find_student_guide(project_root, module_num)
    if guide:
        shutil.copy2(guide, module_staging / guide.name)
        stats["files"] += 1
        print(f"  Copied student guide: {guide.name}")

    return stats


def create_zip(staging_dir: Path, output_path: Path, zip_root_name: str):
    """Create the final zip from staged materials."""
    with ZipFile(output_path, "w", ZIP_DEFLATED) as zf:
        for file_path in sorted(staging_dir.rglob("*")):
            if file_path.is_file():
                # Archive path: zip_root_name/relative_path
                rel = file_path.relative_to(staging_dir)
                arcname = f"{zip_root_name}/{rel}"
                zf.write(file_path, arcname)


def main():
    parser = argparse.ArgumentParser(
        description="Package student materials into a distributable zip file"
    )
    parser.add_argument(
        "--modules",
        required=True,
        help="Comma-separated module numbers (e.g., 1,2,3)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output zip filename (e.g., day1.zip)",
    )
    args = parser.parse_args()

    # Parse module numbers
    try:
        module_nums = [int(n.strip()) for n in args.modules.split(",")]
    except ValueError:
        print("ERROR: --modules must be comma-separated integers (e.g., 1,2,3)")
        sys.exit(1)

    for n in module_nums:
        if n not in MODULE_DIRS:
            print(f"ERROR: Invalid module number {n}. Valid: 1-7")
            sys.exit(1)

    project_root = find_project_root()
    config_path = project_root / "shared" / "scripts" / "mermaid-config.json"
    output_path = Path(args.output).resolve()
    zip_root_name = output_path.stem  # "day1.zip" -> "day1"

    # Check mmdc availability
    has_mmdc = check_mmdc_available()
    if has_mmdc:
        print("mmdc (mermaid-cli) found — diagrams will be rendered to PNG")
    else:
        print("WARNING: mmdc not found — diagram rendering will be skipped")
        print("  Install with: npm install -g @mermaid-js/mermaid-cli")

    if not config_path.exists():
        print(f"WARNING: Mermaid config not found at {config_path}")
        print("  Diagrams will use default mmdc theme")

    # Stage materials in a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        staging = Path(tmpdir)
        total_stats = {"modules": 0, "diagrams": 0, "demos": 0, "labs": 0, "files": 0, "warnings": []}

        for module_num in sorted(module_nums):
            dir_name = MODULE_DIRS[module_num]
            print(f"\n{'='*60}")
            print(f"Module {module_num}: {dir_name}")
            print(f"{'='*60}")

            stats = package_module(module_num, project_root, staging, config_path, has_mmdc)

            if stats.get("error"):
                total_stats["warnings"].append(f"Module {module_num} had errors")
                continue

            total_stats["modules"] += 1
            total_stats["diagrams"] += stats["diagrams"]
            total_stats["demos"] += stats["demos"]
            total_stats["labs"] += stats["labs"]
            total_stats["files"] += stats["files"]
            total_stats["warnings"].extend(stats.get("warnings", []))

        # Create zip
        print(f"\n{'='*60}")
        print("Creating zip...")
        print(f"{'='*60}")
        create_zip(staging, output_path, zip_root_name)

    # Report
    zip_size = output_path.stat().st_size
    size_str = (
        f"{zip_size / (1024*1024):.1f} MB"
        if zip_size > 1024 * 1024
        else f"{zip_size / 1024:.0f} KB"
    )

    print(f"\nDone! Created {output_path.name} ({size_str})")
    print(f"  Modules: {total_stats['modules']}")
    print(f"  Diagrams: {total_stats['diagrams']}")
    print(f"  Demos: {total_stats['demos']}")
    print(f"  Labs: {total_stats['labs']}")
    print(f"  Total files: {total_stats['files']}")

    if total_stats["warnings"]:
        print(f"\nWarnings ({len(total_stats['warnings'])}):")
        for w in total_stats["warnings"]:
            print(f"  - {w}")

    sys.exit(0 if not total_stats["warnings"] else 0)


if __name__ == "__main__":
    main()
