"""The number check. Runs on every pull request, and anyone can run it: `python3 tools/check.py`.

It does four things:
1. Every row of data (shared/caps.csv, each study's data/ and budget/) names its sources, and every
   source it names has a row in shared/sources.csv with a link and the date it was read.
   A missing or unknown source fails the check.
2. It reruns each study's models and lists every number on the page that would move.
   Moving numbers don't fail the check; they're what a reviewer needs to see.
3. It redraws the charts from the data and says which ones would change.
4. It checks that the files read cleanly: CSVs parse, maps are closed polygons, dates are dates.

Options:
  --against <git ref>  compare with the numbers on that branch, e.g. origin/main (what the page shows now)
  --update             write the new values into numbers.csv and redraw the charts (for the maintainer)
  --charts-out <dir>   also write redrawn charts that changed to this folder
  --page <file>        also confirm each number appears in a built page (the study's HTML)
"""
import argparse
import csv
import datetime
import glob
import html
import importlib
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commons import ROOT, fmt, path, read_csv  # noqa: E402

STUDIES = sorted(d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, "numbers.csv")))
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Report:
    def __init__(self):
        self.failures, self.moves, self.notes, self.charts = [], [], [], []

    def fail(self, where, msg):
        self.failures.append((where, msg))


def rel(p):
    return os.path.relpath(p, ROOT)


def check_sources(rep):
    rows = read_csv("shared", "sources.csv")
    ids = {}
    for i, r in enumerate(rows, 2):
        where = f"shared/sources.csv line {i}"
        sid = (r.get("id") or "").strip()
        if not sid:
            rep.fail(where, "a source with no id")
            continue
        if sid in ids:
            rep.fail(where, f"source id `{sid}` is used twice")
        ids[sid] = r
        if not (r.get("url") or "").startswith(("http://", "https://")):
            rep.fail(where, f"source `{sid}` needs a link")
        read = (r.get("read") or "").strip()
        if not DATE.match(read):
            rep.fail(where, f"source `{sid}` needs the date it was read, as YYYY-MM-DD")
        else:
            try:
                if datetime.date.fromisoformat(read) > datetime.date.today() + datetime.timedelta(days=1):
                    rep.fail(where, f"source `{sid}` was read on a future date")
            except ValueError:
                rep.fail(where, f"source `{sid}` has an impossible date, {read}")
    if len(ids) < 10:
        rep.fail("shared/sources.csv", f"only {len(ids)} sources read; the file is probably broken")
    return ids


def data_files():
    files = [path("shared", "caps.csv")]
    for s in STUDIES:
        files += sorted(glob.glob(path(s, "data", "*.csv")))
    return files


def check_data(rep, sources):
    """Every data row names at least one source, and every source it names exists."""
    n = 0
    for f in data_files():
        with open(f, newline="") as fh:
            rows = list(csv.DictReader(fh))
        if not rows:
            rep.fail(rel(f), "no rows")
            continue
        if "source_ids" not in rows[0]:
            rep.fail(rel(f), "needs a `source_ids` column")
            continue
        for i, r in enumerate(rows, 2):
            n += 1
            label = r.get("id") or r.get("metric") or r.get("address") or r.get("bridge_no") or f"row {i}"
            check_row_sources(rep, f"{rel(f)} line {i} ({label})", r.get("source_ids", ""), sources, required=True)
            if "value" in r:
                try:
                    float(r["value"])
                except ValueError:
                    rep.fail(f"{rel(f)} line {i}", f"`{r['value']}` isn't a number")
    if n < 20:
        rep.fail("data", f"only {n} data rows read; the files are probably broken")


def check_row_sources(rep, where, cell, sources, required):
    ids = [s.strip() for s in (cell or "").split(";") if s.strip()]
    if required and not ids:
        rep.fail(where, "a number with no source: add its source to shared/sources.csv and its id here")
    for s in ids:
        if s not in sources:
            rep.fail(where, f"source `{s}` has no row in shared/sources.csv")


