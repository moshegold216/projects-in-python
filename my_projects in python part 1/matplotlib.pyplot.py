import matplotlib.pyplot as plt
# ראשית תלת מימד זה הצגת גרף ע"י כמה קווים או אופציות למשל 2 קווים לאור ך\לרוחב אנחנו נשתמש בו בשביל להציכ נתונים של מון  ונתשתמש בתיקיית מאט וכו' כי זוהי תיקייה של יצירת גרפים ופםיילוט זה היצירה בפועל
import numpy as np # פקודת יבוא הנפיי שזה תקייה לניהול ליסט + חישוביים מתמטיקאים
from mpl_toolkits.mplot3d import Axes3D

# x = np.array([2023, 2024, 2025,2026,])
# y = np.array([20, 19, 30,40])
#  רשימה של מטספלויט בלי  חישובים מיותרים

years = np.array([2023, 2024, 2025,2026])
student = np.array([5, 19, 6,4])*2 #*4#*4   חישוב של כפול
gib = np.array([5,20,7,4])*2
plt.title("count of students")
plt.plot(years,student)
plt.plot(years,gib)
plt.xlabel("year")
plt.ylabel("count of students")
plt.grid()
plt.show()


# היום נלמד על הכלי NMPUY שזה רשימות +חישובים מתמטיקיים
# וזה הכלי המתמטיקי נפייי
