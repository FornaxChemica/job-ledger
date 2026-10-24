# Resume rules

The script enforces these. Follow them when writing the edit file. Add tighter rules here as the team decides them. Do not put a real student's phone, email, or address in this public file.

- Start from `assets/resume-template.tex`. Change only the slot interiors.
- Name and contact text must be facts the student confirmed, copied into `allowed_facts`.
- Every bank project appears in the PROJECTS slot. Do not drop one to make room.
- A PROJECTS item names a bank project before the colon. Do not add a project that is not in the bank.
- An EXPERIENCE item names an employer that already appears in `allowed_facts`, before the `--`.
- Every number in a slot, including years and percents, already appears in `allowed_facts` or the bank text. Do not invent a metric.
- Do not add an employer, a title, a degree, or a tool the bank and the confirmed facts do not support.
- Every posting gets its own resume. Read that posting's skills and keywords. Each one the bank or the confirmed facts support goes in `must_include`, spelled the way the posting spells it. The resume must contain every phrase in `must_include`. A skill the student cannot support stays off the page. Do not borrow it from the posting to pass a keyword screen.
- One page. Short bullets. The lines for this role use the posting's wording. The other projects still appear, shorter if needed. If the compiled PDF runs past one page, shorten wording and edit again. Do not drop a bank project or a supported keyword to make it fit.
