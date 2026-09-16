import re
import uuid
import logging
from typing import Optional, Dict, Any, List
from app.models.schema import ArtifactDB
from app.utils.security import sanitize_html, prepare_iframe_document

logger = logging.getLogger("lenny_assistant.artifact_generator")

ARTIFACT_SYSTEM_INSTRUCTION = """
When the user asks for a document, layout, calculator, canvas, dashboard, template, or rendered artifact:
1. Create a full, self-contained, beautifully styled HTML/CSS snippet or Markdown document.
2. Wrap your artifact output in XML tags like this:
<artifact title="Descriptive Title Here" type="html|markdown|code">
... artifact content here ...
</artifact>

For HTML artifacts:
- Make them visually stunning using modern dark mode styling, CSS grid/flexbox, interactive buttons/inputs, and clean typography.
- Ensure all CSS is embedded in a <style> block.
- Ensure interactive JavaScript (if any) is clean and inline.
"""

class ArtifactGenerator:
    @staticmethod
    def parse_artifacts_from_response(response_text: str) -> List[Dict[str, str]]:
        """
        Parses <artifact title="..." type="..."> content </artifact> blocks from assistant output.
        Also fallback parses standard code fences if requested.
        """
        artifacts = []
        
        # Pattern 1: <artifact title="..." type="...">...</artifact>
        pattern = r'<artifact\s+title=["\'](.*?)["\']\s+type=["\'](.*?)["\']\s*>(.*?)</artifact>'
        matches = re.findall(pattern, response_text, re.DOTALL | re.IGNORECASE)

        for title, artifact_type, content in matches:
            content_clean = content.strip()
            artifacts.append({
                "title": title.strip(),
                "artifact_type": artifact_type.strip().lower(),
                "content": content_clean
            })

        # Pattern 2: Fallback markdown code fence detection if user requested HTML/CSS preview directly
        if not artifacts:
            html_fence_pattern = r'```html\s*\n(.*?)```'
            html_matches = re.findall(html_fence_pattern, response_text, re.DOTALL | re.IGNORECASE)
            for idx, content in enumerate(html_matches, start=1):
                artifacts.append({
                    "title": f"Interactive HTML Artifact {idx}",
                    "artifact_type": "html",
                    "content": content.strip()
                })

        return artifacts

    @staticmethod
    def prepare_rendered_artifact(artifact_type: str, content: str, title: str) -> str:
        """
        Prepares the artifact for frontend preview rendering.
        HTML artifacts are sanitized and wrapped in an isolated iframe document wrapper.
        """
        if artifact_type == "html":
            sanitized = sanitize_html(content)
            return prepare_iframe_document(sanitized, title=title)
        return content
