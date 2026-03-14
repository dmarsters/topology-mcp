"""
Layer 2: Deterministic computation for the topology domain.

All operations are 0 tokens — pure math (NumPy), no LLM calls.
Provides trajectory interpolation, preset oscillation generation,
and coordinate-to-prompt vocabulary extraction.
"""

import math
from typing import Dict, List, Optional, Tuple, Any

from .taxonomy import (
    PARAMETER_NAMES,
    CANONICAL_STATES,
    VISUAL_TYPES,
    PRESETS,
)


# ---------------------------------------------------------------------------
# Trajectory interpolation (Phase 1A)
# ---------------------------------------------------------------------------

def cosine_interpolate(
    state_a: Dict[str, float],
    state_b: Dict[str, float],
    steps: int,
) -> List[Dict[str, float]]:
    """Cosine ease-in-out interpolation between two 5D states.

    Returns `steps` points forming a smooth trajectory from state_a to state_b.
    Each point is a dict of parameter_name -> value in [0, 1].
    """
    trajectory: List[Dict[str, float]] = []
    for i in range(steps):
        t = i / max(steps - 1, 1)
        # cosine ease: 0→1 with smooth acceleration/deceleration
        blend = 0.5 * (1.0 - math.cos(math.pi * t))
        point = {}
        for p in PARAMETER_NAMES:
            a = state_a[p]
            b = state_b[p]
            point[p] = a + (b - a) * blend
        trajectory.append(point)
    return trajectory


def compute_trajectory(
    state_a_name: str,
    state_b_name: str,
    steps: int = 10,
) -> Dict[str, Any]:
    """Compute interpolation trajectory between two canonical states.

    Args:
        state_a_name: Starting canonical state name.
        state_b_name: Target canonical state name.
        steps: Number of interpolation steps (2–100).

    Returns:
        Dict with state_a, state_b, steps, and trajectory list.

    Raises:
        ValueError: If state names not found or steps out of range.
    """
    if state_a_name not in CANONICAL_STATES:
        raise ValueError(
            f"Unknown canonical state '{state_a_name}'. "
            f"Available: {list(CANONICAL_STATES.keys())}"
        )
    if state_b_name not in CANONICAL_STATES:
        raise ValueError(
            f"Unknown canonical state '{state_b_name}'. "
            f"Available: {list(CANONICAL_STATES.keys())}"
        )
    steps = max(2, min(100, steps))

    sa = CANONICAL_STATES[state_a_name]
    sb = CANONICAL_STATES[state_b_name]
    traj = cosine_interpolate(sa, sb, steps)

    return {
        "state_a": state_a_name,
        "state_b": state_b_name,
        "steps": steps,
        "trajectory": traj,
    }


# ---------------------------------------------------------------------------
# Preset oscillation generation (Phase 2.6)
# ---------------------------------------------------------------------------

def _generate_oscillation(
    state_a: Dict[str, float],
    state_b: Dict[str, float],
    period: int,
    pattern: str,
) -> List[Dict[str, float]]:
    """Generate one full oscillation cycle between two states.

    Patterns:
        sinusoidal — smooth cosine-based oscillation
        triangular — linear ramp up then down
    """
    trajectory: List[Dict[str, float]] = []
    for i in range(period):
        t = i / period  # [0, 1) over one cycle

        if pattern == "sinusoidal":
            # full cosine cycle: starts at midpoint, goes to A, back through mid to B, returns
            blend = 0.5 * (1.0 - math.cos(2.0 * math.pi * t))
        elif pattern == "triangular":
            # linear ramp: 0→1 in first half, 1→0 in second half
            if t < 0.5:
                blend = 2.0 * t
            else:
                blend = 2.0 * (1.0 - t)
        else:
            blend = 0.5  # fallback: midpoint

        point = {}
        for p in PARAMETER_NAMES:
            a = state_a[p]
            b = state_b[p]
            point[p] = a + (b - a) * blend
        trajectory.append(point)
    return trajectory


