Update the BMAD Product Requirements Document (PRD) ingestion and generation workflows to enforce the use of a predefined template for all PRD generation, moving away from dynamically creating sections.

Specific Requirements
Mandate Template Usage: The system must use the file named PRD-template.md located in the /templates directory for all new PRD generation. This template contains a predefined set of sections and classifications.

Ingestion & Analysis Workflow:

Modify the existing ingestion workflow to ensure that during the ingestion and analysis of raw input, all data is categorized based on the sections and classifications defined in PRD-template.md. The analysis must align with the template's structure.

Generation Workflow:

Modify the generation workflow to populate the PRD-template.md with the analyzed data.

The generated PRD must strictly adhere to the section headings, order, and overall structure of the template.

Do not create any new sections or alter the existing ones from the template. The output must be a completed version of the template.

Error Handling: If a piece of ingested information cannot be categorized into one of the template's predefined sections, the workflow should flag that information for human review instead of trying to force it into an ill-fitting section or ignoring it.

Technical Context & Implementation Details
File Path: The absolute path to the template is /path/to/project/templates/PRD-template.md.

Output Format: The final output should be a markdown (.md) file.

Desired Outcome
A robust workflow where the final PRD is a complete, well-structured document that follows the PRD-template.md exactly, ensuring consistency and predictability across all generated documents within the BMAD system.