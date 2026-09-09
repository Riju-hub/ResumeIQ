import gc
from typing import Dict, List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

from backend.utils.file_utils import log_warning


def validate_skills_with_projects(
    skills: List[str],
    projects: List[Dict],
    experience_entries: List[Dict],
    embedder: SentenceTransformer,
    threshold: float = 0.6,
) -> Dict:
    if not skills:
        return {
            "validated_skills": [],
            "unvalidated_skills": [],
            "validation_percentage": 0.0,
            "skill_project_mapping": {},
            "validation_score": 0.0,
        }

    experience_text = " ".join(
        f"{e.get('job_title', '')} {e.get('company', '')} {e.get('description', '')}"
        for e in experience_entries
        if isinstance(e, dict)
    ).strip()

    targets: List[Tuple[str, str]] = []
    for proj in projects:
        if isinstance(proj, dict):
            title = proj.get("title", "Untitled Project")
            desc = proj.get("description", "")
            targets.append((title, f"{title} {desc}"))
    if experience_text:
        targets.append(("Experience Section", experience_text))

    validated_skills = []
    unvalidated_skills = []
    skill_project_mapping = {}

    skills_to_embed = []
    for skill in skills:
        s_lower = skill.lower()
        matched = [name for name, text in targets if s_lower in text.lower()]
        if matched:
            validated_skills.append(
                {"skill": skill, "projects": matched, "similarity": 1.0}
            )
            skill_project_mapping[skill] = matched
        else:
            skills_to_embed.append(skill)

    # Low-memory inference mode with small batches
    if skills_to_embed and targets:
        try:
            with torch.inference_mode():
                # Truncate text targets to 500 chars to avoid large tensor expansions
                target_texts = [t[1][:500] for t in targets]

                skill_vecs = embedder.encode(
                    skills_to_embed,
                    batch_size=8,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )
                target_vecs = embedder.encode(
                    target_texts,
                    batch_size=4,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )

                sim_matrix = np.dot(skill_vecs, target_vecs.T)

                for idx, skill in enumerate(skills_to_embed):
                    scores = sim_matrix[idx]
                    matched_names = []
                    max_sim = 0.0
                    for t_idx, score in enumerate(scores):
                        if score >= threshold:
                            matched_names.append(targets[t_idx][0])
                            max_sim = max(max_sim, float(score))

                    if matched_names:
                        validated_skills.append(
                            {
                                "skill": skill,
                                "projects": matched_names,
                                "similarity": max_sim,
                            }
                        )
                        skill_project_mapping[skill] = matched_names
                    else:
                        unvalidated_skills.append(skill)
                        skill_project_mapping[skill] = []

                del skill_vecs, target_vecs, sim_matrix
                gc.collect()

        except Exception as e:
            log_warning(
                f"Batch embedding validation failed: {e}", context="ats_scorer"
            )
            for skill in skills_to_embed:
                unvalidated_skills.append(skill)
                skill_project_mapping[skill] = []
    else:
        for skill in skills_to_embed:
            unvalidated_skills.append(skill)
            skill_project_mapping[skill] = []

    validation_percentage = len(validated_skills) / len(skills) if skills else 0.0
    validation_score = validation_percentage * 15.0

    return {
        "validated_skills": validated_skills,
        "unvalidated_skills": unvalidated_skills,
        "validation_percentage": validation_percentage,
        "skill_project_mapping": skill_project_mapping,
        "validation_score": validation_score,
    }