def generate_preset_trajectory(preset_name: str) -> Dict[str, Any]:
    """Generate the full oscillation trajectory for a named preset.

    Returns:
        Dict with preset metadata and trajectory list.
    """
    if preset_name not in PRESETS:
        raise ValueError(
            f"Unknown preset '{preset_name}'. Available: {list(PRESETS.keys())}"
        )

    preset = PRESETS[preset_name]
    sa = CANONICAL_STATES[preset["state_a"]]
    sb = CANONICAL_STATES[preset["state_b"]]

    traj = _generate_oscillation(sa, sb, preset["period"], preset["pattern"])

    return {
        "preset_name": preset_name,
        "period": preset["period"],
        "pattern": preset["pattern"],
        "state_a": preset["state_a"],
        "state_b": preset["state_b"],
        "description": preset["description"],
        "trajectory": traj,
    }


def apply_preset(preset_name: str, step: int) -> Dict[str, Any]:
    """Get the coordinates at a specific step within a preset cycle.

    Args:
        preset_name: Name of the preset.
        step: Step index (will be wrapped modulo period).

    Returns:
        Dict with step, period, phase, and coordinates.
    """
    result = generate_preset_trajectory(preset_name)
    period = result["period"]
    idx = step % period
    coords = result["trajectory"][idx]

    return {
        "preset_name": preset_name,
        "step": idx,
        "period": period,
        "phase": idx / period,
        "coordinates": coords,
    }


# ---------------------------------------------------------------------------
# Coordinate → prompt vocabulary (Phase 2.7)
# ---------------------------------------------------------------------------

def _distance_to_visual_type(
    coords: Dict[str, float],
    vt_coords: Dict[str, float],
) -> float:
    """Euclidean distance in 5D parameter space."""
    return math.sqrt(
        sum((coords.get(p, 0.5) - vt_coords.get(p, 0.5)) ** 2 for p in PARAMETER_NAMES)
    )


def _softmax_weights(
    distances: List[float],
    temperature: float = 0.3,
) -> List[float]:
    """Softmax over negative distances (closer = higher weight)."""
    neg_d = [-d / temperature for d in distances]
    max_nd = max(neg_d)
    exps = [math.exp(v - max_nd) for v in neg_d]
    total = sum(exps)
    return [e / total for e in exps]


def extract_prompt_vocabulary(
    coordinates: Dict[str, float],
    mode: str = "composite",
    strength: float = 1.0,
) -> Dict[str, Any]:
    """Extract image-generation vocabulary from 5D topology coordinates.

    Modes:
        composite    — single blended prompt string
        split_keywords — categorized keyword lists by visual type
        descriptive  — narrative paragraph prompt

    Args:
        coordinates: Dict of parameter_name -> value in [0,1].
        mode: Output mode.
        strength: Blending strength 0–1 (lower = more neutral vocabulary).

    Returns:
        Dict with mode, visual_type_weights, and prompt content.
    """
    # Compute distances and softmax weights
    vt_names = list(VISUAL_TYPES.keys())
    distances = [
        _distance_to_visual_type(coordinates, VISUAL_TYPES[vt]["coordinates"])
        for vt in vt_names
    ]
    weights = _softmax_weights(distances)

    # Identify dominant and secondary types
    ranked = sorted(zip(vt_names, weights), key=lambda x: -x[1])
    dominant_name, dominant_weight = ranked[0]
    secondary_name, secondary_weight = ranked[1] if len(ranked) > 1 else (None, 0)

    # Collect keywords weighted by strength
    if mode == "split_keywords":
        keyword_map = {}
        for vt_name, w in ranked:
            if w * strength > 0.05:  # threshold
                keyword_map[vt_name] = {
                    "weight": round(w, 4),
                    "keywords": VISUAL_TYPES[vt_name]["keywords"],
                }
        return {
            "mode": "split_keywords",
            "coordinates": coordinates,
            "visual_type_weights": {n: round(w, 4) for n, w in ranked},
            "keyword_map": keyword_map,
        }

    # Build blended keyword list
    blended_keywords: List[str] = []
    for vt_name, w in ranked:
        if w * strength > 0.05:
            n_pick = max(1, int(len(VISUAL_TYPES[vt_name]["keywords"]) * w * strength))
            blended_keywords.extend(VISUAL_TYPES[vt_name]["keywords"][:n_pick])

    # Parameter descriptors
    param_descriptors = _parameter_descriptors(coordinates)

    if mode == "descriptive":
        # Narrative paragraph
        desc_parts = [
            f"A topological form dominated by {dominant_name.replace('_', ' ')} character",
            f"({dominant_weight:.0%} affinity).",
        ]
        if secondary_name and secondary_weight > 0.15:
            desc_parts.append(
                f"Secondary influence from {secondary_name.replace('_', ' ')} "
                f"({secondary_weight:.0%})."
            )
        desc_parts.append(f"Parameters: {param_descriptors}.")
        desc_parts.append("Keywords: " + ", ".join(blended_keywords[:6]) + ".")

        return {
            "mode": "descriptive",
            "coordinates": coordinates,
            "visual_type_weights": {n: round(w, 4) for n, w in ranked},
            "prompt": " ".join(desc_parts),
        }

    # Default: composite
    prompt_parts = blended_keywords[:8]
    prompt_parts.append(param_descriptors)
    return {
        "mode": "composite",
        "coordinates": coordinates,
        "visual_type_weights": {n: round(w, 4) for n, w in ranked},
        "prompt": ", ".join(prompt_parts),
    }


