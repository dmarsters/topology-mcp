"""
Layer 1: Pure taxonomy data for the topology domain.

All lookups are 0 tokens — no computation, no LLM calls.
Maps mathematical topology concepts (surfaces, manifolds, invariants)
to a 5D aesthetic parameter space in [0, 1]^5.

5D Parameter Space:
    genus_complexity      — topological complexity: 0 = sphere, 1 = high-genus surface
    curvature_uniformity  — how uniform Gaussian curvature is distributed across surface
    boundary_definition   — clarity/presence of manifold boundaries (0 = open/unbounded, 1 = sharply bounded)
    orientability_degree  — orientable (1.0) vs non-orientable (0.0)
    connectivity_density  — fundamental group complexity / path richness
"""

from typing import Dict, List, Any

# ---------------------------------------------------------------------------
# 5D parameter names (order matters for coordinate vectors)
# ---------------------------------------------------------------------------
PARAMETER_NAMES: List[str] = [
    "genus_complexity",
    "curvature_uniformity",
    "boundary_definition",
    "orientability_degree",
    "connectivity_density",
]

# ---------------------------------------------------------------------------
# Canonical states — named topological surfaces mapped to 5D coordinates
# ---------------------------------------------------------------------------
CANONICAL_STATES: Dict[str, Dict[str, float]] = {
    "sphere_purity": {
        "genus_complexity": 0.05,
        "curvature_uniformity": 0.95,
        "boundary_definition": 0.90,
        "orientability_degree": 1.00,
        "connectivity_density": 0.10,
    },
    "torus_circulation": {
        "genus_complexity": 0.35,
        "curvature_uniformity": 0.55,
        "boundary_definition": 0.85,
        "orientability_degree": 1.00,
        "connectivity_density": 0.45,
    },
    "mobius_twist": {
        "genus_complexity": 0.20,
        "curvature_uniformity": 0.40,
        "boundary_definition": 0.30,
        "orientability_degree": 0.10,
        "connectivity_density": 0.35,
    },
    "klein_paradox": {
        "genus_complexity": 0.40,
        "curvature_uniformity": 0.30,
        "boundary_definition": 0.15,
        "orientability_degree": 0.05,
        "connectivity_density": 0.55,
    },
    "projective_duality": {
        "genus_complexity": 0.30,
        "curvature_uniformity": 0.60,
        "boundary_definition": 0.50,
        "orientability_degree": 0.15,
        "connectivity_density": 0.40,
    },
    "genus3_labyrinth": {
        "genus_complexity": 0.85,
        "curvature_uniformity": 0.25,
        "boundary_definition": 0.75,
        "orientability_degree": 0.90,
        "connectivity_density": 0.90,
    },
    "hyperbolic_expanse": {
        "genus_complexity": 0.60,
        "curvature_uniformity": 0.70,
        "boundary_definition": 0.20,
        "orientability_degree": 0.85,
        "connectivity_density": 0.75,
    },
    "minimal_tension": {
        "genus_complexity": 0.25,
        "curvature_uniformity": 0.80,
        "boundary_definition": 0.45,
        "orientability_degree": 0.95,
        "connectivity_density": 0.30,
    },
    "trefoil_entangle": {
        "genus_complexity": 0.50,
        "curvature_uniformity": 0.35,
        "boundary_definition": 0.60,
        "orientability_degree": 0.80,
        "connectivity_density": 0.85,
    },
    "surface_revolution": {
        "genus_complexity": 0.15,
        "curvature_uniformity": 0.85,
        "boundary_definition": 0.70,
        "orientability_degree": 1.00,
        "connectivity_density": 0.20,
    },
    "crosscap_fold": {
        "genus_complexity": 0.45,
        "curvature_uniformity": 0.20,
        "boundary_definition": 0.25,
        "orientability_degree": 0.05,
        "connectivity_density": 0.60,
    },
}

