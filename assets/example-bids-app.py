#!/usr/bin/env python
import sys
from pathlib import Path
from bids import BIDSLayout
from bids.reports import BIDSReport

cmd, bids_root, out_root, analysis_level, *opts = sys.argv
layout = BIDSLayout(bids_root)

reports = {}
for subject in layout.get_subjects():
    rep = list(BIDSReport(layout).generate(subject=subject))[0]
    reports.setdefault(rep, []).append(subject)

with open(Path(out_root) / "report.txt", "w") as out_file:
    out_file.write(f"Scan parameter sets detected: {len(reports)}\n\n")
    for rep, subs in reports.items():
        rep = "\n".join(rep.splitlines()[:-2])
        out_file.write(f"-----\nParameters for subjects: {', '.join(subs)}\n\n")
        out_file.write(rep.replace("<deg>", "°") + "\n\n")