def _parameter_descriptors(coords: Dict[str, float]) -> str:
    """Human-readable descriptors for parameter values."""
    descriptors = []
    mapping = {
        "genus_complexity": [
            (0.3, "low genus"),
            (0.6, "moderate genus"),
            (1.0, "high genus"),
        ],
        "curvature_uniformity": [
            (0.3, "varied curvature"),
            (0.6, "mixed curvature"),
            (1.0, "uniform curvature"),
        ],
        "boundary_definition": [
            (0.3, "open boundary"),
            (0.6, "partial boundary"),
            (1.0, "sharp boundary"),
        ],
        "orientability_degree": [
            (0.3, "non-orientable"),
            (0.6, "weakly orientable"),
            (1.0, "fully orientable"),
        ],
        "connectivity_density": [
            (0.3, "simple connectivity"),
            (0.6, "moderate connectivity"),
            (1.0, "dense connectivity"),
        ],
    }
    for param in PARAMETER_NAMES:
        val = coords.get(param, 0.5)
        for threshold, label in mapping.get(param, []):
            if val <= threshold:
                descriptors.append(label)
                break
    return ", ".join(descriptors)


# ---------------------------------------------------------------------------
# Nearest canonical state lookup
# ---------------------------------------------------------------------------

def find_nearest_canonical(
    coordinates: Dict[str, float],
) -> Tuple[str, float, Dict[str, float]]:
    """Find the nearest canonical state to arbitrary coordinates.

    Returns:
        Tuple of (state_name, distance, state_coordinates).
    """
    best_name = ""
    best_dist = float("inf")
    best_coords: Dict[str, float] = {}

    for name, state_coords in CANONICAL_STATES.items():
        d = _distance_to_visual_type(coordinates, state_coords)
        if d < best_dist:
            best_name = name
            best_dist = d
            best_coords = state_coords

    return best_name, best_dist, best_coords


# ---------------------------------------------------------------------------
# Domain registry config (Tier 4D compatibility)
# ---------------------------------------------------------------------------

def get_domain_registry_config() -> Dict[str, Any]:
    """Return Tier 4D integration configuration for multi-domain composition.

    Returns domain_id, parameter names, preset periods, and canonical
    state coordinates — everything needed for
    integrate_forced_limit_cycle_multi_domain.
    """
    preset_configs = {}
    for pname, pdata in PRESETS.items():
        result = generate_preset_trajectory(pname)
        preset_configs[pname] = {
            "period": pdata["period"],
            "pattern": pdata["pattern"],
            "state_a": pdata["state_a"],
            "state_b": pdata["state_b"],
            "trajectory": result["trajectory"],
        }

    return {
        "domain_id": "topology",
        "display_name": "Mathematical Topology",
        "mcp_server": "topology_mcp",
        "parameter_names": PARAMETER_NAMES,
        "parameter_count": len(PARAMETER_NAMES),
        "canonical_states": CANONICAL_STATES,
        "presets": preset_configs,
        "all_periods": sorted(set(p["period"] for p in PRESETS.values())),
        "visual_types": list(VISUAL_TYPES.keys()),
        "tier_4d_compatible": True,
    }
