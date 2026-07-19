# dynamo/log-report

A Terminal-Bench 2 (Harbor) task: parse an Apache-style access log into a small
JSON summary report at `/app/report.json`.

## Layout

```
log-report/
├── task.toml                 # TB2 Harbor task config
├── instruction.md            # the prompt given to the agent
├── environment/
│   ├── Dockerfile            # agent + verifier image (base pinned by @sha256)
│   └── access.log            # task input
├── solution/
│   ├── solve.sh              # oracle entrypoint
│   └── solve.py              # reference implementation
└── tests/
    ├── test.sh               # runs pytest, writes reward.txt + ctrf.json
    └── test_outputs.py       # one test per instruction.md success criterion
```

## Running

Requires Docker and Harbor (`uv tool install harbor`). From the repository root:

```bash
harbor run -p . -a oracle      # reference solution -> reward 1
harbor run -p . --agent nop    # no-op agent        -> reward 0
```

`-p` takes the directory *containing* the task directory, so `.` from the repo
root is correct — pointing it at `log-report/` itself finds no tasks.

## Expected results

| Agent | Reward | CTRF |
|---|---|---|
| `oracle` | 1.0 | 5 passed / 0 failed |
| `nop` | 0.0 | 0 passed / 5 failed |

Ground truth for the bundled `access.log`:

```json
{"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}
```

The verifier asserts these values directly, so creating an empty or placeholder
`/app/report.json` scores 0.