# ---------------------------------------------------------------------------
# Visual types — regions of the 5D space with image-generation keywords
# ---------------------------------------------------------------------------
VISUAL_TYPES: Dict[str, Dict[str, Any]] = {
    "smooth_manifold": {
        "coordinates": {
            "genus_complexity": 0.10,
            "curvature_uniformity": 0.90,
            "boundary_definition": 0.85,
            "orientability_degree": 1.00,
            "connectivity_density": 0.15,
        },
        "keywords": [
            "clean continuous surface with uniform curvature",
            "smooth mathematical manifold rendered in soft light",
            "minimal genus form with gentle highlights on curved topology",
            "sphere-like translucent surface with subsurface scattering",
            "elegant closed manifold floating against dark void",
            "polished topological primitive with specular reflections",
        ],
    },
    "twisted_immersion": {
        "coordinates": {
            "genus_complexity": 0.35,
            "curvature_uniformity": 0.25,
            "boundary_definition": 0.20,
            "orientability_degree": 0.08,
            "connectivity_density": 0.50,
        },
        "keywords": [
            "self-intersecting non-orientable surface with iridescent edge",
            "Möbius-like twisted band fading through impossible geometry",
            "Klein bottle immersion with glass-refraction rendering",
            "paradoxical surface folding through itself in cool blue-violet",
            "cross-cap singularity point radiating structural tension lines",
            "non-orientable manifold with chromatic aberration at self-crossing",
        ],
    },
    "porous_genus": {
        "coordinates": {
            "genus_complexity": 0.80,
            "curvature_uniformity": 0.30,
            "boundary_definition": 0.70,
            "orientability_degree": 0.85,
            "connectivity_density": 0.85,
        },
        "keywords": [
            "high-genus surface with multiple tunnels and handles",
            "organic porous topology resembling coral or bone structure",
            "multiply-connected manifold with light passing through holes",
            "labyrinthine surface with saddle points at each handle junction",
            "dense topological network with negative curvature pockets",
            "Swiss-cheese manifold casting complex shadow lattice",
        ],
    },
    "crystalline_boundary": {
        "coordinates": {
            "genus_complexity": 0.25,
            "curvature_uniformity": 0.50,
            "boundary_definition": 0.95,
            "orientability_degree": 0.90,
            "connectivity_density": 0.40,
        },
        "keywords": [
            "sharp-edged manifold with clearly defined boundary curves",
            "crystalline topological surface with faceted edge geometry",
            "bounded manifold with glowing rim light along boundary",
            "precise geometric surface terminating at crisp boundary contour",
            "angular topology with prismatic refractions at boundary faces",
            "manifold-with-boundary rendered as cut gemstone cross-section",
        ],
    },
    "hyperbolic_tiling": {
        "coordinates": {
            "genus_complexity": 0.55,
            "curvature_uniformity": 0.75,
            "boundary_definition": 0.15,
            "orientability_degree": 0.80,
            "connectivity_density": 0.70,
        },
        "keywords": [
            "Poincaré disc tiling with recursively shrinking polygons",
            "hyperbolic plane tessellation in warm amber and deep indigo",
            "Escher-inspired hyperbolic pattern receding toward ideal boundary",
            "constant negative curvature surface with regular geodesic grid",
            "conformal disc model with infinite repetition toward rim",
            "hyperbolic manifold tiling with alternating luminance cells",
        ],
    },
    "knotted_filament": {
        "coordinates": {
            "genus_complexity": 0.45,
            "curvature_uniformity": 0.35,
            "boundary_definition": 0.55,
            "orientability_degree": 0.75,
            "connectivity_density": 0.90,
        },
        "keywords": [
            "trefoil knot rendered as thick luminous tube in 3-space",
            "topological knot with crossing-number shadows on ground plane",
            "interlocked torus knot with metallic surface and soft caustics",
            "mathematical knot diagram extruded into sculptural ribbon",
            "Seifert surface spanning a knot boundary with membrane tension",
            "braided filament tracing a closed path through ambient space",
        ],
    },
}

