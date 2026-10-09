"""M6.3, the recovery decision artifact (#41 addendum, agreed 2026-09-08).

WHAT THESE TESTS ARE ABOUT. The addendum's finding was that the recorded default
"every recovery mutation cites the recovery decision as its one authorization
source" had been ruled and never mechanized: the run's AuthorizationDecision is
one-per-run, its composer refuses a second human act beside a policy-authorized
run, and the request composer took no alternate source. This file pins the
mechanism that closed that gap, and one regression in particular (finding 1 of
the rev-1 adversarial review): a POLICY-AUTHORIZED run must be able to compose a
recovery decision, because the transaction composer's refusal is about the
one-per-run authorization and a recovery authorization is not one.

NO MODEL CALL ANYWHERE, in the code under test or here.
"""

from __future__ import annotations

import json

import pytest

from orchestrator import authorization_decision as ad
from orchestrator import recovery_decision as rd

CID = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
DIGEST = "a" * 64
OTHER_DIGEST = "b" * 64


def request(**overrides) -> rd.RecoveryDecisionRequest:
    fields = {
        "correlation_id": CID,
        "sequence": 2,
        "decided_at": "2026-09-08T10:00:00Z",
        "decided_by": "robert",
        "disposition_ref": f"{CID}.disposition-2.json",
        "plan_digest": DIGEST,
        "execution_mode": "simulation",
        "strategy_id": "rpm-rollback-verified-v1",
        "wave_number": 1,
        "hostname": "web-prod-01",
        "prior_step_idempotency_key": "c" * 64,
    }
    fields.update(overrides)
    return rd.RecoveryDecisionRequest(**fields)


# --- naming and identity ---------------------------------------------------------


def test_the_artifact_is_named_per_act_not_per_run() -> None:
    """IDENTITY PER-ACT is the one structural difference from the transaction
    decision, and it is deliberate: a run can be halted, recovered, halted again
    and recovered again, and each act is its own record."""
    assert rd.artifact_name(CID, 2) == f"{CID}.recovery-decision-2.json"
    assert rd.artifact_name(CID, 5) != rd.artifact_name(CID, 2)


def test_a_sequence_below_one_is_refused() -> None:
    with pytest.raises(ValueError):
        rd.artifact_suffix(0)


def test_the_artifact_composes_its_own_name(tmp_path) -> None:
    """A citation may not name a file the artifact does not claim to be: the
    name comes off the artifact ALONE, so the id and the file name cannot be
    made to disagree by a caller."""
    artifact, _ = rd.compose_recovery_decision(tmp_path, request())
    assert rd.artifact_name_of(artifact) == f"{CID}.recovery-decision-2.json"
    assert artifact.sequence == 2


# --- read-back-first -------------------------------------------------------------


def test_the_composer_writes_once_and_reuses_on_reprocessing(tmp_path) -> None:
    """A tick that composed a decision and died before recording its line
    re-processes the same disposition; minting a second decision id for one
    human act would put two authorizations on one act's record."""
    first, fresh = rd.compose_recovery_decision(tmp_path, request())
    assert fresh is True
    second, again = rd.compose_recovery_decision(tmp_path, request())
    assert again is False
    assert second.decision_id == first.decision_id
    assert second.model_dump() == first.model_dump()


def test_a_second_act_under_the_same_sequence_with_other_bytes_raises(tmp_path) -> None:
    """Same path, different content: two records disagreeing about what one act
    authorized. No code path resolves that."""
    rd.compose_recovery_decision(tmp_path, request())
    with pytest.raises(rd.RecoveryDecisionConflictError):
        rd.compose_recovery_decision(tmp_path, request(plan_digest=OTHER_DIGEST))
    with pytest.raises(rd.RecoveryDecisionConflictError):
        rd.compose_recovery_decision(
            tmp_path, request(disposition_ref=f"{CID}.disposition-9.json")
        )


def test_persist_refuses_to_overwrite_different_bytes(tmp_path) -> None:
    artifact, _ = rd.compose_recovery_decision(tmp_path, request())
    moved = artifact.model_copy(update={"hostname": "web-prod-02"})
    with pytest.raises(rd.RecoveryDecisionConflictError):
        rd.persist(tmp_path, moved)


def test_persist_is_idempotent_for_identical_bytes(tmp_path) -> None:
    artifact, _ = rd.compose_recovery_decision(tmp_path, request())
    assert rd.persist(tmp_path, artifact) is False


def test_a_corrupt_artifact_raises_rather_than_reading_as_absent(tmp_path) -> None:
    """A decision that will not parse is not an absent decision: treating it as
    one would let a second be composed beside a first nobody could read."""
    rd.artifact_path(tmp_path, CID, 2).write_text("{ not json", encoding="utf-8")
    with pytest.raises(Exception):
        rd.load(tmp_path, CID, 2)


def test_two_acts_on_one_run_are_two_artifacts(tmp_path) -> None:
    first, _ = rd.compose_recovery_decision(tmp_path, request(sequence=2))
    second, _ = rd.compose_recovery_decision(tmp_path, request(sequence=4))
    assert first.decision_id != second.decision_id
    assert rd.load(tmp_path, CID, 2) == first
    assert rd.load(tmp_path, CID, 4) == second


# --- the finding-1 regression ----------------------------------------------------


