import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

CSV_PATH = "my_csv.csv"
SEP = ","          # אצלך זה פסיק
INTERVAL_MS = 150  # מהירות אנימציה

# ---------- טוען קובץ + נירמול שמות עמודות ----------
def load_df():
    df = pd.read_csv(CSV_PATH, sep=SEP)
    df.columns = df.columns.str.strip().str.lower()  # למשל 126.x במקום 126.X
    if "time" in df.columns:
        df = df.sort_values("time")
    return df

# ---------- מזהה אוטומטית איזה "מסלולים" קיימים ----------
def detect_tracks(columns):
    tracks = set()
    cols = set(columns)

    for c in cols:
        if c.endswith(".x"):
            base = c[:-2]  # בלי ".x"

            # ✅ הגבלה: רק מספרים, עד 7 ספרות
            if not re.fullmatch(r"\d{1,7}", base):
                continue

            if f"{base}.y" in cols and f"{base}.z" in cols:
                tracks.add(base)

    return sorted(tracks)


df = load_df()
tracks = detect_tracks(df.columns)

if "time" not in df.columns:
    raise ValueError("חסר עמודה TIME בקובץ (אחרי נירמול זה צריך להיות 'time').")

if not tracks:
    raise ValueError("לא נמצאו עמודות בסגנון N.x N.y N.z (לדוגמה 125.x 125.y 125.z).")

# ---------- מכין נתונים ----------
t = df["time"].to_numpy()

data = {}  # track_id -> dict עם x,y,z
for tr in tracks:
    data[tr] = {
        "x": df[f"{tr}.x"].to_numpy(dtype=float),
        "y": df[f"{tr}.y"].to_numpy(dtype=float),
        "z": df[f"{tr}.z"].to_numpy(dtype=float),
    }

# ---------- גבולות צירים לכל המסלולים יחד ----------
all_x = np.concatenate([np.nan_to_num(data[tr]["x"], nan=np.nan) for tr in tracks])
all_y = np.concatenate([np.nan_to_num(data[tr]["y"], nan=np.nan) for tr in tracks])
all_z = np.concatenate([np.nan_to_num(data[tr]["z"], nan=np.nan) for tr in tracks])

xmin, xmax = np.nanmin(all_x), np.nanmax(all_x)
ymin, ymax = np.nanmin(all_y), np.nanmax(all_y)
zmin, zmax = np.nanmin(all_z), np.nanmax(all_z)

# ---------- ציור ----------
fig = plt.figure(figsize=(12, 8), dpi=120)
ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)

# יוצר לכל track קו + נקודה (אוטומטי)
lines = {}
points = {}

for tr in tracks:
    line, = ax.plot([], [], [], lw=2, label=tr)
    pt,   = ax.plot([], [], [], marker="o")
    lines[tr] = line
    points[tr] = pt

ax.legend(title="Tracks")

current_i = -1

def update(_):
    global current_i, df, t, data

    # טוען מחדש כדי לתמוך ב-live (אם הקובץ מתעדכן)
    df_new = load_df()
    t_new = df_new["time"].to_numpy()

    # עדכון מסלולים (במקרה שנוספו/השתנו ערכים)
    # אם נוספו עמודות חדשות באמצע — פה נשארים עם אותם tracks שזוהו בתחילה.
    # (אפשר גם לזהות מחדש כל פעם, אבל זה כבד יותר.)
    for tr in tracks:
        # אם חסר משהו בקובץ החדש, מדלגים עליו
        xcol, ycol, zcol = f"{tr}.x", f"{tr}.y", f"{tr}.z"
        if xcol not in df_new.columns or ycol not in df_new.columns or zcol not in df_new.columns:
            continue
        data[tr]["x"] = df_new[xcol].to_numpy(dtype=float)
        data[tr]["y"] = df_new[ycol].to_numpy(dtype=float)
        data[tr]["z"] = df_new[zcol].to_numpy(dtype=float)

    n = len(t_new)
    if n == 0:
        return list(lines.values()) + list(points.values())

    if current_i < n - 1:
        current_i += 1

    i = current_i

    # מעדכן כל מסלול
    for tr in tracks:
        x = data[tr]["x"]
        y = data[tr]["y"]
        z = data[tr]["z"]

        # אם יש NaN בנקודה הנוכחית - פשוט לא מזיז נקודה (אפשר גם לדלג)
        if i >= len(x):
            continue

        # לוקחים רק ערכים תקינים עד i
        xs = x[:i + 1]
        ys = y[:i + 1]
        zs = z[:i + 1]

        mask = ~np.isnan(xs) & ~np.isnan(ys) & ~np.isnan(zs)

        if np.any(mask):
            lines[tr].set_data(xs[mask], ys[mask])
            lines[tr].set_3d_properties(zs[mask])

        # נקודה נוכחית – רק אם היא תקינה
        if not (np.isnan(x[i]) or np.isnan(y[i]) or np.isnan(z[i])):
            points[tr].set_data([x[i]], [y[i]])
            points[tr].set_3d_properties([z[i]])

    ax.set_title(f"Live 3D Track | TIME = {t_new[i]}")
    return list(lines.values()) + list(points.values())

ani = FuncAnimation(fig, update, interval=INTERVAL_MS, blit=False, repeat=False)
plt.show()
