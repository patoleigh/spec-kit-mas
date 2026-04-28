"""Approved project stack profiles for stack-aware initialization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


STACK_CONTEXT_FILE = Path(".specify/context/stack.md")


@dataclass(frozen=True)
class StackProfile:
    """Company-approved stack metadata and planning guidance."""

    key: str
    name: str
    purpose: str
    constraints: tuple[str, ...]
    typical_risks: tuple[str, ...]
    expected_artifacts: tuple[str, ...]
    preferred_practices: tuple[str, ...]
    avoid: tuple[str, ...]


APPROVED_STACKS: dict[str, StackProfile] = {
    "cakephp2-mysql": StackProfile(
        key="cakephp2-mysql",
        name="CakePHP 2.x + MySQL",
        purpose="Legacy business applications and admin-heavy workflows that must remain inside the existing CakePHP 2.x estate.",
        constraints=(
            "Preserve CakePHP 2.x conventions, controller/model/view boundaries, and legacy bootstrap behavior.",
            "Favor incremental MySQL schema changes that are reversible and safe for existing data.",
            "Work within the current deployment model and shared hosting or legacy infrastructure assumptions.",
        ),
        typical_risks=(
            "Tight coupling in legacy code paths and side effects across reused models or components.",
            "Slow queries, pagination regressions, or export bottlenecks on large back-office datasets.",
            "Fragile migrations or manual production fixes when schema changes are insufficiently planned.",
        ),
        expected_artifacts=(
            "Updated controllers, models, views, and any shared components or helpers touched by the feature.",
            "Explicit MySQL schema or migration notes plus validation and rollback steps.",
            "QA notes covering admin workflows, listings, filters, exports, and permission-sensitive paths.",
        ),
        preferred_practices=(
            "Reuse established CakePHP patterns before introducing new abstractions.",
            "Document query, indexing, and pagination implications for admin or reporting screens.",
            "Keep changes traceable and low-risk, especially around shared models and operational data.",
        ),
        avoid=(
            "Do not introduce architecture that bypasses CakePHP conventions without a recorded exception.",
            "Do not hide schema changes, manual SQL, or production data fixes outside the plan.",
            "Do not ship large-listing or export changes without operational validation.",
        ),
    ),
    "moodle5-plugin": StackProfile(
        key="moodle5-plugin",
        name="Moodle 5 Plugin",
        purpose="Isolated Moodle 5 functionality delivered as a plugin that fits Moodle extension points and release processes.",
        constraints=(
            "Stay inside Moodle 5 plugin APIs, capabilities, events, privacy, and upgrade-step conventions.",
            "Preserve compatibility with the hosting Moodle instance and supported plugin boundaries.",
            "Respect Moodle language strings, renderer patterns, and admin UX expectations.",
        ),
        typical_risks=(
            "Capability or privacy regressions that expose restricted course, user, or grading data.",
            "Upgrade step failures, missing version bumps, or inconsistent install and rollback behavior.",
            "Divergence from Moodle APIs that increases maintenance cost across upgrades.",
        ),
        expected_artifacts=(
            "Plugin structure updates such as classes, db, lang, templates or pages, and relevant tests.",
            "Upgrade and installation notes, capabilities, permissions, privacy, and event impacts.",
            "Admin and teacher workflow validation for Moodle-specific navigation and forms.",
        ),
        preferred_practices=(
            "Use Moodle extension points, capability checks, and forms APIs consistently.",
            "Plan for install, upgrade, downgrade, and privacy/data-export implications up front.",
            "Keep plugin responsibilities focused and well-bounded from core customizations.",
        ),
        avoid=(
            "Do not patch Moodle core when a plugin extension point is the correct path.",
            "Do not skip capability, privacy, or upgrade-step analysis for new data or workflows.",
            "Do not introduce custom front-end patterns that fight Moodle's established UX unless justified.",
        ),
    ),
    "moodle5-portal": StackProfile(
        key="moodle5-portal",
        name="Moodle 5 Portal",
        purpose="Broader Moodle-based portals and institutional workflows that span multiple modules, audiences, or operational teams.",
        constraints=(
            "Fit the existing portal information architecture, Moodle 5 capabilities, and operational ownership model.",
            "Treat integrations, reporting, and data synchronization as first-class planning concerns.",
            "Preserve portal-wide consistency for navigation, permissions, and institutional branding or templating.",
        ),
        typical_risks=(
            "Cross-module permission leakage or inconsistent behavior between portal areas.",
            "Reporting, cohort, enrollment, or synchronization issues that affect institutions at scale.",
            "Operational drift when portal workflows are planned without admin and support teams in mind.",
        ),
        expected_artifacts=(
            "Portal area structure, module touchpoints, integration notes, and affected operational workflows.",
            "Data-flow or reporting impacts across portal surfaces, including pagination and exports where relevant.",
            "Deployment, rollback, and post-release validation steps for institution-facing operations.",
        ),
        preferred_practices=(
            "Document which portal roles, cohorts, reports, and operational teams are affected.",
            "Design for supportability, observability, and safe rollout across shared institutional environments.",
            "Keep Moodle-native patterns and portal conventions aligned instead of mixing ad hoc solutions.",
        ),
        avoid=(
            "Do not treat portal features as isolated if they cross permissions, reporting, or integrations.",
            "Do not add institution-facing workflow changes without rollback and support validation.",
            "Do not bypass shared portal conventions for navigation, logging, or data handling.",
        ),
    ),
    "laravel-inertia-react": StackProfile(
        key="laravel-inertia-react",
        name="Laravel + Inertia + React",
        purpose="Modern Laravel applications with server-driven routing and React-based UI through Inertia.",
        constraints=(
            "Keep Laravel as the backend source of truth for routing, authorization, validation, and data access.",
            "Use Inertia page patterns and React components without turning the app into an unmanaged SPA.",
            "Plan backend and frontend changes together, including shared form, policy, and API contract expectations.",
        ),
        typical_risks=(
            "Boundary drift between Laravel controllers, Inertia responses, and React page responsibilities.",
            "Authorization, validation, or state-management gaps between server and client behavior.",
            "Inconsistent component patterns, duplicated logic, or deployment issues across PHP and front-end assets.",
        ),
        expected_artifacts=(
            "Laravel routes, controllers, policies, requests, models, migrations, and tests as needed.",
            "Inertia pages, React components, form flows, and front-end test notes where the feature changes UI.",
            "Deployment and QA notes for migrations, assets, queues, and environment-sensitive behavior.",
        ),
        preferred_practices=(
            "Keep validation, authorization, and business rules centered in Laravel.",
            "Use Inertia page props intentionally and keep React components focused and reusable.",
            "Plan migrations, seed data, asset builds, and end-to-end admin flows together.",
        ),
        avoid=(
            "Do not introduce parallel front-end data flows that bypass Laravel or Inertia without justification.",
            "Do not duplicate authorization or validation logic across backend and frontend unnecessarily.",
            "Do not ship UI-heavy changes without covering related backend constraints, QA, and rollback steps.",
        ),
    ),
}


def approved_stack_ids() -> tuple[str, ...]:
    """Return approved stack identifiers in stable order."""

    return tuple(APPROVED_STACKS.keys())


def approved_stack_help() -> str:
    """Return a human-readable approved stack list."""

    return ", ".join(approved_stack_ids())


def get_stack_profile(stack_id: str | None) -> StackProfile | None:
    """Resolve an approved stack profile by identifier."""

    if not stack_id:
        return None
    return APPROVED_STACKS.get(stack_id)


def render_stack_context(profile: StackProfile) -> str:
    """Render the durable project stack context file."""

    def bullets(items: tuple[str, ...]) -> str:
        return "\n".join(f"- {item}" for item in items)

    return (
        f"---\n"
        f"stack_id: {profile.key}\n"
        f"stack_name: {profile.name}\n"
        f"---\n\n"
        f"# Project Stack Profile\n\n"
        f"## Selected Stack\n\n"
        f"- **ID**: {profile.key}\n"
        f"- **Name**: {profile.name}\n\n"
        f"## Purpose / Typical Use\n\n"
        f"- {profile.purpose}\n\n"
        f"## Main Constraints\n\n"
        f"{bullets(profile.constraints)}\n\n"
        f"## Typical Risks\n\n"
        f"{bullets(profile.typical_risks)}\n\n"
        f"## Expected Artifacts\n\n"
        f"{bullets(profile.expected_artifacts)}\n\n"
        f"## Preferred Practices\n\n"
        f"{bullets(profile.preferred_practices)}\n\n"
        f"## Things To Avoid\n\n"
        f"{bullets(profile.avoid)}\n"
    )


def write_stack_context(project_root: Path, profile: StackProfile) -> Path:
    """Write the durable stack context file into the project."""

    destination = project_root / STACK_CONTEXT_FILE
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_stack_context(profile), encoding="utf-8")
    return destination
