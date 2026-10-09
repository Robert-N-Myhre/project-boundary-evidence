"""M2.10: the deterministic acquisition floor (ARCHITECTURE-CHANGES #31).

Three properties, kept apart on purpose.

DERIVATION is pure: which contract-named hosts the floor will fetch, and the two
deliberate exclusions (uppercase, and hyphenated prose with no digit) that keep
it from manufacturing targets out of English.

EXECUTION is the floor itself, run through the REAL gateway over real stores in
tmp_path with a scripted broker: two calls per target in order, a Source-of-Truth
absence that never suppresses the live-facts fetch, all-or-nothing against the
floor's own allowance, and a defect that halts with its record intact.

THE SEAM is what invoke() does with it: floor evidence in the FIRST data block,
labelled as orchestrator-acquired, floor positions ahead of every agent position,
and a reused proposal that runs no floor at all.

No reasoning model anywhere in this file: the scope agent is a scripted fake and
the classifier answers a fixed verdict, so the real screening path still runs.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

import pytest
import yaml

from orchestrator import (
    acquisition_floor,
    config,
    context_gateway,
    context_scope,
    netbox_adapter,
    scope_proposal,
)
from orchestrator.acquisition_floor import (
    FloorAcquisitionError,
    FloorBudgetInsufficientError,
    FloorTarget,
    derive_targets,
    run_floor,
)
from orchestrator.candidate_contract import (
    AcceptedIntakeContract,
    Confidence,
    PreparedContentProvenance,
    ValidatedField,
)
from orchestrator.context_gateway import GatewayBudget, SourceContext
from orchestrator.netbox_adapter import NetBoxAdapter
from orchestrator.stage_account import ExecutionMode, StageAccount

CID = "01ARZ3NDEKTSV4RRFFQ69G5FAV"


@pytest.fixture(autouse=True)
def _real_config():
    config._cached = None
    yield
    config._cached = None


@pytest.fixture
def cfg():
    return config.load_config()


# --- contract builder ---------------------------------------------------------


def _field(value):
    return ValidatedField(
        value=value,
        confidence=Confidence.HIGH,
        provenance=PreparedContentProvenance(
            source_type="prepared_content", quote="q", digest_ref="a" * 64
        ),
    )


def contract(**fields) -> AcceptedIntakeContract:
    return AcceptedIntakeContract(
        state="ACCEPTED",
        schema_version=1,
        correlation_id=CID,
        accepted_at="2026-08-10T00:00:00Z",
        digest_ref="a" * 64,
        validated_ref=f"{CID}.contract-validated.json",
        model_identity="qwen3-14b-q4_k_m",
        prompt_version="iua@abcdef012345",
        fields={name: _field(value) for name, value in fields.items()},
        gaps=[],
    )


# --- derivation ----------------------------------------------------------------


def test_a_single_named_host_is_one_target():
    targets = derive_targets(contract(configuration_item="web-prod-04"))
    assert targets == [FloorTarget(name="web-prod-04", source_field="configuration_item")]


def test_a_multi_host_conjunction_yields_both_hosts():
    # The corpus shape that proves configuration_item is free-form prose: intake
    # records the requester's phrase, not a normalized host list.
    targets = derive_targets(
        contract(configuration_item="web-prod-04 and app-mq-01")
    )
    assert [t.name for t in targets] == ["web-prod-04", "app-mq-01"]
    assert {t.source_field for t in targets} == {"configuration_item"}


@pytest.mark.parametrize(
    "value",
    [
        "Tier 2 hosts",
        "web servers",
        "all the database replicas",
        "read-only maintenance on the cache tier",
        "a well-known single-user box",
        "the DR pair",
    ],
)
def test_prose_without_an_estate_shaped_name_yields_nothing(value):
    # Group labels have no hyphenated token at all; hyphenated English has no
    # digit. Both must derive nothing, because a derived target the store has
    # never heard of refers the whole proposal under the strict absence rule.
    assert derive_targets(contract(configuration_item=value)) == []


def test_a_hostname_shaped_group_label_is_a_target():
    # Robert's ruling, 2026-08-10, and its named day-one cost: a group label
    # shaped like a hostname IS fetched, and its guaranteed absence refers. The
    # avoided failure is a requested host silently dropped from scope.
    targets = derive_targets(contract(configuration_item="web-fleet-tier3"))
    assert [t.name for t in targets] == ["web-fleet-tier3"]


@pytest.mark.parametrize("value", ["WEB-PROD-04", "Web-Prod-04", "web-PROD-04"])
def test_an_uppercase_token_is_never_a_target(value):
    # Deliberate: estate naming is lowercase, so a token carrying uppercase is
    # not a name this store holds, and fetching it would manufacture an absence
    # finding about something that was never a hostname.
    assert derive_targets(contract(configuration_item=value)) == []


def test_the_objective_is_scanned_after_the_configuration_item():
    targets = derive_targets(
        contract(
            configuration_item="web-prod-04",
            objective="Patch web-prod-04 and db-replica-02 before the window",
        )
    )
    # Dedupe keeps FIRST appearance, and the configuration item is scanned
    # first, so the repeated host is recorded against the field that named it
    # as the change's target.
    assert [(t.name, t.source_field) for t in targets] == [
        ("web-prod-04", "configuration_item"),
        ("db-replica-02", "objective"),
    ]


def test_only_the_two_named_fields_are_scanned():
    # A hostname in any other accepted-contract field is not a floor target:
    # the scan set is two fields, in code, and widening it is a reviewed change.
    assert derive_targets(contract(category="web-prod-04")) == []
    assert acquisition_floor.TARGET_SOURCE_FIELDS == (
        "configuration_item",
        "objective",
    )


def test_a_non_string_field_value_is_skipped_not_stringified():
    # planned_window is the structured shape that exists today. Serializing a
    # container and scanning the result would derive targets out of punctuation.
    targets = derive_targets(
        contract(planned_window={"start": "2026-08-11 22:00 UTC", "end": "x"})
    )
    assert targets == []


def test_an_absent_field_is_simply_not_scanned():
    assert derive_targets(contract()) == []


# --- a real gateway over real stores -------------------------------------------


class FakeTransport:
    """The scripted-broker idiom from test_tool_roster.py."""

    def __init__(self, responder):
        self._responder = responder
        self._pending: list[str] = []
        self.closed = False

    def send_line(self, line: str) -> None:
        answer = self._responder(json.loads(line))
        if answer is not None:
            self._pending.append(answer)

    def read_line(self) -> str:
        return self._pending.pop(0) if self._pending else ""

    def close(self) -> None:
        self.closed = True


def vm(name: str, *, description: str = "") -> dict[str, Any]:
    return {
        "id": 1,
        "name": name,
        "status": {"value": "active", "label": "Active"},
        "role": {"slug": "web-frontend", "name": "web-frontend"},
        "platform": {"slug": "rhel", "name": "RHEL"},
        "cluster": {"name": "web-c1"},
        "description": description,
        "custom_fields": {
            "sentinel_tier": 3,
            "sentinel_owner": "web-team",
            "sentinel_os_version": "9.4",
            "sentinel_last_verified": "2026-07-02",
            "sentinel_hold_reason": "",
            "sentinel_hold_authority": "",
            "sentinel_hold_expires": None,
            "sentinel_restricted": None,
        },
    }


def broker(estate, *, calls: list[dict] = None):
    """A name-filtering fake broker, so an exact-name lookup for a host the
    estate does not hold really does come back empty (the ghost specimen), and
    the gateway's own filter post-condition really runs.

    `estate` is a LIST of NetBox-shaped records, filtered on each record's own
    `name`: NetBox does not enforce unique virtual-machine names, so two records
    under one name has to be expressible here."""

    def responder(message):
        method = message.get("method")
        if method == "initialize":
            return json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "result": {
                        "protocolVersion": netbox_adapter.PROTOCOL_VERSION,
                        "capabilities": {},
                        "serverInfo": {"name": "netbox", "version": "3.4.2"},
                    },
                }
            )
        if method == "notifications/initialized":
            return None
        if method == "tools/call":
            arguments = message["params"]["arguments"]
            if calls is not None:
                calls.append(arguments)
            filters = arguments.get("filters") or {}
            name = filters.get("name")
            results = [
                record
                for record in estate
                if name is None or record["name"] == name
            ]
            payload = {
                "count": len(results),
                "next": None,
                "previous": None,
                "results": results,
            }
            return json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(payload)}],
                        "structuredContent": payload,
                        "isError": False,
                    },
                }
            )
        raise AssertionError(f"unscripted method {method!r}")

    return responder


def sources(tmp_path, *, estate=None, live_facts=(), broker_calls=None) -> SourceContext:
    corpus = tmp_path / "corpus"
    corpus.mkdir(exist_ok=True)
    index = corpus / "index.yaml"
    index.write_text(yaml.safe_dump({"documents": []}), encoding="utf-8")
    ledger = tmp_path / "patch-ledger.jsonl"
    ledger.write_text("", encoding="utf-8")
    live = tmp_path / "live-facts"
    live.mkdir(exist_ok=True)
    for hostname in live_facts:
        (live / f"{hostname}.yaml").write_text(
            yaml.safe_dump(
                {
                    "hostname": hostname,
                    "observed_at": "2026-08-09T06:00:00Z",
                    "origin": "aap-facts",
                    "os": {"name": "rhel", "version": "9.4"},
                }
            ),
            encoding="utf-8",
        )
    return SourceContext(
        netbox=NetBoxAdapter(
            transport_factory=lambda: FakeTransport(
                broker(list(estate or ()), calls=broker_calls)
            )
        ),
        live_facts_dir=live,
        patch_ledger_path=ledger,
        corpus_dir=corpus,
        corpus_index_path=index,
    )


def _clean_classifier(role, prompt, *, config):
    assert role == "classifier"
    return "CLEAN"


def _floor(tmp_path, cfg, targets, *, budget=None, src=None, screenings=None, **kwargs):
    return run_floor(
        correlation_id=CID,
        targets=targets,
        budget=budget or GatewayBudget(agent_total=8, floor_total=8),
        config=cfg,
        screenings_dir=screenings or (tmp_path / "screenings"),
        sources=src if src is not None else sources(tmp_path),
        call_model=_clean_classifier,
        **kwargs,
    )


# --- execution ------------------------------------------------------------------


def test_each_target_costs_one_sot_call_then_one_live_facts_call(tmp_path, cfg):
    budget = GatewayBudget(agent_total=8, floor_total=8)
    result = _floor(
        tmp_path,
        cfg,
        [
            FloorTarget("web-prod-04", "configuration_item"),
            FloorTarget("app-mq-01", "objective"),
        ],
        budget=budget,
        src=sources(
            tmp_path,
            estate=[vm("web-prod-04"), vm("app-mq-01")],
            live_facts=("web-prod-04", "app-mq-01"),
        ),
    )

    assert [(c.position, c.tool) for c in result.executed] == [
        (1, context_gateway.SOT_HOST_BY_NAME_TOOL),
        (2, context_gateway.LIVE_FACTS_TOOL),
        (3, context_gateway.SOT_HOST_BY_NAME_TOOL),
        (4, context_gateway.LIVE_FACTS_TOOL),
    ]
    assert all(c.acquisition_origin == "floor" for c in result.executed)
    # Charged to the floor lane only: the agent's loop is untouched by the floor.
    assert (budget.floor_used, budget.agent_used) == (4, 0)
    assert budget.agent_remaining == 8


def test_the_arguments_are_composed_in_code_from_the_target_name(tmp_path, cfg):
    calls: list[dict] = []
    result = _floor(
        tmp_path,
        cfg,
        [FloorTarget("web-prod-04", "configuration_item")],
        src=sources(
            tmp_path,
            estate=[vm("web-prod-04")],
            live_facts=("web-prod-04",),
            broker_calls=calls,
        ),
    )
    assert [c.arguments for c in result.executed] == [
        {"hostname": "web-prod-04"},
        {"hostname": "web-prod-04"},
    ]
    # And the estate boundary is still injected by the gateway, not by the floor.
    assert all(
        call["filters"]["tag"] == netbox_adapter.ESTATE_TAG for call in calls
    )


def test_a_source_of_truth_absence_never_suppresses_the_live_facts_call(tmp_path, cfg):
    # #31's floor scope, and the F9 arm: SoT-absent does not skip the live-facts
    # fetch, and BOTH absences are recorded. A host the governed store has never
    # heard of may still be reporting facts, which is itself worth knowing.
    result = _floor(
        tmp_path,
        cfg,
        [FloorTarget("ghost-host-99", "configuration_item")],
        src=sources(tmp_path, estate=[], live_facts=("ghost-host-99",)),
    )
    assert [(c.tool, c.legal_empty) for c in result.executed] == [
        (context_gateway.SOT_HOST_BY_NAME_TOOL, True),
        (context_gateway.LIVE_FACTS_TOOL, False),
    ]
    assert result.absent_targets == ("ghost-host-99",)
    assert result.summary.targets[0].sot_absent is True


def test_both_stores_empty_is_two_recorded_absences(tmp_path, cfg):
    result = _floor(
        tmp_path,
        cfg,
        [FloorTarget("ghost-host-99", "configuration_item")],
        src=sources(tmp_path, estate=[]),
    )
    assert [c.legal_empty for c in result.executed] == [True, True]
    assert result.absent_targets == ("ghost-host-99",)


def test_zero_targets_is_legal_and_costs_nothing(tmp_path, cfg):
    budget = GatewayBudget(agent_total=8, floor_total=8)
    result = _floor(tmp_path, cfg, [], budget=budget)
    assert result.executed == () and result.rounds == () and result.positions == ()
    assert result.stage_accounts == ()
    assert budget.used == 0
    # The summary is written anyway: "the floor derived nothing" and "no floor
    # ran" are different facts, and the gate downstream tells them apart.
    assert result.summary_account["stage"] == acquisition_floor.FLOOR_STAGE
    assert result.summary.calls_made == 0


def test_a_floor_that_does_not_fit_runs_no_calls_at_all(tmp_path, cfg):
    # All-or-nothing, in pre-flight: a partial floor is a gate minimum silently
    # not met for the hosts it never reached.
    budget = GatewayBudget(agent_total=8, floor_total=3)
    calls: list[dict] = []
    with pytest.raises(FloorBudgetInsufficientError) as exc:
        _floor(
            tmp_path,
            cfg,
            [
                FloorTarget("web-prod-04", "configuration_item"),
                FloorTarget("app-mq-01", "configuration_item"),
            ],
            budget=budget,
            src=sources(
                tmp_path,
                estate=[vm("web-prod-04")],
                broker_calls=calls,
            ),
        )
    assert budget.used == 0 and budget.floor_used == 0
    assert calls == []
    assert exc.value.stage_accounts == []


def test_a_floor_that_exactly_fits_runs(tmp_path, cfg):
    budget = GatewayBudget(agent_total=8, floor_total=2)
    result = _floor(
        tmp_path,
        cfg,
        [FloorTarget("web-prod-04", "configuration_item")],
        budget=budget,
        src=sources(tmp_path, estate=[vm("web-prod-04")]),
    )
    assert result.calls_made == 2
    assert budget.floor_remaining == 0


def test_a_gateway_defect_mid_floor_halts_and_keeps_the_calls_it_made(tmp_path, cfg):
    # The second target's Source-of-Truth lookup matches two records, which the
    # gateway refuses rather than treating as one host. The first target's two
    # calls are already recorded, and their accounts travel on the exception.
    # Two records under one name: NetBox does not enforce uniqueness, and the
    # gateway refuses to treat an ambiguous match as one host.
    estate = [vm("web-prod-04"), vm("app-mq-01"), {**vm("app-mq-01"), "id": 2}]
    with pytest.raises(FloorAcquisitionError) as exc:
        _floor(
            tmp_path,
            cfg,
            [
                FloorTarget("web-prod-04", "configuration_item"),
                FloorTarget("app-mq-01", "configuration_item"),
            ],
            src=sources(tmp_path, estate=estate, live_facts=("web-prod-04",)),
        )
    assert exc.value.gateway_error_type == "SoTAmbiguousMatchError"
    recorded = [
        a["tool_call"]
        for a in exc.value.stage_accounts
        if a.get("tool_call") is not None
    ]
    assert [c.budget_used for c in recorded] == [1, 2]
    assert all(c.acquisition_origin == "floor" for c in recorded)


def test_a_store_rejected_request_during_the_floor_is_a_defect_not_feedback(
    tmp_path, cfg, monkeypatch
):
    # F4's feedback arm belongs to the AGENT's loop: the floor's arguments are
    # composed in code, so there is nobody to hand a correction to.
    def reject(self, object_type, filters, *, limit, offset=0, fields=None):
        raise netbox_adapter.NetBoxRequestRejectedError("HTTP 400")

    monkeypatch.setattr(NetBoxAdapter, "get_objects", reject)
    with pytest.raises(FloorAcquisitionError) as exc:
        _floor(
            tmp_path,
            cfg,
            [FloorTarget("web-prod-04", "configuration_item")],
            src=sources(tmp_path),
        )
    assert exc.value.gateway_error_type == "StoreRejectedRequestError"


def test_the_summary_account_states_the_targets_their_sources_and_the_absences(
    tmp_path, cfg
):
    result = _floor(
        tmp_path,
        cfg,
        [
            FloorTarget("web-prod-04", "configuration_item"),
            FloorTarget("ghost-host-99", "objective"),
        ],
        src=sources(
            tmp_path,
            estate=[vm("web-prod-04")],
            live_facts=("web-prod-04",),
        ),
    )
    account = result.summary_account
    assert account["stage"] == acquisition_floor.FLOOR_STAGE
    assert account["status"] == "success"
    assert "floor_target:web-prod-04@configuration_item" in account["produced"]
    assert "floor_target:ghost-host-99@objective" in account["produced"]
    assert "floor_absent:ghost-host-99" in account["produced"]
    assert "floor_calls:4" in account["produced"]
    assert account["absent"].artifact == "sot_host_record"
    assert "ghost-host-99" in account["absent"].reason

    summary = account["acquisition_floor"]
    assert list(summary.positions) == [1, 2, 3, 4]
    assert [(t.name, t.source_field, t.sot_absent) for t in summary.targets] == [
        ("web-prod-04", "configuration_item", False),
        ("ghost-host-99", "objective", True),
    ]

    # Every kwargs dict the floor produced is a valid stage account once the
    # daemon adds what only it may supply.
    for kwargs in (account, *result.stage_accounts):
        StageAccount(
            schema_version=1,
            timestamp="2026-08-10T00:00:00Z",
            mode=ExecutionMode.SIMULATION,
            record_version=1,
            **kwargs,
        )


def test_the_summary_carries_the_reassessment_round(tmp_path, cfg):
    result = _floor(
        tmp_path,
        cfg,
        [FloorTarget("web-prod-04", "configuration_item")],
        src=sources(tmp_path, estate=[vm("web-prod-04")]),
        round_number=2,
    )
    assert result.summary.round == 2
    assert all(a["tool_call"].round == 2 for a in result.stage_accounts)


def test_the_floor_writes_nothing(tmp_path, cfg):
    # Producer, never a writer: the daemon commits, and a tick that dies
    # mid-floor leaves no write-once artifact behind to collide with.
    runs = tmp_path / "runs"
    runs.mkdir()
    _floor(
        tmp_path,
        cfg,
        [FloorTarget("web-prod-04", "configuration_item")],
        src=sources(tmp_path, estate=[vm("web-prod-04")]),
    )
    assert list(runs.iterdir()) == []


# --- the invoke seam ---------------------------------------------------------------


def _propose(hosts=(), gaps=()):
    return json.dumps(
        {
            "action": "propose",
            "proposal": {
                "scoped_inventory": [
                    {
                        "hostname": name,
                        "evidence_refs": list(refs),
                        "confidence": {
                            "identity_match": "HIGH",
                            "application_mapping": "MEDIUM",
                            "evidence_sufficiency": "MEDIUM",
                        },
                    }
                    for name, refs in hosts
                ],
                "candidate_mappings": [],
                "gaps": [{"subject": s, "reason": r, "note": n} for s, r, n in gaps],
            },
        }
    )


GAPS_ONLY = _propose(gaps=(("the request", "NO_DATA", "nothing matched"),))


class Agent:
    def __init__(self, plan):
        self.plan = list(plan)
        self.prompts: list[str] = []

    def __call__(self, role, prompt, *, config):
        if role == "classifier":
            return "CLEAN"
        self.prompts.append(prompt)
        assert self.plan, "the agent was called more times than scripted"
        outcome = self.plan.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


def _invoke(tmp_path, agent, cfg, contract_, *, budget=None, src=None, round_number=0):
    runs = tmp_path / "runs"
    runs.mkdir(exist_ok=True)
    return context_scope.invoke(
        runs,
        CID,
        contract_,
        cfg,
        budget=budget or GatewayBudget(agent_total=8, floor_total=8),
        sources=src if src is not None else sources(tmp_path),
        screenings_dir=tmp_path / "screenings",
        call_model=agent,
        round_number=round_number,
    )


def _data_block(prompt: str) -> dict[str, Any]:
    return json.loads(
        prompt.split("<<<UNTRUSTED_CONTENT")[1].split("UNTRUSTED_CONTENT>>>")[0]
    )


def test_floor_evidence_is_in_the_first_data_block_and_labelled(tmp_path, cfg):
    agent = Agent([_propose(hosts=(("web-prod-04", (1,)),))])
    run = _invoke(
        tmp_path,
        agent,
        cfg,
        contract(configuration_item="web-prod-04"),
        src=sources(
            tmp_path,
            estate=[vm("web-prod-04")],
            live_facts=("web-prod-04",),
        ),
    )
    assert run.halted is False
    block = _data_block(agent.prompts[0])
    entries = block["rounds"]
    assert [e["call"] for e in entries] == [1, 2]
    assert [e["acquisition"] for e in entries] == ["floor", "floor"]
    assert [e["tool"] for e in entries] == [
        context_gateway.SOT_HOST_BY_NAME_TOOL,
        context_gateway.LIVE_FACTS_TOOL,
    ]
    assert entries[0]["typed_facts"]["hostname"] == "web-prod-04"


def test_the_template_explains_what_a_floor_labelled_entry_is(tmp_path):
    # The label is only honest if the deterministic framing says what it means.
    # Both templates, because acquisition may already be closed when the agent
    # first sees the floor's results.
    for template in (context_scope.SCOPE_TEMPLATE, context_scope.SCOPE_FINAL_TEMPLATE):
        rendered = context_scope.prompt_templates.render(template, "x")
        assert '"acquisition"' in rendered
        assert '"acquisition": "floor"' in rendered
        assert '"acquisition": "agent"' in rendered


def test_floor_positions_precede_every_agent_position(tmp_path, cfg):
    agent = Agent(
        [
            json.dumps(
                {
                    "action": "call_tool",
                    "tool": "patch_history_for_host",
                    "arguments": {"hostname": "web-prod-04"},
                }
            ),
            _propose(hosts=(("web-prod-04", (1,)),)),
        ]
    )
    run = _invoke(
        tmp_path,
        agent,
        cfg,
        contract(configuration_item="web-prod-04"),
        src=sources(
            tmp_path,
            estate=[vm("web-prod-04")],
            live_facts=("web-prod-04",),
        ),
    )
    calls = run.proposal.tool_calls
    assert [(c.position, c.acquisition_origin) for c in calls] == [
        (1, "floor"),
        (2, "floor"),
        (3, "agent"),
    ]


def test_a_reused_proposal_runs_no_floor_at_all(tmp_path, cfg):
    src = sources(
        tmp_path,
        estate=[vm("web-prod-04")],
        live_facts=("web-prod-04",),
    )
    contract_ = contract(configuration_item="web-prod-04")
    first = _invoke(
        tmp_path, Agent([_propose(hosts=(("web-prod-04", (1,)),))]), cfg, contract_, src=src
    )
    assert first.floor_summary is not None

    calls: list[dict] = []
    unreachable = sources(tmp_path, estate=[], broker_calls=calls)
    second = _invoke(
        tmp_path,
        Agent([]),  # a script with nothing in it: any model call fails the test
        cfg,
        contract_,
        src=unreachable,
    )
    assert second.result_facts["scope_proposal_status"] == "reused"
    assert calls == []
    assert second.floor_summary is None
    # And no floor facts at all: a reused invocation ran none, so claiming a
    # target count of zero would be claiming a floor that did not happen.
    assert "floor_target_count" not in second.result_facts
    assert "floor_absent_targets" not in second.result_facts


def test_the_result_facts_name_the_targets_and_the_absences(tmp_path, cfg):
    agent = Agent([GAPS_ONLY])
    run = _invoke(
        tmp_path,
        agent,
        cfg,
        contract(configuration_item="web-prod-04 and ghost-host-99"),
        src=sources(tmp_path, estate=[vm("web-prod-04")]),
    )
    assert run.result_facts["floor_target_count"] == 2
    assert run.result_facts["floor_absent_targets"] == ["ghost-host-99"]


def test_a_floor_budget_shortfall_halts_before_any_model_call(tmp_path, cfg):
    agent = Agent([])  # any scope-agent call fails the test
    run = _invoke(
        tmp_path,
        agent,
        cfg,
        contract(configuration_item="web-prod-04 and app-mq-01"),
        budget=GatewayBudget(agent_total=8, floor_total=2),
        src=sources(tmp_path, estate=[vm("web-prod-04")]),
    )
    assert run.halted is True
    assert run.result_facts["context_scope_failure"] == "floor_budget_insufficient"
    assert agent.prompts == []
    assert scope_proposal.load(tmp_path / "runs", CID) is None
    defect = run.stage_accounts[-1]
    assert defect["stage"] == acquisition_floor.FLOOR_STAGE
    assert defect["status"] == "failed"
    assert defect["absent"].artifact == "scope_proposal"


def test_a_floor_gateway_defect_halts_before_any_model_call(tmp_path, cfg):
    agent = Agent([])
    estate = [vm("app-mq-01"), {**vm("app-mq-01"), "id": 2}]
    run = _invoke(
        tmp_path,
        agent,
        cfg,
        contract(configuration_item="app-mq-01"),
        src=sources(tmp_path, estate=estate),
    )
    assert run.halted is True
    assert run.result_facts["context_scope_failure"] == (
        "floor_gateway_error:SoTAmbiguousMatchError"
    )
    assert agent.prompts == []
    assert run.stage_accounts[-1]["stage"] == acquisition_floor.FLOOR_STAGE


def test_the_floor_summary_account_leads_the_calls_that_made_it(tmp_path, cfg):
    agent = Agent([GAPS_ONLY])
    run = _invoke(
        tmp_path,
        agent,
        cfg,
        contract(configuration_item="web-prod-04"),
        src=sources(tmp_path, estate=[vm("web-prod-04")]),
    )
    stages = [a["stage"] for a in run.stage_accounts]
    assert stages[0] == acquisition_floor.FLOOR_STAGE
    assert stages[1] == context_gateway.GATEWAY_STAGE


# --- Appendix C: every writer names the lane, provable by reading the source ---
#
# `acquisition_origin` is OPTIONAL on both durable records, so that a pre-M2.10
# artifact still loads. That optionality is exactly what lets a new writer omit
# it silently, and a value-level test only sees the paths it happens to drive.
# So the property is asserted on the SOURCE of the three modules that construct
# these records, with a planted offender proving the scan can fail.

import ast  # noqa: E402

ORCHESTRATOR_DIR = pathlib.Path(context_scope.__file__).resolve().parent

# Every module that constructs a durable call record. A fourth would have to be
# added here to pass, which is the point: the list is the claim.
WRITER_SOURCES = {
    "context_gateway.py": ORCHESTRATOR_DIR / "context_gateway.py",
    "acquisition_floor.py": ORCHESTRATOR_DIR / "acquisition_floor.py",
    "context_scope.py": ORCHESTRATOR_DIR / "context_scope.py",
}

RECORD_TYPES = ("ToolCall", "ExecutedCallRecord")


def _unlabelled_constructions(source: str) -> list[str]:
    """Every ToolCall / ExecutedCallRecord construction in `source` that does
    not pass acquisition_origin, as "<Type> at line N"."""
    offenders = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = (
            func.attr
            if isinstance(func, ast.Attribute)
            else func.id
            if isinstance(func, ast.Name)
            else None
        )
        if name not in RECORD_TYPES:
            continue
        if not any(kw.arg == "acquisition_origin" for kw in node.keywords):
            offenders.append(f"{name} at line {node.lineno}")
    return offenders


@pytest.mark.parametrize("name", sorted(WRITER_SOURCES))
def test_every_call_record_writer_names_its_lane(name):
    source = WRITER_SOURCES[name].read_text(encoding="utf-8")
    assert _unlabelled_constructions(source) == [], (
        f"{name} constructs a durable call record without acquisition_origin"
    )


def test_at_least_one_construction_exists_in_each_writer():
    # A scan that finds nothing passes vacuously. This is the positive control:
    # each module really does construct one of these records.
    for name, path in WRITER_SOURCES.items():
        constructed = [
            node
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in RECORD_TYPES
        ]
        assert constructed, f"{name} constructs no call record at all"


def test_the_scan_catches_a_planted_offender():
    planted = "ToolCall(tool='t', source='s', result_digest='d', budget_used=1)"
    assert _unlabelled_constructions(planted) == ["ToolCall at line 1"]
    labelled = (
        "ToolCall(tool='t', acquisition_origin='floor', source='s', "
        "result_digest='d', budget_used=1)"
    )
    assert _unlabelled_constructions(labelled) == []


def test_a_second_invocation_after_a_halt_re_runs_the_floor_cleanly(tmp_path, cfg):
    """The floor is idempotent by having no state: it writes nothing, so an
    invocation that halted before persisting a proposal can simply be run again,
    and the second floor records the same calls at the same positions with no
    collision of any kind."""
    contract_ = contract(configuration_item="web-prod-04")
    src = lambda: sources(  # noqa: E731 - a factory, so each run gets a session
        tmp_path,
        estate=[vm("web-prod-04")],
        live_facts=("web-prod-04",),
    )

    first = _invoke(
        tmp_path, Agent(["not json at all"]), cfg, contract_, src=src()
    )
    assert first.halted is True
    assert first.result_facts["context_scope_failure"] == "unparseable_response"
    assert first.floor_summary is not None
    assert scope_proposal.load(tmp_path / "runs", CID) is None

    second = _invoke(
        tmp_path,
        Agent([_propose(hosts=(("web-prod-04", (1,)),))]),
        cfg,
        contract_,
        src=src(),
    )
    assert second.halted is False
    assert second.floor_summary is not None
    assert list(second.floor_summary.positions) == list(first.floor_summary.positions)
    assert [c.position for c in second.proposal.tool_calls] == [1, 2]
