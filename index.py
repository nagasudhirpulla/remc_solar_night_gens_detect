from src.config.appConfig import loadAppConfig, getSolarGens
from src.services.scada_fetcher import fetchScadaPntRtData
import subprocess, os, platform
import datetime as dt
import jinja2

# this script will run at night, so check will be done on real time data

appConf = loadAppConfig()
solarGens = getSolarGens()

flaggedGenIndices:list[int] = []
# iterate on each solar generator
for gInd, g in enumerate(solarGens):
    # get real time data from historian
    genVal = fetchScadaPntRtData(g['actId'])
    # flag generator if value greater than 2 MW
    if genVal > appConf["solarGenThreshold"]:
        flaggedGenIndices.append(gInd)
        solarGens[gInd]["gen"] = genVal

# Report HTML template
templateStr = """<h1>Solar Generators with generation at Night hours on {{todayStr}}</h1>
<table class="table">
    <thead>
        <tr>
            <th>Generator</th>
            <th>Value</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        {% for item in violGens %}
        <tr>
            <td>{{item.name}}</td>
            <td>{{item.gen}}</td>
            <td>{{item.genType}}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
"""

# generate report from data
todayStr = dt.datetime.now().strftime("%d-%b-%Y")
context = {
    "todayStr": todayStr,
    "violGens": [solarGens[i] for i in flaggedGenIndices],
}
template = jinja2.Environment(
    loader=jinja2.BaseLoader
).from_string(templateStr)

reportText = template.render(context)

reportPath = f"reports/gens_{todayStr}.html"
with open(reportPath, mode='w') as f:
    f.write(reportText)

# open file in OS
if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', os.path.abspath(reportPath)))
elif platform.system() == 'Windows':    # Windows
    os.startfile(os.path.abspath(reportPath))
else:                                   # linux variants
    subprocess.call(('xdg-open', os.path.abspath(reportPath)))