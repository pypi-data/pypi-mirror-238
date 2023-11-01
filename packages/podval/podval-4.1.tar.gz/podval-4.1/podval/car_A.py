def task_1():
    print('''from sklearn.datasets import fetch_openml

# Загрузка датасета
dataset = fetch_openml(name='analcatdata_supreme')

# Вывод текстового описания
print(dataset.DESCR)

# Разделение данных на X и y
X = dataset.data
y = dataset.target''')

def task_2():
    print('''X.shape[1] # количество признаков
X.shape[0] # число строк
X.info()
X.describe().round(2)
X.hist(figsize = (12,7), bins = 15)
plt.show()''')


def task_3_oleg():
    print('''for column in ['Liberal', 'Unconstitutional', 'Precedent_alteration', 'Unanimous', 'Lower_court_disagreement']:
    print(X[column].unique().tolist())
X.dtypes
y.dtypes
X = X.drop(['Liberal', 'Unconstitutional', 'Precedent_alteration', 'Unanimous', 'Lower_court_disagreement'], axis = 1)
# работает лучше чем X.drop(, inplace = True)
#Последний столбец не категориальный
X.Actions_taken.unique().tolist()''')

def task_3():
    print('''df = pd.DataFrame(dataset.data, columns=dataset.feature_names)

# Вывод типа данных каждого признака
print("Типы данных признаков:")
print(df.dtypes)

# Вывод типа данных целевой переменной
print("Тип данных целевой переменной:")
print(dataset.target.dtype)
df = df.drop(['название_колонки'], axis=1)''')

def task_4_oleg():
    print('''X.isna().sum()
y.isna().sum()''')

def task_4():
    print('''df = pd.DataFrame(dataset.data, columns=dataset.feature_names)

# Проверка на пропущенные значения в признаках
if df.isnull().any().any():
    print("В данных есть пропущенные значения.")
else:
    print("В данных нет пропущенных значений.")

# Проверка на пропущенные значения в целевой переменной
if dataset.target.isnull().any():
    print("В целевой переменной есть пропущенные значения.")
else:
    print("В целевой переменной нет пропущенных значений.")
# Заполнение пропущенных значений медианными значениями
df = df.fillna(df.median())

# Заполнение пропущенных значений в целевой переменной медианным значением
dataset.target = dataset.target.fillna(dataset.target.median())''')

def task_5():
    print('''y.hist()
plt.show()''')

def task_6():
    print('''class linear_reg:
    def __init__(self):
        self.w0 = 0
        self.eps = 1e-4
        self.wi = np.array([])

    def error(self, X, Y):
        return sum(((self.predict(X) - Y)**2) / (2 * len(X)))

    def predict(self, X):
        return X @ self.wi + self.w0

    def fit(self, X, Y, alpha=1, max_steps=50000):
        X = np.array(X)
        Y = np.array(Y)
        self.wi = np.array([0.0] * X.shape[1])
        step = 0
        steps, errors = [], []
        for _ in range(max_steps):
            dJ0 = sum(self.predict(X) - Y) / X.shape[0]
            dJ1 = X.T @ (self.predict(X) - Y) / X.shape[0]
            self.w0 -= alpha * dJ0
            self.wi -= alpha * dJ1
            new_err = self.error(X, Y)
            step += 1
            steps.append(step)
            errors.append(new_err)
#             if step > 1 and abs(errors[step - 1] - errors[step - 2]) < self.eps:
#                 print('Модель перестала обучаться')
#                 break
        else:
            print('Модель обучилась успешно. Количество шагов закончилось.')

        return steps, errors
mod = linear_reg()
steps, errors = mod.fit(X,y, alpha = 0.0000001, max_steps = 100)

plt.plot(errors,label = 'Кривая ошибки')
plt.xlabel("Шаг обучения")
plt.ylabel("Ошибка")
plt.title('График обучения')
plt.legend()
plt.show()

plt.scatter(mod.predict(X),y, label = "Предсказание модели")
plt.plot(y,y,color = 'red', label = "Распределение целевой переменной")
plt.xlabel("Целевая переменная у")
plt.ylabel("Целевая переменная У")
plt.title('Распределение целевой переменной')
plt.legend()
plt.show()

#веса полученные моедлью
mod.wi
mod.w0

#Веса полученные с МНК в матричном виде
X['intercept'] = 1
B = np.linalg.inv((X.T @ X)) @ X.T @ y
B

#Удаление столбца Intercept (был необходим для расчёта параметров с помощью МНК)
X = X.drop('intercept',axis = 1)

for alph in [1,0.1,0.01,0.001,0.0001]:
    mod = linear_reg()
    steps, errors = mod.fit(X,y, alpha = alph, max_steps = 100)
    print(errors, "\n"*3)''')

def task_7():
    print('''from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)

_ = [print(k, v) for k, v in zip(X.columns, model.coef_)]

print("Intercept: \n", model.intercept_)''')

def task_8():
    print('''from sklearn.metrics import mean_squared_error, r2_score

# MSE для модели из sklearn
MSE = mean_squared_error(model.predict(X),y)
MSE

# MSE для модели из sklearn
MSE1 = mean_squared_error(mod.predict(X),y)
MSE1

# R^2 для модели из sklearn
r2 = r2_score(model.predict(X),y)
r2

# R^2 для модели из sklearn
r2_1 = r2_score(mod.predict(X),y)
r2_1''')
