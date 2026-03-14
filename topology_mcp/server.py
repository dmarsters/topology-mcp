#!/usr/bin/env python3
"""
Topology MCP Server — Mathematical topology mapped to aesthetic parameter space.

Three-layer architecture:
    Layer 1: Pure taxonomy lookup (0 tokens)
    Layer 2: Deterministic computation (0 tokens)
    Layer 3: Claude synthesis (~100-200 tokens)

Provides tools for navigating a 5D topology parameter space
(genus_complexity, curvature_uniformity, boundary_definition,
orientability_degree, connectivity_density) with canonical states
derived from mathematical surfaces.

Compatible with aesthetic-dynamics-core for Tier 4D multi-domain
composition via forced limit cycles.
"""

import json
from typing import Optional, List, Dict
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastmcp import FastMCP

from taxonomy import (
    PARAMETER_NAMES,
    CANONICAL_STATES,
    VISUAL_TYPES,
    SURFACES,
    PRESETS,
)
from computation import (
    compute_trajectory,
    generate_preset_trajectory,
    apply_preset,
    extract_prompt_vocabulary,
    find_nearest_canonical,
    get_domain_registry_config,
)

# ---------------------------------------------------------------------------
# Server initialization
# ---------------------------------------------------------------------------
mcp = FastMCP("topology_mcp")


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------
class ResponseFormat(str, Enum):
    """Output format for responses."""
    MARKDOWN = "markdown"
    JSON = "json"


def _format_response(data: dict, fmt: ResponseFormat) -> str:
    """Format response as JSON or Markdown."""
    if fmt == ResponseFormat.JSON:
        return json.dumps(data, indent=2)
    # Markdown: caller provides pre-formatted string
    return data.get("markdown", json.dumps(data, indent=2))


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 1 TOOLS — Pure taxonomy lookup (0 tokens)
# ═══════════════════════════════════════════════════════════════════════════

# --- get_server_info -------------------------------------------------------