def check_budgets(rep, sources, values, update=False):
    for s in STUDIES:
        for f in sorted(glob.glob(path(s, "budget", "*.csv"))):
            rows = read_csv(rel(f))
            quoted, waiting, changed = 0.0, 0, False
            for i, r in enumerate(rows, 2):
                where = f"{rel(f)} line {i} ({r.get('line')})"
                status = r.get("status", "")
                if status == "needs a quote":
                    waiting += 1
                    check_row_sources(rep, where, r.get("source_ids"), sources, required=False)
                elif status == "quoted":
                    check_row_sources(rep, where, r.get("source_ids"), sources, required=True)
                    try:
                        quoted += float(r["amount_usd_low"] or r["amount_usd_high"])
                    except ValueError:
                        rep.fail(where, "a quoted line needs an amount")
                elif status == "range":
                    for col, key in (("amount_usd_low", "phase_one_low"), ("amount_usd_high", "phase_one_high")):
                        want = values.get(s, {}).get(f"cost.{key}")
                        if want is not None and abs(float(r[col]) - round(want / 1e7) * 1e7) > 1:
                            rep.moves.append((s, f"budget total {col}", fmt(float(r[col]), "usd_m"), fmt(want, "usd_m10"), rel(f)))
                            r[col], changed = str(round(want / 1e7) * 10_000_000), True
                else:
                    rep.fail(where, "status must be `needs a quote`, `quoted` or `range`")
            if update and changed:
                with open(f, "w", newline="") as fh:
                    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
                    w.writeheader()
                    w.writerows(rows)
            rep.notes.append(f"{rel(f)}: {waiting} lines still need a quote" + (f"; quoted so far {fmt(quoted, 'usd_m')}" if quoted else ""))


def check_maps(rep):
    files = glob.glob(path("shared", "maps", "*.geojson")) + [f for s in STUDIES for f in glob.glob(path(s, "maps", "*.geojson"))]
    if not files:
        rep.fail("maps", "no maps found")
    for f in files:
        try:
            with open(f) as fh:
                g = json.load(fh)
        except ValueError as e:
            rep.fail(rel(f), f"doesn't read as JSON: {e}")
            continue
        for k, feat in enumerate(g.get("features", [])):
            geom = feat.get("geometry") or {}
            polys = [geom.get("coordinates", [])] if geom.get("type") == "Polygon" else geom.get("coordinates", [])
            for poly in polys:
                for ring in poly:
                    if len(ring) < 4 or ring[0] != ring[-1]:
                        rep.fail(rel(f), f"feature {k} ({feat.get('properties', {}).get('name')}) has a ring that isn't closed")
                    if any(not (-180 <= p[0] <= 180 and -90 <= p[1] <= 90) for p in ring):
                        rep.fail(rel(f), f"feature {k} has a point that isn't [longitude, latitude]")


def run_models(study, rep):
    """{"model.number": value} for every model in the study."""
    mdir = path(study, "models")
    sys.path.insert(0, mdir)
    out, charts = {}, {}
    try:
        for f in sorted(glob.glob(os.path.join(mdir, "*.py"))):
            name = os.path.splitext(os.path.basename(f))[0]
            if name.startswith("_"):
                continue
            try:
                mod = importlib.import_module(name)
                for k, v in mod.numbers().items():
                    out[f"{name}.{k}"] = v
                charts.update(getattr(mod, "CHARTS", {}))
            except Exception as e:  # a broken model is a failure, not a crash
                rep.fail(rel(f), f"the model didn't run: {type(e).__name__}: {e}")
    finally:
        sys.path.remove(mdir)
    return out, charts


def resolve(study, src, values):
    kind, _, ref = src.partition(":")
    if kind == "model":
        return values.get(ref)
    if kind == "data":
        fname, _, metrics = ref.partition(":")
        rows = {r["metric"]: float(r["value"]) for r in read_csv(study, "data", fname)}
        return sum(rows[m] for m in metrics.split("+"))
    raise KeyError(src)