def _policy_authorized(runs, correlation_id: str = CID) -> None:
    """A run whose ONE authorization decision is a STANDING POLICY one. This is
    the shape `compose_transaction_decision` refuses to compose a second human
    act beside, and the shape the recovery decision must be composable for."""
    ad.persist(
        runs,
        ad.AuthorizationDecision(
            schema_version=1,
            decision_id="01ARZ3NDEKTSV4RRFFQ69G5FB0",
            correlation_id=correlation_id,
            decided_at="2026-09-01T09:00:00Z",
            disposition=ad.AuthorizationDisposition.AUTHORIZED,
            wave_ids=[1],
            plan_ref=f"{correlation_id}.waveplan-verified.round1.json",
            plan_digest=DIGEST,
            execution_mode="simulation",
            expires_at="2026-09-30T09:00:00Z",
            source_interface="orchestrator.authorization_gateway",
            policy_source=ad.PolicySource(
                policy_id="pol-1",
                matrix_id="mtx-1",
                register_id="reg-1",
                class_id="cls-1",
                grant_ids=["grant-1"],
                actor="change-authority",
            ),
        ),
    )


def test_a_policy_authorized_run_composes_a_recovery_decision_without_raising(
    tmp_path,
) -> None:
    """FINDING 1 OF THE REV-1 REVIEW, pinned as a regression.

    `compose_transaction_decision` raises AuthorizationDecisionConflictError
    against a policy-authorized run, because a human act cannot compose a SECOND
    one-per-run authorization beside a standing one. If the recovery
    authorization had been mechanized as a widening of that artifact, every
    policy-authorized run in the build would have had no recovery exit at all.
    It is its own artifact kind precisely so this passes."""
    _policy_authorized(tmp_path)
    # The transaction arm still refuses, which is what makes this test measure
    # something rather than merely pass.
    with pytest.raises(ad.AuthorizationDecisionConflictError):
        ad.compose_transaction_decision(
            tmp_path,
            ad.TransactionDecisionRequest(
                correlation_id=CID,
                decided_at="2026-09-08T10:00:00Z",
                actor="robert",
                disposition_ref=f"{CID}.disposition-2.json",
                approved=True,
                wave_ids=(1,),
                plan_ref=f"{CID}.waveplan-verified.round1.json",
                plan_digest=DIGEST,
                execution_mode="simulation",
                expiry_days=7,
                conditions=(),
                source_interface="web.resolutions",
            ),
        )

    artifact, fresh = rd.compose_recovery_decision(tmp_path, request())
    assert fresh is True
    assert artifact.disposition == rd.AUTHORIZE_RECOVERY


def test_composing_a_recovery_decision_never_touches_the_runs_own_decision(
    tmp_path,
) -> None:
    """The addendum's rule, measured on the bytes: the run's AuthorizationDecision
    is never read for a write decision, never re-composed, and never changed."""
    _policy_authorized(tmp_path)
    path = ad.artifact_path(tmp_path, CID)
    before = path.read_text(encoding="utf-8")

    rd.compose_recovery_decision(tmp_path, request())

    assert path.read_text(encoding="utf-8") == before


# --- the model's own refusals ----------------------------------------------------


def test_the_disposition_literal_admits_only_the_authorizing_value() -> None:
    """An artifact recording a CANCEL or a DEFER as a recovery authorization
    would be a record of an act nobody performed."""
    payload = json.loads(
        rd.RecoveryDecision(
            schema_version=1,
            correlation_id=CID,
            sequence=2,
            decision_id="01ARZ3NDEKTSV4RRFFQ69G5FB1",
            decided_by="robert",
            decided_at="2026-09-08T10:00:00Z",
            disposition=rd.AUTHORIZE_RECOVERY,
            plan_digest=DIGEST,
            execution_mode="simulation",
            strategy_id="rpm-rollback-verified-v1",
            wave_number=1,
            hostname="web-prod-01",
            prior_step_idempotency_key="c" * 64,
            disposition_ref=f"{CID}.disposition-2.json",
        ).model_dump_json()
    )
    payload["disposition"] = "cancel"
    with pytest.raises(Exception):
        rd.RecoveryDecision.model_validate(payload)


def test_the_model_carries_no_conditions_field(tmp_path) -> None:
    """The transaction approver's conditions scope the PATCH approval. A
    recovery authorization is a different act about a different mutation, and
    there is deliberately no field on which one person's caveats could be
    presented as another's."""
    assert "conditions" not in rd.RecoveryDecision.model_fields
    artifact, _ = rd.compose_recovery_decision(tmp_path, request())
    assert "conditions" not in json.loads(artifact.model_dump_json())


def test_a_wave_number_below_one_is_unrepresentable() -> None:
    with pytest.raises(Exception):
        request(wave_number=0)
        rd.RecoveryDecision(
            schema_version=1,
            correlation_id=CID,
            sequence=1,
            decision_id="01ARZ3NDEKTSV4RRFFQ69G5FB2",
            decided_by="robert",
            decided_at="2026-09-08T10:00:00Z",
            disposition=rd.AUTHORIZE_RECOVERY,
            plan_digest=DIGEST,
            execution_mode="simulation",
            strategy_id="rpm-rollback-verified-v1",
            wave_number=0,
            hostname="web-prod-01",
            prior_step_idempotency_key="c" * 64,
            disposition_ref=f"{CID}.disposition-1.json",
        )


def test_the_line_facts_name_the_artifact_the_phase_must_find(tmp_path) -> None:
    """The phase re-enters on the `recovery_authorized` line and has to find the
    decision it is executing under. Guessing which sequence authorized it would
    be a guess about which authorization a mutation rides."""
    artifact, _ = rd.compose_recovery_decision(tmp_path, request())
    facts = rd.decision_line_facts(artifact)
    assert facts[rd.RECOVERY_DECISION_ID_KEY] == artifact.decision_id
    assert facts[rd.RECOVERY_DECISION_SEQUENCE_KEY] == 2
    assert (
        rd.load(tmp_path, CID, facts[rd.RECOVERY_DECISION_SEQUENCE_KEY]) == artifact
    )
    assert facts[rd.RECOVERY_DECISION_REF_KEY] == rd.artifact_name_of(artifact)
