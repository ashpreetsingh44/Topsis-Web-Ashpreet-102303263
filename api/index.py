
import pandas as pd
import numpy as np
from io import StringIO

def topsis(df, weights, impacts):
    data = df.iloc[:,1:].astype(float)
    norm = np.sqrt((data**2).sum())
    weighted = (data / norm) * weights
    best = []
    worst = []
    for i in range(len(impacts)):
        if impacts[i] == '+':
            best.append(weighted.iloc[:,i].max())
            worst.append(weighted.iloc[:,i].min())
        else:
            best.append(weighted.iloc[:,i].min())
            worst.append(weighted.iloc[:,i].max())
    best = np.array(best)
    worst = np.array(worst)
    d1 = np.sqrt(((weighted - best)**2).sum(axis=1))
    d2 = np.sqrt(((weighted - worst)**2).sum(axis=1))
    score = d2 / (d1 + d2)
    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)
    return df

def handler(request):
    if request.method == "GET":
        html = '''
        <html><body>
        <h2>TOPSIS Web Service</h2>
        <form method="POST" action="/api/index.py" enctype="multipart/form-data">
        CSV File: <input type="file" name="file" required><br><br>
        Weights: <input name="weights" value="1,1,1,1"><br><br>
        Impacts: <input name="impacts" value="+,+,-,+"><br><br>
        <button type="submit">Get Result</button>
        </form>
        </body></html>
        '''
        return html, 200, {"Content-Type": "text/html"}

    file = request.files.get("file")
    weights = list(map(float, request.form.get("weights").split(",")))
    impacts = request.form.get("impacts").split(",")

    df = pd.read_csv(StringIO(file.stream.read().decode()))
    result = topsis(df, weights, impacts)

    csv_out = result.to_csv(index=False)
    return csv_out, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=result.csv"
    }
