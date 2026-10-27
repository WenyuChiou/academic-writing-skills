"""Fixture/routing integrity only; actual reader judgments are assessed separately."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / 'skills/academic-writing-skills/references'


def test_concern_controls_are_hypothetical_and_readable():
    packet = json.loads((ROOT / 'evals/comment_concern_cases.json').read_text(encoding='utf-8'))
    assert len(packet['cases']) == 6
    assert len({case['id'] for case in packet['cases']}) == 6
    for case in packet['cases']:
        for field in ('id', 'comment', 'current_context', 'source_limit'):
            assert isinstance(case[field], str) and case[field].strip()
        assert case['original_selection'] is None or isinstance(case['original_selection'], str)


def test_one_existing_comment_record_supplies_all_three_routes():
    target = 'comment-scoped-revision.md#test-concern-closure-separately-from-edit-completion'
    for name in ('execution-and-acceptance.md', 'reviewer-response-workflow.md'):
        assert target in (GUIDES / name).read_text(encoding='utf-8')
    guide = (GUIDES / 'comment-scoped-revision.md').read_text(encoding='utf-8')
    assert 'evidence-context-cases.md#13-a-rewrite-is-not-concern-closure' in guide
    assert 'evals/comment_concern_cases.json' in (GUIDES / 'evidence-context-cases.md').read_text(encoding='utf-8')
