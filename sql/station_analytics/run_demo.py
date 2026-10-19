"""Run a tiny SQLite analytics demo; uses only the Python standard library."""
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent


def load_queries() -> dict[str, str]:
    queries: dict[str, str] = {}
    name = None
    chunks: list[str] = []
    for line in (HERE / "queries.sql").read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name: "):
            if name is not None:
                queries[name] = "\n".join(chunks).strip()
            name = line[len("-- name: "):].strip()
            chunks = []
        elif name is not None:
            chunks.append(line)
    if name is not None:
        queries[name] = "\n".join(chunks).strip()
    return queries


def make_database() -> sqlite3.Connection:
    """Fresh in-memory database: no external dependencies or personal data."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((HERE / "seed.sql").read_text(encoding="utf-8"))
    return conn


def main() -> None:
    with make_database() as conn:
        for name, sql in load_queries().items():
            results = conn.execute(sql).fetchall()
            print(f"\n### {name} ({len(results)} rows)")
            for row in results[:8]:
                print(dict(row))
            if len(results) > 8:
                print(f"... {len(results) - 8} more rows")


if __name__ == "__main__":
    main()