def numbers_at(ref, study):
    """numbers.csv as it is on a git ref, or None if it isn't there."""
    try:
        text = subprocess.run(["git", "show", f"{ref}:{study}/numbers.csv"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return {r["id"]: r for r in csv.DictReader(io.StringIO(text))}


def page_text(file):
    with open(file) as fh:
        t = fh.read()
    t = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def check_numbers(rep, study, values, against, update, page):
    f = path(study, "numbers.csv")
    rows = read_csv(study, "numbers.csv")
    base = numbers_at(against, study) if against else None
    text = page_text(page) if page else None
    for i, r in enumerate(rows, 2):
        where = f"{study}/numbers.csv line {i} ({r['id']})"
        try:
            v = resolve(study, r["from"], values)
        except (KeyError, FileNotFoundError) as e:
            rep.fail(where, f"can't find `{r['from']}` ({e})")
            continue
        if v is None:
            rep.fail(where, f"no model gives `{r['from']}`")
            continue
        try:
            now = fmt(v, r["format"])
        except KeyError:
            rep.fail(where, f"unknown format `{r['format']}`")
            continue
        was = (base or {}).get(r["id"], r)["shown"] if base is not None else r["shown"]
        if base is not None and r["id"] not in base:
            rep.moves.append((study, r["id"], "(new)", now, r["where"]))
        elif now != was:
            rep.moves.append((study, r["id"], was, now, r["where"]))
        r["shown"] = now
        if text is not None and now not in text and now.replace("$", "") not in text:
            rep.notes.append(f"{study}: `{now}` ({r['id']}) isn't on the page you passed")
    if update:
        with open(f, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)


def check_charts(rep, charts, update, out_dir):
    for target, draw in charts.items():
        new = draw()
        try:
            with open(path(target)) as fh:
                old = fh.read()
        except FileNotFoundError:
            old = None
        if new != old:
            rep.charts.append(target)
            if update:
                with open(path(target), "w") as fh:
                    fh.write(new)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
                with open(os.path.join(out_dir, os.path.basename(target)), "w") as fh:
                    fh.write(new)


def markdown(rep):
    out = ["## Number check", ""]
    if rep.failures:
        out += [f"**{len(rep.failures)} problem{'s' if len(rep.failures) != 1 else ''} to fix before this can merge:**", ""]
        out += [f"- `{w}`: {m}" for w, m in rep.failures] + [""]
    else:
        out += ["Every number has a source, and every file reads cleanly.", ""]
    if rep.moves:
        out += ["**Numbers on the page that would move:**", "", "| Study | Number | Now | Would be | Where on the page |", "| --- | --- | --- | --- | --- |"]
        out += [f"| {s} | `{i}` | {a} | {b} | {w} |" for s, i, a, b, w in rep.moves] + [""]
    else:
        out += ["No number on the page would move.", ""]
    out += [f"**Charts that would change:** {', '.join(f'`{c}`' for c in rep.charts)}" if rep.charts else "No chart would change.", ""]
    out += [f"- {n}" for n in rep.notes]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--against")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--charts-out")
    ap.add_argument("--page")
    a = ap.parse_args()
    rep = Report()
    if not STUDIES:
        rep.fail("repo", "no study folder with a numbers.csv was found")
    sources = check_sources(rep)
    check_data(rep, sources)
    check_maps(rep)
    values = {}
    for s in STUDIES:
        values[s], charts = run_models(s, rep)
        check_numbers(rep, s, values[s], a.against, a.update, a.page)
        check_charts(rep, charts, a.update, a.charts_out)
    check_budgets(rep, sources, values, a.update)
    md = markdown(rep)
    print(md)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(md)
    sys.exit(1 if rep.failures else 0)


if __name__ == "__main__":
    main()
