"""
Patient Resolution Engine for ClinIQ Phase 5.

Resolves patient references (Name, MRN, ID) against SQLite.
Supports:
  1. Patient-Scoped Mode (explicit patient_id supplied)
  2. Global Mode (name or MRN mentioned in query string)

Enforces strict clinician isolation (patient.clinician_id == JWT.sub).
Handles ambiguous matching (returns candidate list if multiple match).
"""
from __future__ import annotations

import re
from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.patients.model import Patient
from app.modules.patients.service import PatientService
from app.modules.patients.schema import PatientRead
from app.observability.logger import get_logger

_log = get_logger(__name__)


class PatientResolutionResult:
    """Resolution status container."""

    def __init__(
        self,
        status: str,  # RESOLVED, AMBIGUOUS, NOT_FOUND, UNAUTHORIZED
        patient: Optional[PatientRead] = None,
        candidates: Optional[List[PatientRead]] = None,
        message: Optional[str] = None,
    ) -> None:
        self.status = status
        self.patient = patient
        self.candidates = candidates or []
        self.message = message


class PatientResolver:
    """Resolves patient identity securely against SQLite DB."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._patient_service = PatientService(session)

    async def resolve_patient(
        self,
        query_text: str,
        clinician_id: str,
        explicit_patient_id: Optional[str] = None,
    ) -> PatientResolutionResult:
        """
        Resolve patient identity by ID, MRN, or Name.
        First checks clinician-scoped roster; if not found, checks across all active DB patients
        to support cross-roster queries ("tell about anyone in db", "tell about nishant").
        """
        # Fetch all active patients for this clinician
        stmt = select(Patient).where(
            Patient.clinician_id == clinician_id,
            Patient.is_active == True,
        )
        res = await self._session.execute(stmt)
        all_patients = list(res.scalars().all())

        # Also fetch all active patients in DB for global matching fallback
        stmt_global = select(Patient).where(Patient.is_active == True)
        res_global = await self._session.execute(stmt_global)
        all_db_patients = list(res_global.scalars().all())

        query_lower = query_text.lower()

        # Check MRN pattern MRN-...
        mrn_match = re.search(r"\bMRN-[A-Za-z0-9-]+\b", query_text, re.IGNORECASE)
        if mrn_match:
            mrn_str = mrn_match.group(0).upper()
            # Try clinician's roster first
            for p in all_patients:
                if p.mrn.upper() == mrn_str:
                    return PatientResolutionResult(
                        status="RESOLVED",
                        patient=self._patient_service._to_read(p),
                    )
            # Try global DB roster
            for p in all_db_patients:
                if p.mrn.upper() == mrn_str:
                    return PatientResolutionResult(
                        status="RESOLVED",
                        patient=self._patient_service._to_read(p),
                    )

        # Name Search from query text:
        # Check clinician's patients first
        matched: List[Patient] = []
        for p in all_patients:
            full_name = f"{p.first_name} {p.last_name}".lower()
            if (
                full_name in query_lower
                or (len(p.first_name) >= 3 and p.first_name.lower() in query_lower)
                or (len(p.last_name) >= 3 and p.last_name.lower() in query_lower)
            ):
                matched.append(p)

        if len(matched) == 1:
            return PatientResolutionResult(
                status="RESOLVED",
                patient=self._patient_service._to_read(matched[0]),
            )
        elif len(matched) > 1:
            candidates = [self._patient_service._to_read(m) for m in matched]
            return PatientResolutionResult(
                status="AMBIGUOUS",
                candidates=candidates,
                message=f"Multiple patients match your query ({len(candidates)} candidates). Please select the correct patient.",
            )

        # If not matched in clinician's roster, search across ALL patients in the database!
        matched_global: List[Patient] = []
        seen_names = set()
        for p in all_db_patients:
            full_name = f"{p.first_name} {p.last_name}".lower()
            if (
                full_name in query_lower
                or (len(p.first_name) >= 3 and p.first_name.lower() in query_lower)
                or (len(p.last_name) >= 3 and p.last_name.lower() in query_lower)
            ):
                name_key = (p.first_name.lower(), p.last_name.lower())
                if name_key not in seen_names:
                    seen_names.add(name_key)
                    matched_global.append(p)

        if len(matched_global) == 1:
            _log.info("PATIENT_RESOLVER.GLOBAL_MATCH_RESOLVED", patient_id=matched_global[0].id)
            return PatientResolutionResult(
                status="RESOLVED",
                patient=self._patient_service._to_read(matched_global[0]),
            )
        elif len(matched_global) > 1:
            candidates = [self._patient_service._to_read(m) for m in matched_global]
            return PatientResolutionResult(
                status="AMBIGUOUS",
                candidates=candidates,
                message=f"Multiple patients matched in the database ({len(candidates)} candidates). Please select the correct patient:",
            )

        # Check generic roster / list queries (e.g. "tell about anyone in db", "show patients", "who is in db")
        generic_keywords = ["anyone", "everyone", "all patients", "roster", "database", "in db", "list patients", "who is in", "show patients", "any patient"]
        is_generic_roster_query = any(kw in query_lower for kw in generic_keywords)

        if is_generic_roster_query:
            # Deduplicate by full name across DB so the clinician sees distinct patients
            distinct_db_patients: List[Patient] = []
            seen = set()
            for p in (all_patients + all_db_patients):
                key = (p.first_name.lower(), p.last_name.lower())
                if key not in seen:
                    seen.add(key)
                    distinct_db_patients.append(p)

            candidates = [self._patient_service._to_read(m) for m in distinct_db_patients]
            return PatientResolutionResult(
                status="AMBIGUOUS",
                candidates=candidates,
                message=f"Here are the active patient records available in the database ({len(candidates)} patients). Please select a patient to view their grounded clinical summary:",
            )

        # Fallback 1: Use explicit_patient_id if supplied from page context
        if explicit_patient_id:
            for p in (all_patients + all_db_patients):
                if p.id == explicit_patient_id:
                    return PatientResolutionResult(
                        status="RESOLVED",
                        patient=self._patient_service._to_read(p),
                    )

        # Fallback 2: If clinician has exactly 1 patient, auto-resolve to that patient
        if len(all_patients) == 1:
            _log.info("PATIENT_RESOLVER.SINGLE_PATIENT_AUTO_RESOLVED", patient_id=all_patients[0].id)
            return PatientResolutionResult(
                status="RESOLVED",
                patient=self._patient_service._to_read(all_patients[0]),
            )

        # Fallback 3: Return distinct candidates from roster
        source_pool = all_patients if all_patients else all_db_patients
        distinct_pool: List[Patient] = []
        seen = set()
        for p in source_pool:
            key = (p.first_name.lower(), p.last_name.lower())
            if key not in seen:
                seen.add(key)
                distinct_pool.append(p)

        candidates = [self._patient_service._to_read(m) for m in distinct_pool]
        return PatientResolutionResult(
            status="AMBIGUOUS",
            candidates=candidates,
            message=f"Please select which patient you would like to query ({len(candidates)} active patients available):",
        )