@mcp.tool(
    name="get_server_info",
    annotations={
        "title": "Topology Server Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_server_info() -> str:
    """Get comprehensive information about the Topology MCP server.

    Layer 1: Pure reference (0 tokens).

    Returns server metadata, capabilities, parameter space dimensions,
    canonical states, rhythmic presets, visual vocabulary types, and
    Tier 4D compatibility status.
    """
    preset_summary = {}
    for pname, pdata in PRESETS.items():
        preset_summary[pname] = {
            "period": pdata["period"],
            "pattern": pdata["pattern"],
            "states": f"{pdata['state_a']} ↔ {pdata['state_b']}",
        }

    info = {
        "server": "topology_mcp",
        "description": "Maps mathematical topology concepts (surfaces, manifolds, invariants) "
                       "to compositional parameters, rhythmic dynamics, and image generation prompts",
        "version": "1.0.0",
        "surfaces_available": len(SURFACES),
        "parameter_space": {
            "dimensions": 5,
            "parameters": PARAMETER_NAMES,
            "bounds": [0.0, 1.0],
            "canonical_states": len(CANONICAL_STATES),
        },
        "layer_structure": {
            "layer_1": "Topological taxonomy (surfaces, invariants, canonical states)",
            "layer_2": "Trajectory computation, preset oscillation, prompt vocabulary extraction",
            "layer_3": "Claude synthesis of visual descriptions",
        },
        "cost_profile": {
            "layer_1": "0 tokens (pure lookup)",
            "layer_2": "0 tokens (deterministic computation)",
            "layer_3": "~100-200 tokens (Claude synthesis)",
        },
        "phase_1a_trajectory": {
            "enabled": True,
            "method": "cosine_interpolation",
            "tools": ["compute_topology_trajectory"],
        },
        "phase_2_6_rhythmic": {
            "enabled": True,
            "presets": preset_summary,
            "all_periods": sorted(set(p["period"] for p in PRESETS.values())),
            "tools": ["list_topology_presets", "apply_topology_preset"],
        },
        "phase_2_7_visualization": {
            "enabled": True,
            "visual_types": list(VISUAL_TYPES.keys()),
            "visual_type_count": len(VISUAL_TYPES),
            "prompt_modes": ["composite", "split_keywords", "descriptive"],
            "tools": ["generate_topology_attractor_prompt"],
        },
        "tier_4d_composition": {
            "compatible": True,
            "domain_id": "topology",
            "tools": ["get_topology_coordinates", "get_topology_domain_registry_config"],
        },
        "compatible_bricks": [
            "aesthetic-dynamics-core — Phase 1A trajectory computation (required)",
            "constellation-composition — Stellar patterns [Periods: 15, 18, 22, 24, 28]",
            "heraldic-blazonry — Ceremonial patterns [Periods: 12, 16, 22, 25, 30]",
            "diatom-morph — Biological structure [Periods: 12, 15, 20, 30]",
            "catastrophe-morph — Morphology [Periods: 15, 16, 20, 22]",
        ],
    }
    return json.dumps(info, indent=2)


# --- list_all_surfaces -----------------------------------------------------

@mcp.tool(
    name="list_all_surfaces",
    annotations={
        "title": "List Topological Surfaces",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_all_surfaces(
    response_format: ResponseFormat = ResponseFormat.JSON,
) -> str:
    """List all topological surfaces in the taxonomy with their invariants.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns surface names, genus, Euler characteristic, orientability,
    boundary status, curvature type, fundamental group, and associated
    canonical state.
    """
    if response_format == ResponseFormat.JSON:
        return json.dumps({"surfaces": SURFACES, "count": len(SURFACES)}, indent=2)

    lines = ["# Topological Surfaces", ""]
    for name, data in SURFACES.items():
        lines.append(f"## {name.replace('_', ' ').title()}")
        lines.append(f"- **Genus**: {data['genus']}")
        lines.append(f"- **Euler χ**: {data['euler_characteristic']}")
        lines.append(f"- **Orientable**: {data['orientable']}")
        lines.append(f"- **Boundary**: {data['boundary']}")
        lines.append(f"- **Curvature**: {data['curvature']}")
        lines.append(f"- **π₁**: {data['fundamental_group']}")
        lines.append(f"- **Canonical state**: `{data['canonical_state']}`")
        lines.append(f"- {data['description']}")
        lines.append("")
    return "\n".join(lines)


# --- get_topology_coordinates ----------------------------------------------

class CoordinateInput(BaseModel):
    """Input for coordinate lookup."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(
        ...,
        description="Canonical state name (e.g. 'torus_circulation') or surface name (e.g. 'torus')",
        min_length=1,
        max_length=100,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.JSON,
        description="Output format: 'json' for structured or 'markdown' for readable",
    )


@mcp.tool(
    name="get_topology_coordinates",
    annotations={
        "title": "Get Topology Coordinates",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_topology_coordinates(params: CoordinateInput) -> str:
    """Extract normalized 5D parameter coordinates for a canonical state or surface name.

    Layer 1: Pure taxonomy lookup (0 tokens).

    If a canonical state name is given (e.g. 'torus_circulation'), returns its
    exact coordinates. If a surface name is given (e.g. 'torus'), returns the
    associated canonical state's coordinates.

    Coordinates are suitable for:
    - Trajectory computation (Phase 1A)
    - Rhythmic composition input (Phase 2.6)
    - Attractor visualization (Phase 2.7)
    - Multi-domain composition (Tier 4D)

    Args:
        params (CoordinateInput): Validated input containing:
            - name (str): Canonical state or surface name
            - response_format (ResponseFormat): Output format

    Returns:
        str: 5D coordinates in requested format
    """
    name = params.name.lower().strip()

    # Direct canonical state match
    if name in CANONICAL_STATES:
        result = {
            "name": name,
            "type": "canonical_state",
            "coordinates": CANONICAL_STATES[name],
            "parameter_names": PARAMETER_NAMES,
        }
    # Surface name match
    elif name in SURFACES:
        cs_name = SURFACES[name]["canonical_state"]
        result = {
            "name": name,
            "type": "surface",
            "canonical_state": cs_name,
            "coordinates": CANONICAL_STATES[cs_name],
            "surface_invariants": {
                "genus": SURFACES[name]["genus"],
                "euler_characteristic": SURFACES[name]["euler_characteristic"],
                "orientable": SURFACES[name]["orientable"],
            },
            "parameter_names": PARAMETER_NAMES,
        }
    else:
        return json.dumps({
            "error": f"Unknown name '{params.name}'",
            "available_canonical_states": list(CANONICAL_STATES.keys()),
            "available_surfaces": list(SURFACES.keys()),
        }, indent=2)

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(result, indent=2)

    lines = [f"# Coordinates: {name}", ""]
    for p in PARAMETER_NAMES:
        lines.append(f"- **{p}**: {result['coordinates'][p]:.2f}")
    return "\n".join(lines)


# --- get_topology_visual_types ---------------------------------------------

@mcp.tool(
    name="get_topology_visual_types",
    annotations={
        "title": "Get Topology Visual Types",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_topology_visual_types() -> str:
    """List all topology visual types with their coordinates and keywords.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns the complete visual vocabulary catalog used by the attractor
    prompt generator. Each visual type represents a region of the 5D
    topology parameter space with associated image-generation keywords.
    """
    output = {}
    for vt_name, vt_data in VISUAL_TYPES.items():
        output[vt_name] = {
            "coordinates": vt_data["coordinates"],
            "keywords": vt_data["keywords"],
            "keyword_count": len(vt_data["keywords"]),
        }

    return json.dumps({
        "visual_types": output,
        "count": len(VISUAL_TYPES),
        "parameter_names": PARAMETER_NAMES,
    }, indent=2)


# --- list_topology_presets -------------------------------------------------

@mcp.tool(
    name="list_topology_presets",
    annotations={
        "title": "List Topology Presets",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_topology_presets(
    response_format: ResponseFormat = ResponseFormat.JSON,
) -> str:
    """List all available Phase 2.6 rhythmic presets with their parameters.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns preset names, periods, oscillation patterns, state pairs,
    and descriptions. Presets define temporal oscillation patterns between
    canonical topology states for rhythmic composition and Tier 4D
    multi-domain limit cycle discovery.
    """
    if response_format == ResponseFormat.JSON:
        return json.dumps({
            "presets": PRESETS,
            "count": len(PRESETS),
            "all_periods": sorted(set(p["period"] for p in PRESETS.values())),
        }, indent=2)

    lines = ["# Topology Rhythmic Presets", ""]
    for pname, pdata in PRESETS.items():
        lines.append(f"## {pname}")
        lines.append(f"- **Period**: {pdata['period']} steps")
        lines.append(f"- **Pattern**: {pdata['pattern']}")
        lines.append(f"- **States**: `{pdata['state_a']}` ↔ `{pdata['state_b']}`")
        lines.append(f"- {pdata['description']}")
        lines.append("")
    return "\n".join(lines)


# --- search_surfaces -------------------------------------------------------

class SurfaceSearchInput(BaseModel):
    """Input for surface search."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    orientable: Optional[bool] = Field(
        default=None, description="Filter by orientability (True/False)"
    )
    has_boundary: Optional[bool] = Field(
        default=None, description="Filter by presence of boundary"
    )
    max_genus: Optional[int] = Field(
        default=None, description="Maximum genus to include", ge=0, le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.JSON,
        description="Output format",
    )


@mcp.tool(
    name="search_surfaces",
    annotations={
        "title": "Search Topological Surfaces",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def search_surfaces(params: SurfaceSearchInput) -> str:
    """Search topological surfaces by invariant properties.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Filter the surface catalog by orientability, boundary presence,
    and genus constraints.

    Args:
        params (SurfaceSearchInput): Filter criteria containing:
            - orientable (Optional[bool]): Filter by orientability
            - has_boundary (Optional[bool]): Filter by boundary presence
            - max_genus (Optional[int]): Maximum genus to include
            - response_format (ResponseFormat): Output format

    Returns:
        str: Matching surfaces in requested format
    """
    matches = {}
    for name, data in SURFACES.items():
        if params.orientable is not None and data["orientable"] != params.orientable:
            continue
        if params.has_boundary is not None and data["boundary"] != params.has_boundary:
            continue
        if params.max_genus is not None and data["genus"] is not None:
            if data["genus"] > params.max_genus:
                continue
        matches[name] = data

    result = {"matches": matches, "count": len(matches)}
    if params.response_format == ResponseFormat.JSON:
        return json.dumps(result, indent=2)

    lines = [f"# Search Results ({len(matches)} surfaces)", ""]
    for name, data in matches.items():
        lines.append(f"- **{name.replace('_', ' ').title()}** — genus {data['genus']}, "
                      f"{'orientable' if data['orientable'] else 'non-orientable'}, "
                      f"{'bounded' if data['boundary'] else 'closed'}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# LAYER 2 TOOLS — Deterministic computation (0 tokens)
# ═══════════════════════════════════════════════════════════════════════════

# --- compute_topology_trajectory -------------------------------------------

class TrajectoryInput(BaseModel):
    """Input for trajectory computation."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    state_a: str = Field(
        ..., description="Starting canonical state name (e.g. 'sphere_purity')"
    )
    state_b: str = Field(
        ..., description="Target canonical state name (e.g. 'genus3_labyrinth')"
    )
    steps: int = Field(
        default=10,
        description="Number of interpolation steps (2–100)",
        ge=2,
        le=100,
    )


@mcp.tool(
    name="compute_topology_trajectory",
    annotations={
        "title": "Compute Topology Trajectory",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def compute_topology_trajectory(params: TrajectoryInput) -> str:
    """Compute smooth interpolation trajectory between two canonical states.

    Layer 2: Deterministic interpolation (0 tokens).

    Uses cosine ease-in-out for perceptually smooth transitions. Each step
    includes full 5D coordinates suitable for attractor prompt generation
    or multi-domain composition input.

    Args:
        params (TrajectoryInput): Validated input containing:
            - state_a (str): Starting canonical state
            - state_b (str): Target canonical state
            - steps (int): Number of interpolation steps (2–100)

    Returns:
        str: JSON trajectory with per-step 5D coordinates
    """
    try:
        result = compute_trajectory(params.state_a, params.state_b, params.steps)
        return json.dumps(result, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)


# --- apply_topology_preset -------------------------------------------------

class PresetApplyInput(BaseModel):
    """Input for applying a rhythmic preset."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    preset_name: str = Field(
        ..., description="Name of the rhythmic preset (e.g. 'genus_ascent')"
    )
    step: int = Field(
        default=0,
        description="Step index within the preset cycle (wraps modulo period)",
        ge=0,
    )


@mcp.tool(
    name="apply_topology_preset",
    annotations={
        "title": "Apply Topology Preset",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def apply_topology_preset(params: PresetApplyInput) -> str:
    """Apply a Phase 2.6 rhythmic preset at a specific step.

    Layer 2: Deterministic computation (0 tokens).

    Returns the 5D coordinates at the given step within the preset's
    oscillation cycle. Step wraps modulo period for continuous looping.

    Args:
        params (PresetApplyInput): Validated input containing:
            - preset_name (str): Preset to apply
            - step (int): Step index (wraps modulo period)

    Returns:
        str: JSON with step, period, phase, and 5D coordinates
    """
    try:
        result = apply_preset(params.preset_name, params.step)
        return json.dumps(result, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)


# --- generate_topology_attractor_prompt ------------------------------------

class AttractorPromptInput(BaseModel):
    """Input for generating image-generation prompts from coordinates."""
    model_config = ConfigDict(extra="forbid")

    coordinates: Optional[Dict] = Field(
        default=None,
        description=(
            "5D parameter coordinates. Keys: genus_complexity, curvature_uniformity, "
            "boundary_definition, orientability_degree, connectivity_density. "
            "Values: 0.0–1.0. If omitted, use canonical_state instead."
        ),
    )
    canonical_state: Optional[str] = Field(
        default=None,
        description="Name of a canonical state to use as source coordinates",
    )
    mode: str = Field(
        default="composite",
        description="'composite' = single blended prompt, 'split_keywords' = categorized lists, 'descriptive' = narrative paragraph",
    )
    strength: float = Field(
        default=1.0,
        description="Blending strength 0.0–1.0 (lower = more neutral vocabulary)",
        ge=0.0,
        le=1.0,
    )

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        allowed = {"composite", "split_keywords", "descriptive"}
        if v not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        return v


@mcp.tool(
    name="generate_topology_attractor_prompt",
    annotations={
        "title": "Generate Topology Attractor Prompt",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def generate_topology_attractor_prompt(params: AttractorPromptInput) -> str:
    """Generate image-generation-ready prompts from 5D topology coordinates.

    Layer 2: Deterministic vocabulary extraction (0 tokens).

    Translates abstract parameter coordinates into concrete visual vocabulary
    suitable for Stable Diffusion, ComfyUI, DALL-E, or Midjourney. Three
    output modes are available:

    - **composite**: Single prompt string combining keywords and geometric specs.
      Best for direct image generation.
    - **split_keywords**: Categorized keyword lists (visual type, specifications,
      parameter descriptors). Best for ComfyUI prompt engineering.
    - **descriptive**: Narrative paragraph prompt. Best for DALL-E / Midjourney.

    Coordinates can be provided directly, or derived from a canonical state name.

    Args:
        params (AttractorPromptInput): Validated input containing:
            - coordinates (Optional[Dict]): 5D coordinates
            - canonical_state (Optional[str]): State name for coordinate lookup
            - mode (str): Output mode
            - strength (float): Blending strength

    Returns:
        str: JSON with prompt content, visual type weights, and mode
    """
    # Resolve coordinates
    if params.coordinates:
        coords = {p: float(params.coordinates.get(p, 0.5)) for p in PARAMETER_NAMES}
    elif params.canonical_state:
        if params.canonical_state not in CANONICAL_STATES:
            return json.dumps({
                "error": f"Unknown canonical state '{params.canonical_state}'",
                "available": list(CANONICAL_STATES.keys()),
            }, indent=2)
        coords = CANONICAL_STATES[params.canonical_state]
    else:
        return json.dumps({
            "error": "Provide either 'coordinates' or 'canonical_state'",
        }, indent=2)

    result = extract_prompt_vocabulary(coords, params.mode, params.strength)
    return json.dumps(result, indent=2)


# --- generate_topology_rhythmic_sequence -----------------------------------

class RhythmicSequenceInput(BaseModel):
    """Input for generating a full rhythmic sequence."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    preset_name: str = Field(
        ..., description="Name of the rhythmic preset"
    )
    num_cycles: int = Field(
        default=1,
        description="Number of complete oscillation cycles to generate (1–10)",
        ge=1,
        le=10,
    )
    include_prompts: bool = Field(
        default=False,
        description="If True, generate attractor prompts for each step",
    )


@mcp.tool(
    name="generate_topology_rhythmic_sequence",
    annotations={
        "title": "Generate Topology Rhythmic Sequence",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def generate_topology_rhythmic_sequence(params: RhythmicSequenceInput) -> str:
    """Generate a complete rhythmic oscillation sequence from a preset.

    Layer 2: Deterministic computation (0 tokens).

    Produces one or more complete oscillation cycles between the preset's
    two canonical states. Optionally includes attractor prompts for each step.

    Args:
        params (RhythmicSequenceInput): Validated input containing:
            - preset_name (str): Preset to generate from
            - num_cycles (int): Number of cycles (1–10)
            - include_prompts (bool): Whether to add prompts per step

    Returns:
        str: JSON with full sequence data and optional prompts
    """
    try:
        base = generate_preset_trajectory(params.preset_name)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)

    # Tile trajectory for multiple cycles
    full_trajectory = base["trajectory"] * params.num_cycles

    steps_out = []
    for i, coords in enumerate(full_trajectory):
        step_data = {
            "step": i,
            "cycle": i // base["period"],
            "phase_in_cycle": (i % base["period"]) / base["period"],
            "coordinates": coords,
        }
        if params.include_prompts:
            prompt_result = extract_prompt_vocabulary(coords, "composite", 1.0)
            step_data["prompt"] = prompt_result.get("prompt", "")
        steps_out.append(step_data)

    return json.dumps({
        "preset_name": params.preset_name,
        "period": base["period"],
        "num_cycles": params.num_cycles,
        "total_steps": len(full_trajectory),
        "pattern": base["pattern"],
        "state_a": base["state_a"],
        "state_b": base["state_b"],
        "sequence": steps_out,
    }, indent=2)


# --- get_topology_domain_registry_config -----------------------------------

@mcp.tool(
    name="get_topology_domain_registry_config",
    annotations={
        "title": "Get Topology Domain Registry Config",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_topology_domain_registry_config() -> str:
    """Return Tier 4D integration configuration for compositional limit cycles.

    Layer 2: Pure lookup (0 tokens).

    Returns the domain signature for registering with aesthetic-dynamics-core
    multi-domain composition. Includes domain_id, parameter names, preset
    periods, and canonical state coordinates — everything needed for
    integrate_forced_limit_cycle_multi_domain.
    """
    config = get_domain_registry_config()
    return json.dumps(config, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
