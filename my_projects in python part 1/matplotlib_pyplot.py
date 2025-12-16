import matplotlib.pyplot as plt

# x = [0,1,2,3,4,5,6,]
# y = [-1,1,5,3,5,2,3]
# z = [-2,1,4,2,4,1,]
# c = [1,1,4,2,4,1,]
x = [0,4,15, 25, 30]
y = [1,25,5, 25, 0]
y2 = [2,24,4, 24, -1]


# plt.plot(x,y,z,c)
plt.plot(x,y)
plt.plot(x,y2)
plt.title("example for baruch ")
plt.xlim(0,30)
plt.ylim(0,30)
plt.xlabel("x")
plt.ylabel("y")

# plt.legend(x,y)
plt.grid()
plt.show()
#  היום אנחנו נלמד על יצירת גרפים נשתמש בספרייה מטאפלוטליב  ספרייה בפייתון שבה ניתן ליצור גריפם ובתוכה יה תיקייה בשם .פיילוט שזה כלי ציור וכו