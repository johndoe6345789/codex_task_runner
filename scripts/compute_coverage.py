import glob, os, sys
react_files = glob.glob('frontend/src/fakemui/**/*.jsx', recursive=True)+glob.glob('frontend/src/fakemui/**/*.js', recursive=True)
react_names = set(os.path.splitext(os.path.basename(p))[0] for p in react_files)
qmldir_path='src/codex_task_runner/ui/qml/fakemui/qmldir'
if not os.path.exists(qmldir_path):
    print('qmldir not found', qmldir_path); sys.exit(1)
qml = open(qmldir_path).read()
qml_names = set()
for line in qml.splitlines():
    line=line.strip()
    if not line or line.startswith('#'): continue
    parts=line.split()
    qml_names.add(parts[0])
matched=[]
missing=[]
for rn in sorted(react_names):
    cname='C'+rn if not rn.startswith('C') else rn
    if cname in qml_names:
        matched.append((rn,cname))
    else:
        missing.append(rn)
print('React components found:',len(react_names))
print('QML registered components:',len(qml_names))
print('Matched:',len(matched))
print('Missing:',len(missing))
print('\nMatched list:')
for a,b in matched:
    print(a,'->',b)
print('\nMissing list:')
for m in sorted(missing):
    print(m)
