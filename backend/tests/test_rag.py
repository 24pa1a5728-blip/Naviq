import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import pytest
from main import topological_sort

def load_services():
    with open("data/services.json", "r") as f:
        return json.load(f)

def test_urls_start_with_https():
    services = load_services()
    for s in services:
        assert s["official_portal"]["url"].startswith("https://")
        for step in s["steps"]:
            assert step["source"]["url"].startswith("https://")

def test_dependencies_exist():
    services = load_services()
    for s in services:
        step_ids = {step["id"] for step in s["steps"]}
        for step in s["steps"]:
            for dep in step.get("depends_on", []):
                assert dep in step_ids, f"Dependency {dep} not found in service {s['id']}"

def test_topological_sort_no_cycles():
    services = load_services()
    for s in services:
        sorted_steps = topological_sort(s["steps"])
        assert len(sorted_steps) == len(s["steps"])
        
def test_topological_sort_cycle_fails():
    bad_steps = [
        {"id": "a", "depends_on": ["b"]},
        {"id": "b", "depends_on": ["a"]}
    ]
    with pytest.raises(ValueError, match="Cycle detected"):
        topological_sort(bad_steps)