# ---------------------------------------------------------------------------
# Surface catalog — extended reference for Layer 1 list tools
# ---------------------------------------------------------------------------
SURFACES: Dict[str, Dict[str, Any]] = {
    "sphere": {
        "genus": 0,
        "euler_characteristic": 2,
        "orientable": True,
        "boundary": False,
        "curvature": "positive (constant)",
        "fundamental_group": "trivial",
        "canonical_state": "sphere_purity",
        "description": "The simplest closed surface. Zero genus, constant positive Gaussian curvature.",
    },
    "torus": {
        "genus": 1,
        "euler_characteristic": 0,
        "orientable": True,
        "boundary": False,
        "curvature": "mixed (positive outer, negative inner)",
        "fundamental_group": "Z × Z",
        "canonical_state": "torus_circulation",
        "description": "Genus-1 surface with one handle. Product of two circles.",
    },
    "mobius_strip": {
        "genus": 0,
        "euler_characteristic": 0,
        "orientable": False,
        "boundary": True,
        "curvature": "zero (flat embedding)",
        "fundamental_group": "Z",
        "canonical_state": "mobius_twist",
        "description": "Non-orientable surface with a single boundary component. One-sided.",
    },
    "klein_bottle": {
        "genus": 1,
        "euler_characteristic": 0,
        "orientable": False,
        "boundary": False,
        "curvature": "mixed (requires immersion in R³)",
        "fundamental_group": "Z ⋊ Z",
        "canonical_state": "klein_paradox",
        "description": "Non-orientable closed surface. Cannot be embedded in R³ without self-intersection.",
    },
    "real_projective_plane": {
        "genus": 1,
        "euler_characteristic": 1,
        "orientable": False,
        "boundary": False,
        "curvature": "positive (constant, as elliptic geometry)",
        "fundamental_group": "Z/2Z",
        "canonical_state": "projective_duality",
        "description": "Non-orientable surface obtained by identifying antipodal points of a sphere.",
    },
    "genus_3_surface": {
        "genus": 3,
        "euler_characteristic": -4,
        "orientable": True,
        "boundary": False,
        "curvature": "negative (hyperbolic metric)",
        "fundamental_group": "surface group π₁(Σ₃)",
        "canonical_state": "genus3_labyrinth",
        "description": "Orientable surface with three handles. Rich fundamental group structure.",
    },
    "hyperbolic_plane": {
        "genus": None,
        "euler_characteristic": None,
        "orientable": True,
        "boundary": False,
        "curvature": "negative (constant)",
        "fundamental_group": "trivial (simply connected)",
        "canonical_state": "hyperbolic_expanse",
        "description": "The unique simply connected surface of constant negative curvature.",
    },
    "catenoid": {
        "genus": 0,
        "euler_characteristic": 0,
        "orientable": True,
        "boundary": True,
        "curvature": "negative (minimal surface, zero mean curvature)",
        "fundamental_group": "Z",
        "canonical_state": "minimal_tension",
        "description": "Minimal surface of revolution. Zero mean curvature everywhere.",
    },
    "trefoil_knot_complement": {
        "genus": 1,
        "euler_characteristic": 0,
        "orientable": True,
        "boundary": True,
        "curvature": "hyperbolic (knot complement)",
        "fundamental_group": "braid group B₃",
        "canonical_state": "trefoil_entangle",
        "description": "The complement of a trefoil knot in S³. Rich topological structure.",
    },
    "surface_of_revolution": {
        "genus": 0,
        "euler_characteristic": 2,
        "orientable": True,
        "boundary": False,
        "curvature": "variable (depends on profile curve)",
        "fundamental_group": "trivial",
        "canonical_state": "surface_revolution",
        "description": "Generated by rotating a profile curve. Axial symmetry guarantees orientability.",
    },
    "cross_cap": {
        "genus": 1,
        "euler_characteristic": 1,
        "orientable": False,
        "boundary": False,
        "curvature": "singular at self-intersection",
        "fundamental_group": "Z/2Z",
        "canonical_state": "crosscap_fold",
        "description": "Immersion of the real projective plane in R³. Single point of self-intersection.",
    },
}

# ---------------------------------------------------------------------------
# Presets — Phase 2.6 rhythmic oscillation between canonical states
# Periods chosen for Tier 4D emergent attractor compatibility:
#   [14, 17, 19, 21, 26] — coprime-rich set for beat frequency diversity
# ---------------------------------------------------------------------------
PRESETS: Dict[str, Dict[str, Any]] = {
    "genus_ascent": {
        "period": 17,
        "pattern": "sinusoidal",
        "state_a": "sphere_purity",
        "state_b": "genus3_labyrinth",
        "description": "Smooth climb from genus-0 purity through increasing topological complexity.",
    },
    "orientation_flip": {
        "period": 14,
        "pattern": "triangular",
        "state_a": "torus_circulation",
        "state_b": "klein_paradox",
        "description": "Triangular oscillation between orientable torus and non-orientable Klein bottle.",
    },
    "curvature_tide": {
        "period": 21,
        "pattern": "sinusoidal",
        "state_a": "sphere_purity",
        "state_b": "hyperbolic_expanse",
        "description": "Sinusoidal wave between positive (spherical) and negative (hyperbolic) curvature.",
    },
    "boundary_pulse": {
        "period": 19,
        "pattern": "sinusoidal",
        "state_a": "mobius_twist",
        "state_b": "torus_circulation",
        "description": "Pulse between bounded non-orientable strip and closed orientable torus.",
    },
    "manifold_breathing": {
        "period": 26,
        "pattern": "triangular",
        "state_a": "projective_duality",
        "state_b": "genus3_labyrinth",
        "description": "Slow breathing between projective simplicity and genus-3 labyrinthine complexity.",
    },
}
