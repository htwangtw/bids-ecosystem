class: center middle

# The BIDS Ecosystem
### Christopher J. Markiewicz
#### Center for Reproducible Neuroscience
#### Stanford University

###### [effigies.github.io/bids-ecosystem](https://effigies.github.io/bids-ecosystem)

---
name: footer
layout: true

<div class="slide-slug">BIDS Ecosystem - Neuro Data Science School - May 2020</div>

---

# Outline

1. BIDS Review

2. BIDS Validator

3. PyBIDS

4. BIDS-Apps

5. Derivatives

6. Case Study: FitLins/Neuroscout

---
layout: true
template: footer
name: BIDS

# BIDS: Brain Imaging Data Structure

---
layout: true
template: BIDS

.pull-left[![Bids Layout](assets/bids.png)]

---

.pull-right[
* BIDS is a directory structure, based on common practices

* Builds on existing standards (NIfTI, JSON, TSV)

* Intended for human *and* machine legibility

* The [BIDS Validator](https://bids-standard.github.io/bids-validator)
  makes compliance easy to verify

* The [specification](https://bids-specification.readthedocs.io/en/stable/)
  is a searchable HTML document
]

---

.pull-right[

* Basic metadata in the file names

  * Subject, session, imaging modality, etc.
  * Generally just enough to assign unique names

]

---
count: false

.pull-right[
* Basic metadata in the file names
  * Subject, session, imaging modality, etc.
  * Generally just enough to assign unique names

* NIfTI headers and JSON sidecars contain detailed,
  image-related metadata

]

---
count: false

.pull-right[
* Basic metadata in the file names
  * Subject, session, imaging modality, etc.
  * Generally just enough to assign unique names

* NIfTI headers and JSON sidecars contain detailed,
  image-related metadata

* [`dataset_description.json`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#dataset_descriptionjson),
  [`participants.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file),
  [`sessions.tsv`](https://bids-specification.readthedocs.io/en/stable/05-longitudinal-and-multi-site-studies.html#sessions-file),
  and [`scans.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file)
  record study-level metadata that may not be associated
  with specific images
]

---
layout: true
template: footer

---

# Bidsification

Constructing a BIDS dataset can be tedious and error-prone, so there are several
[converters](https://bids.neuroimaging.io/benefits.html#converters).

<figure style="width: 60%">
![:img DICOM to BIDS conversion, 100%](assets/dicom-reorganization-transparent-black_1000x477.png)
</figure>

DICOM images store their relevant metadata internally, but naming conventions tend
to be scanner/institution-specific.

The [Heuristic DICOM Converter](https://heudiconv.readthedocs.io/) (HeuDiConv) and
[bidsify](https://github.com/NILAB-UvA/bidsify) allow you to specify the mapping and
apply in bulk. Both build off of [dcm2niix](https://github.com/rordenlab/dcm2niix/).

---

# Bidsification: ReproIn

The [ReproIn](https://github.com/ReproNim/reproin) project aims to
standardize scanner conventions, to eliminate the need to rewrite these mappings.

<figure style="width: 60%">
![:img ReproIn conversion schema, 100%](assets/dbic-conversions_cropped.png)
<figcaption>From <a href="https://github.com/ReproNim/reproin/blob/master/README.md#overall-workflow">ReproIn</a>;
doi:![:doi](10.5281/zenodo.3625000)</figcaption>
</figure>

---

.install-cmd[
```Bash
npm install -g bids-validator
```
]

# BIDS Validator

The machine-readable structure makes validation possible:

```Bash
$ bids-validator /data/bids/openneuro/ds000228
bids-validator@1.5.3

        1: [WARN] Task scans should have a corresponding events.tsv file. If this is a resting state scan you can ignore this warning or rename the task to include the word "rest". (code: 25 - EVENTS_TSV_MISSING)
                ./sub-pixar001/func/sub-pixar001_task-pixar_bold.nii.gz
                ./sub-pixar002/func/sub-pixar002_task-pixar_bold.nii.gz
                ./sub-pixar003/func/sub-pixar003_task-pixar_bold.nii.gz
                ./sub-pixar004/func/sub-pixar004_task-pixar_bold.nii.gz
                ./sub-pixar005/func/sub-pixar005_task-pixar_bold.nii.gz
                ./sub-pixar006/func/sub-pixar006_task-pixar_bold.nii.gz
                ./sub-pixar007/func/sub-pixar007_task-pixar_bold.nii.gz
                ./sub-pixar008/func/sub-pixar008_task-pixar_bold.nii.gz
                ./sub-pixar009/func/sub-pixar009_task-pixar_bold.nii.gz
                ./sub-pixar010/func/sub-pixar010_task-pixar_bold.nii.gz
                ... and 145 more files having this issue (Use --verbose to see them all).
...
```

.center[
## https://bids-standard.github.io/bids-validator/
]

---
layout: true
template: footer

.install-cmd[
```Bash
pip install pybids
```
]

---

# PyBIDS

A common specification of neuroimaging datasets affords queries for and
adaptation to the available data.

[PyBIDS](https://github.com/bids-standard/pybids/) is a Python library for
querying and manipulating BIDS datasets.


```Python
>>> from bids import BIDSLayout
>>> layout = BIDSLayout('/data/bids/openneuro/ds000228')
>>> bold = layout.get(subject='pixar002', suffix='bold', extension='nii.gz')
>>> bold
[<BIDSImageFile filename='/data/bids/openneuro/ds000228/sub-pixar002/func/sub-pixar002_task-pixar_bold.nii.gz'>]
>>> md = bold[0].get_metadata()
>>> md['RepetitionTime']
2
>>> bold[0].get_entities()
{'datatype': 'func',
 'extension': 'nii.gz',
 'subject': 'pixar002',
 'suffix': 'bold',
 'task': 'pixar'}
```

---

# PyBIDS - File queries

`get` queries return all matching files:

```Python
>>> layout.get(subject='pixar002')
[<BIDSJSONFile filename='/data/bids/openneuro/ds000228/sub-pixar002/anat/sub-pixar002_T1w.json'>,
 <BIDSImageFile filename='/data/bids/openneuro/ds000228/sub-pixar002/anat/sub-pixar002_T1w.nii.gz'>,
 <BIDSJSONFile filename='/data/bids/openneuro/ds000228/sub-pixar002/func/sub-pixar002_task-pixar_bold.json'>,
 <BIDSImageFile filename='/data/bids/openneuro/ds000228/sub-pixar002/func/sub-pixar002_task-pixar_bold.nii.gz'>]
```

--

Operating over a set of files is straightforward:

```Python
# Correct image headers from BIDS metadata
for bold_series in layout.get(suffix='bold', extension='nii.gz'):
    img = bold_series.get_image()  # Returns nibabel image object
    zooms = img.header.get_zooms()
    zooms[3] = bold_series.get_metadata()['RepetitionTime']
    img.header.set_zooms(zooms)
    img.to_filename(bold_series)
```

---

# PyBIDS - Entity queries

Each file has a set of associated entities, such as `subject`, `task`, `suffix` or `extension`.
You can query the layout for what entities exist for *any* file:

```Python
>>> layout.get_subjects()
['pixar001',
 'pixar002',
 ...
 'pixar155']
>>> layout.get_tasks()
['pixar']
>>> layout.get_suffixes(subject=bids.layout.Query.ANY)
['bold', 'T1w']
```

--

A full list of possible entities can be found:

```Python
>>> list(layout.get_entities(metadata=False))
['subject',
 'session',
 'task',
 'acquisition',
 'ceagent',
  ...
]
```

---

# PyBIDS - Metadata queries

BIDS has [The Inheritance Principle](https://bids-specification.readthedocs.io/en/v1.3.0/02-common-principles.html#the-inheritance-principle):

> Any metadata file [...] may be defined at any directory level [...]. The values from the top level are inherited by all lower levels unless they are overridden by a file at the lower level.

For example, in ds000228:

.left-column-mid[
* `task-pixar_bold.json`

```JSON
{
    "EchoTime": 0.03,
    "RepetitionTime": 2,
    "MagneticFieldStrength": 3,
    "dcmmeta_slice_dim": 2,
    ...
}
```
]
.right-column-mid[
* `sub-pixar001/func/sub-pixar001_task-pixar_bold.json`

```JSON
{
    "FlipAngle": 90,
    ...
}
```
]

---

# PyBIDS - Metadata queries

PyBIDS applies the inheritance principle, so metadata spread throughout the
dataset is associated with each relevant file:

```Python
>>> bold_file = layout.get(subject='pixar001', suffix='bold',
...                        extension=['nii', 'nii.gz'])[0]
>>> md = bold_file.get_metadata()
>>> md.keys()
dict_keys(['CogAtlasID', 'EchoTime', 'EffectiveEchoSpacing', 'FlipAngle',
           'MagneticFieldStrength', 'Manufacturer', ...])
>>> md['EchoTime']
0.03
>>> md['FlipAngle']
90
```

Many metadata terms are optional in BIDS, so queries that may work smoothly
in one dataset, or on one file, may fail on others:

```Python
>>> md['SliceEncodingDirection']
KeyError: "Metadata term 'SliceEncodingDirection' unavailable for file /data/bids/openneuro/ds000228/sub-pixar001/func/sub-pixar001_task-pixar_bold.nii.gz."
```

---

# PyBIDS - Metadata queries

Like filename entities, metadata entities get convenience methods:

```Python
>>> layout.get_FlipAngles()
[7, 84, 88, 89, 90]
```

--

These can be constrained to answer (maybe) interesting questions:

```Python
>>> layout.get_suffix(FlipAngle=7)
['T1w']
>>> layout.get_suffix(FlipAngle=88)
['bold']
>>> layout.get_FlipAngle(suffix='bold')
[84, 88, 89, 90]
```

--

How common is each?

```Python
>>> {fa: len(layout.get(FlipAngle=fa))
     for fa in layout.get_FlipAngle(suffix='bold')}
{84: 1, 88: 1, 89: 1, 90: 152}
>>> layout.get_subjects(FlipAngle=88)
['pixar028']
```

---
layout: true
template: footer

.install-cmd[
```Bash
datalad clone ///openneuro/ds000224
```
]

---

# PyBIDS - Tabular data

The Midnight Scan Club dataset contains a lot of tabular data, so we will use that:

```Python
>>> layout = BIDSLayout('/data/bids/openneuro/ds000224')
```

--

TSV files can be accessed just like NIfTI files, and their contents loaded as
[Pandas](https://pandas.pydata.org/) dataframes:

```Python
>>> participants = layout.get(suffix='participants', extension='tsv')[0]
>>> participants
<BIDSDataFile filename='/data/bids/openneuro/ds000224/participants.tsv'>
>>> participants.get_df()
  participant_id gender  age education_degree  education_years
0      sub-MSC01      M   34        Doctorate             22.0
1      sub-MSC02      M   34        Doctorate             28.0
...
9      sub-MSC10      M   31     Professional             19.0
```

---

# PyBIDS - Tabular data

PyBIDS can also aggregate file metadata along with the `get_collections()` method:

```Python
>>> collections = layout.get_collections(level='dataset')
>>> collections
[<bids.variables.collections.BIDSVariableCollection at 0x7f5e1b6467f0>]
```

This object is useful for manipulating the data programmatically, such as when
running [BIDS Statistical Models](https://bids.neuroimaging.io/bep002).

--

For a more familiar interface, dataframes are retrievable:

```Python
>>> collections[0].to_df()
         suffix subject age education_degree education_years gender
0  participants   MSC01  34        Doctorate              22      M
1  participants   MSC02  34        Doctorate              28      M
...
9  participants   MSC10  31     Professional              19      M
```

Note the suffix of the containing file is now a column, and the subject
column has replaced `participant_id` (and the `sub-` has been dropped).

---

# PyBIDS - Tabular data

The `'subject'` level shows the subject's `sessions.tsv`:

```Python
>>> layout.get_collections(level='subject', subject='MSC01')[0].to_df()
     session    suffix subject             acq_time
0     func01  sessions   MSC01  1894-08-25T01:07:51
1     func02  sessions   MSC01  1894-08-26T00:09:21
...
11  struct02  sessions   MSC01  1894-06-29T00:12:09
```

--

The `'session'` level shows the scans in the session:

```Python
>>> layout = BIDSLayout('/data/bids/openneuro/ds000224')
>>> layout.get_collections(level='session', subject='MSC01', session='func01')[0].to_df()
           task suffix  ...      TaskName             acq_time
0  glasslexical   bold  ...  glasslexical  1894-08-25T02:44:47
1  glasslexical   bold  ...  glasslexical  1894-08-25T02:53:17
2         motor   bold  ...         motor  1894-08-25T02:37:34
3         motor   bold  ...         motor  1894-08-25T03:00:54

[4 rows x 30 columns]
```

Note that metadata from `*_bold.json` (`TaskName` + ~20 columns) is also here.

---

# PyBIDS - Tabular data

The `'run'` level collects data from `events.tsv`, `*_physio.tsv.gz`, `*_stim.tsv.gz` or
`*_regressors.tsv`.

```Python
>>> layout.get_collections(level='run', subject='MSC01', session='func01',
                           task='motor', run=1)[0].to_df()
    task suffix subject  run  duration  onset session datatype trial_type
0  motor   bold   MSC01    1      15.4    8.8  func01     func      RHand
1  motor   bold   MSC01    1      15.4   24.2  func01     func      RFoot
2  motor   bold   MSC01    1      15.4   55.0  func01     func      LFoot
3  motor   bold   MSC01    1      15.4   70.4  func01     func     Tongue
...
```

---
layout: true
template: footer

---

# PyBIDS - Generating data

PyBIDS has the capability to generate filenames, if you need to add metadata to a
dataset.

```Python
>>> import json
>>> entities = {"task": "rest", "suffix": "bold", "extension": "json"}
>>> layout.build_path(entities)
/data/bids/openneuro/ds000228/task-rest_bold.json
>>> layout.write_contents_to_file(
...     entities, contents=json.dumps({"Instructions": "Just relax."}))
```

Adding entities produces more complex filenames.

--

Summaries of the data can also be generated.

```Python
>>> from bids.report import BIDSReport
>>> reports = BIDSReport(layout).generate()
>>> print(reports.most_common()[0][0])
For session None:
	MR data were acquired using a 3-Tesla Siemens TrioTim MRI scanner.
	Zero runs of pixar single-echo fMRI data were collected (32 slices in interleaved descending order; repetition time, TR=2000ms; echo time, TE=30ms; flip angle, FA=90<deg>; field of view, FOV=192x192mm; matrix size=64x64; voxel size=3x3x3.3mm). Each run was 5:36 minutes in length, during which 168 functional volumes were acquired.

Dicoms were converted to NIfTI-1 format. This section was (in part) generated automatically using pybids (0.10.2).
```

---

# PyBIDS - Final thoughts

Many grad students have written a large subset of the preceding for their own labs.

* File structure, mirroring inputs/outputs of the preferred tool suite (FreeSurfer, AFNI, etc.)

--
* A metadata folder, file or database, containing study parameters and individual subject/session details

--
* A library of functions for fetching files, metadata, computing data, and saving results

--

Each lab's pipelines are inevitably idiosyncratic, and to reproduce with someone else's data,
the data must be reformatted to fit code expectations, or the code must be modified to handle
the new structure.

--

By standardizing on a data structure, code written to that structure gains stability and
broad applicability.


---
layout: true
template: footer
name: Apps

# BIDS Applications

---

A common specification of neuroimaging datasets affords queries for and
adaptation to the available data.

--

Queryable (meta)data allows a very simple protocol for a
[BIDS App](https://bids-apps.neuroimaging.io/apps/):

```Bash
bids-app /bids-directory /output-directory participant [OPTIONS]
```

.footnote[
\* Note that `participant` is an analysis level. Apps may also operate
at the `run`, `session` or `group` levels.
]

--

## Examples

**MRIQC**

```Bash
mriqc /data/bids/openneuro/ds000228 /data/processed/ds000228-mriqc group
```

--

**fMRIPrep**

```Bash
fmriprep /data/bids/openneuro/ds000228 /data/processed/ds000228-fmriprep \
    participant --participant-label pixar001
```

---

.pull-left[
### Many application types are possible
]
.pull-right[
[![:img BIDS App list, 100%](assets/bids-apps.png)](https://bids-apps.neuroimaging.io/apps/)
]

---
count: false

.pull-left[
### Many application types are possible

* Quality control

]
.pull-right[
[![:img BIDS QC Apps, 100%](assets/bids-apps-qc.png)](https://bids-apps.neuroimaging.io/apps/)
]

---
count: false

.pull-left[
### Many application types are possible

* Quality control

* Anatomical pipelines

]
.pull-right[
[![:img BIDS Anatomical Apps, 100%](assets/bids-apps-anatomical.png)](https://bids-apps.neuroimaging.io/apps/)
]

---
count: false

.pull-left[
### Many application types are possible

* Quality control

* Anatomical pipelines

* Functional pipelines

]
.pull-right[
[![:img BIDS Functional Apps, 100%](assets/bids-apps-functional.png)](https://bids-apps.neuroimaging.io/apps/)
]

---
count: false

.pull-left[
### Many application types are possible

* Quality control

* Anatomical pipelines

* Functional pipelines

* Diffusion pipelines

]
.pull-right[
[![:img BIDS Diffusion Apps, 100%](assets/bids-apps-diffusion.png)](https://bids-apps.neuroimaging.io/apps/)
]

---
count: false

.pull-left[
### Many application types are possible

* Quality control

* Anatomical pipelines

* Functional pipelines

* Diffusion pipelines

### Lowered friction encourages adoption

* Researchers gain easy access to tools by formatting data
  in BIDS

* Accepting BIDS datasets makes your tools easy to try

]
.pull-right[
[![:img BIDS App list, 100%](assets/bids-apps.png)](https://bids-apps.neuroimaging.io/apps/)
]

---
layout: true
template: footer

# Example: Summarize scan parameters

A [short program](assets/example-bids-app.py) to summarize variations in scan parameters across subjects.

---
---
count: false

```Python
import sys
from pathlib import Path
from bids import BIDSLayout
from bids.reports import BIDSReport
```

Import some BIDS tools and Python libraries.

---
count: false

```Python
import sys
from pathlib import Path
from bids import BIDSLayout
from bids.reports import BIDSReport

cmd, bids_root, out_root, analysis_level, *opts = sys.argv
layout = BIDSLayout(bids_root)
```

Collect the command-line arguments to implement the BIDS Apps protocol.

There are libraries to help add options, but this is the heart of it.

---
count: false

```Python
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
```

Generate a report per subject. Add the subject to a list associated with
report text.

---
count: false

```Python
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
```

Write the number of scans parameter sets to a report file, then
for each set...

---
count: false

```Python
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
```

... report which subjects had the same parameters, and what they were.

---

To run the app:

```Bash
python ./example-bids-app.py /data/ds000228 /data/out/ds000228-example group
```

Output ([download](assets/report.txt)):

```text
Scan parameter sets detected: 9

-----
Parameter set detected for subjects: pixar001, pixar002, pixar003, pixar008, pixar009, pixar010, pixar011, pixar013, pixar014, pixar015, pixar016, pixar017, pixar018, pixar020, pixar021, pixar022, pixar023, pixar024, pixar025, pixar026, pixar027, pixar029, pixar030, pixar031

For session None:
	MR data were acquired using a 3-Tesla Siemens TrioTim MRI scanner.
	T1-weighted structural MRI data were collected (192 slices; repetition time, TR=2530ms; echo time, TE=1.64ms; flip angle, FA=7°; field of view, FOV=176x192mm; matrix size=176x192; voxel size=1x1x1mm).
	Zero runs of pixar single-echo fMRI data were collected (32 slices in interleaved descending order; repetition time, TR=2000ms; echo time, TE=30ms; flip angle, FA=90°; field of view, FOV=192x192mm; matrix size=64x64; voxel size=3x3x3.3mm). Each run was 5:36 minutes in length, during which 168 functional volumes were acquired.
...
```

--

In a more complicated application, you might modulate processing based on these differences.

---
layout: true
template: Apps

---

For development and distribution, BIDS Apps encourages a continuous-integration
(CI) approach.

<figure style="width: 75%">
![:img BIDS App creation, 100%](assets/bids-app-creation.png)
<figcaption>From doi:![:doi](10.1371/journal.pcbi.1005209.g001)</figcaption>
</figure>

---

BIDS Apps use the notion of analysis levels, which provide natural opportunities for
parallelism.

<figure style="width: 100%">
![:img BIDS App workflow, 100%](assets/bids-app-workflow.png)
<figcaption>From doi:![:doi](10.1371/journal.pcbi.1005209.g002)</figcaption>
</figure>

---
layout: true
template: footer

# BIDS Apps and Reproducibility

---

Start-to-finish pipelines aid in performing *reproducible* analyses.

<figure style="width: 60%; display: block; margin-left: auto; margin-right: auto">
![:img Reproducibility matrix, 100%](assets/ReproducibleMatrix.jpg)
<figcaption>From <a href="https://the-turing-way.netlify.app/reproducibility/03/definitions.html#The-Turing-Way-definition-of-reproducibility">The
Turing Way, Ch. 2</a>; doi:![:doi](10.5281/zenodo.3233853)</figcaption>
</figure>

--

Open analysis on open data is subject to independent reproduction.

--

Accepting BIDS datasets makes *replicating* results on independent data easier.

---

* Container technologies partially address environmental sources of
  variability &mdash; see, *e.g.*,
  [Gronenschild, et al. (2012)](https://doi.org/10.1371/journal.pone.0038234
   "The Effects of FreeSurfer Version, Workstation Type, and Macintosh Operating
   System Version on Anatomical Volume and Cortical Thickness Measurements")
  or [Glatard, et al. (2015)](https://doi.org/10.3389/fninf.2015.00012
   "Reproducibility of neuroimaging analyses across operating systems")

--

* The uniform interface also eases deployment to HPC or cloud environments
  like [CBRAIN](http://mcin.ca/technology/cbrain/) or
  [AWS Batch](https://aws.amazon.com/batch/).

--

* The output of a BIDS App is a *derivative* dataset. The BIDS standard is
[being extended](https://bids-specification.readthedocs.io/en/derivatives/05-derivatives/01-introduction.html)
to describe many types of derivatives, with a focus on derivatives that
can be reused in yet more BIDS apps.

---
layout: true
template: footer
name: Derivatives

# BIDS Derivatives

---


#### Dataset-level metadata is stored in augmented [`dataset_description.json`](https://bids-specification.readthedocs.io/en/derivatives/05-derivatives/01-introduction.html#derived-dataset-and-pipeline-description):

* `PipelineDescription` contains references to the code (including version)
  that produced the derivative dataset.
* `SourceDatasets` is a list of references to the specific version of the
  dataset analyzed

--

#### Basic metadata remains in filenames

```
fmriprep/sub-01/func/sub-01_task-rest_space-fsaverage_hemi-L.func.gii
```

--

#### Additional metadata in [sidecar JSON files](https://bids-specification.readthedocs.io/en/derivatives/05-derivatives/01-introduction.html#common-file-level-metadata-fields)

* `Sources` direct inputs to the process that produced the file
* `CoordinateSystem` indicates the coordinate system of image files
* Metadata of source files that still apply should be preserved
* Metadata of source files that no longer apply must be removed

---

Derivatives generally fall into three categories:

1. Preprocessed images (or otherwise transformed data) that can be used for further
  analysis

  * Tissue segmentations
  * Normalized BOLD series
  * Fitted diffusion model parameters

--

2. Measures of statistics of interest

  * Parcellation statistics
  * Local functional connectivity density
  * Fractional anisotropy

--

3. Figures and reports for assessing the quality of data/processing

  * Surface reconstruction plots
  * Brain-extraction mask overlays
  * Susceptibility distortion correction before/after

---
template: footer

# Conclusion


---
layout: true
template: footer

class: center middle

---

# Questions?

##### [effigies.github.io/bids-ecosystem](https://effigies.github.io/bids-ecosystem)
