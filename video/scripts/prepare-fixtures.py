from pathlib import Path
import json, subprocess, shutil
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
OUT=ROOT/'public/documents'
OUT.mkdir(parents=True,exist_ok=True)
base={
 'demo':True,'employer':'Northwind Labs','role':'Software engineering intern','location':'Remote, United States','status':'kit ready',
 'verdict':'Worth considering','quote':'Coursework or a personal project in Python is welcome.','section':'Minimum qualifications',
 'fit':[{'requirement':'Python','state':'supported','evidence':'Built a Python tool to organize campus dining data for comparison.','source':'Supplied project notes'}],
 'resume_doc':{'name':'Maya Chen','sections':[
  {'title':'Education','lines':['B.S. Computer Science · Arizona State University','Expected May 2027 · Data Structures, Databases']},
  {'title':'Projects','entries':[{'title':'Campus Dining','subtitle':'Python · Personal project','bullets':['Built a Python tool to organize campus dining data for comparison.']}]}
 ]},
 'cover_doc':{'name':'Maya Chen','salutation':'Dear Northwind Labs team,','paragraphs':['I am applying for the software engineering intern role. My Campus Dining project uses Python to organize dining data for comparison. I would welcome the opportunity to bring that project experience to your team.'],'close':'Sincerely,','signature':'Maya Chen'},
 'prepared_answers':[{'q':'Earliest start','a':'May 2027.'}],
 'approval':{'package':'Waiting for you','form':'Not filled','submit':'Not approved','confirmed':'No'},
 'return_copy':"Return to Cubbie and reply 'use this package'."
}
(OUT/'package.json').write_text(json.dumps(base,indent=2))
subprocess.run([str(REPO/'.venv/bin/python'),str(REPO/'scripts/render_package.py'),'--input',str(OUT/'package.json'),'--out',str(OUT/'package.html')],check=True)
profile={'demo':True,'profile':{'name':'Maya Chen','education':'B.S. Computer Science, Arizona State University, expected May 2027','skills':['Python'],'evidence':[{'name':'Campus Dining','did':'Built a Python tool to organize campus dining data for comparison.','result':'A comparison tool; no usage metric claimed.'}]}}
(OUT/'profile.json').write_text(json.dumps(profile,indent=2))
subprocess.run([str(REPO/'.venv/bin/python'),str(REPO/'scripts/render_visual.py'),'card','--kind','profile','--input',str(OUT/'profile.json'),'--out',str(ROOT/'public/cards/profile.png')],check=True)
edit={'allowed_facts':'Maya Chen. Arizona State University. B.S. Computer Science. May 2027. Python. Data Structures. Databases. Built a Python tool to organize campus dining data for comparison. No professional experience claimed.','bank_projects':['Campus Dining'],'must_include':['Python'],'resume_slots':{'NAME':'Maya Chen','CONTACT':'Fictional sample profile.','SUMMARY':'Computer science student with a Python project.','EDUCATION':'B.S. Computer Science, Arizona State University. Expected May 2027. Coursework: Data Structures and Databases.','EXPERIENCE':'\\item Academic and personal projects only.','PROJECTS':'\\item Campus Dining: Built a Python tool to organize campus dining data for comparison.'},'cover_slots':{'ROLE':'I am applying for the software engineering intern role at Northwind Labs.','BODY':'My Campus Dining project uses Python to organize campus dining data for comparison. I would welcome the opportunity to discuss this project with your team.'}}
(OUT/'edit.json').write_text(json.dumps(edit,indent=2))
subprocess.run([str(REPO/'.venv/bin/python'),str(REPO/'scripts/tex_edit.py'),'--edit',str(OUT/'edit.json'),'--out-dir',str(OUT/'tex')],check=True)
for name in ['resume','cover-letter']:
 result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(OUT/'tex'),str(OUT/'tex'/f'{name}.tex')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (OUT/'tex'/f'{name}-build.log').write_text(result.stdout)
 if result.returncode: raise RuntimeError(result.stdout[-2000:])
 shutil.copy2(OUT/'tex'/f'{name}.pdf',OUT/('Resume.pdf' if name=='resume' else 'Cover letter.pdf'))
(OUT/'Project notes.txt').write_text('FICTIONAL SAMPLE — MAYA CHEN\nCampus Dining\nBuilt a Python tool to organize campus dining data for comparison.\nStudent confirmed this work in the illustrative fixture.\n')
transcript='''<!doctype html><html><body style="font-family:sans-serif;padding:50px;color:#173c2d"><p>FICTIONAL SAMPLE · NOT AN OFFICIAL TRANSCRIPT</p><h1>Coursework summary</h1><h2>Maya Chen</h2><p>B.S. Computer Science · Arizona State University</p><p>Expected May 2027</p><hr><h2>Relevant coursework</h2><p>Data Structures</p><p>Databases</p><p>No grades or student identification included.</p></body></html>'''
(OUT/'transcript.html').write_text(transcript)
print('Prepared fictional profile, actual review HTML, controlled-slot LaTeX, PDFs, and project notes.')
