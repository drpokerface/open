# library/ - the swarm's compiled wins: ratified playbooks and tools, copied into every seed workspace.

- `playbooks/` - one markdown recipe per task class, harvested from verified wins, with measured costs
- `tools/` - small self-contained, fault-proven .py utilities promoted from winning workspaces
- `proposals/` - harvest proposals awaiting the owner; review with: `python swarm.py library`
- `calibration.md` - the owner's own 0-10 scores of past deliverables (ground truth for judge taste)

Workers propose a harvest after each verified win (hostile-audited first); only the owner
ratifies. Ratified entries ride into every future seed workspace (minus `proposals/`),
where doctrine says: search the library first - reuse beats rebuild.
