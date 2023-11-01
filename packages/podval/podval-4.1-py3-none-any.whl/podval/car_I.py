def num_1():
    print('''from sklearn.datasets import fetch_openml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
data = fetch_openml("debutanizer", version = 1)
print(data.keys())
print(data['DESCR'])
X = data.data
y = data.target''')
    
def num_2():
    print('''print(X.info())
data_df = pd.DataFrame(data.data, columns=data.feature_names)

columns, rows = data_df.shape
print(f"Число строк (объектов): {columns}")
print(f"Число столбцов (признаков): {rows}")

description = data_df.describe()
print(description)
    ''')
    
def num_3():
    print('''print(X.dtypes)
print(y.dtypes)

# Проверьте, являются ли признаки числовыми
# non_numeric_columns = data_df.select_dtypes(exclude=['number']).columns  #Возвращает подмножество столбцов DataFrame на основе типов столбцов.
# if not non_numeric_columns.empty:
#     print("Нечисловые колонки:")
#     print(non_numeric_columns)
# else:
#     print("Все признаки числовые.")

# # Если есть нечисловые колонки, их можно удалить
# if not non_numeric_columns.empty:
#     data_df = data_df.select_dtypes(include=['number'])
#     print("Нечисловые колонки удалены.")
X.hist(figsize = (12,7))
plt.show()

# for column in X:
#     print(X[column].unique().tolist())
    
# X = X.drop(['Название кол'], axis = 1)
    ''')
    
def num_4():
    print('''missing_values = data_df.isnull().sum().sum()
if missing_values > 0:
    print(f"В данных есть {missing_values} пропущенных значений.")
    data_df = data_df.fillna(data_df.median())
    print("Пропущенные значения заполнены медианными значениями.")
    
if y.isnull().sum() > 0:
    print("В целевой переменной есть пропущенные значения.")
#     y = y.fillna(y.median())
    ''')
    
def num_5():
    print('''y.hist(edgecolor='k')
plt.title("Гистограмма распределения целевой переменной")
plt.xlabel("Значения целевой переменной")
plt.ylabel("Частота")
plt.show()
#Вывод
# Нормальным (Гауссовым): Если гистограмма имеет форму колокола, центрированного вокруг среднего значения.

# Равномерным: Если все значения в целевой переменной имеют приблизительно одинаковую частоту.

# Экспоненциальным: Если гистограмма имеет форму убывающей экспоненты.

# Логнормальным: Если после логарифмического преобразования данных гистограмма становится более похожей на нормальное распределение.

# Другим видам распределения: В зависимости от данных, распределение может быть другим.
    ''')
    
def num_6():
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
steps, errors = mod.fit(X,y, alpha = 0.6, max_steps = 5000)

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

print(mod.wi)

print(mod.w0)
# Уравнение полученной гиперплоскости с помощью модели:
### $\bar Y = -4.587e-08\times X_0 + 1.03e-03\times X1 + 5.407e-07$

# Уравнение полученное с помощью МНК:
### $\bar Y = 0.018113\times X_0 - 0.036636\times X1 + 74.29021$

# X['intercept'] = 1
# B = np.linalg.inv((X.T @ X)) @ X.T @ y
# print(B)
# X = X.drop('intercept',axis = 1)class linear_reg:
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
steps, errors = mod.fit(X,y, alpha = 0.6, max_steps = 5000)

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

print(mod.wi)

print(mod.w0)
# Уравнение полученной гиперплоскости с помощью модели:
### $\bar Y = -4.587e-08\times X_0 + 1.03e-03\times X1 + 5.407e-07$

# Уравнение полученное с помощью МНК:
### $\bar Y = 0.018113\times X_0 - 0.036636\times X1 + 74.29021$

# X['intercept'] = 1
# B = np.linalg.inv((X.T @ X)) @ X.T @ y
# print(B)
# X = X.drop('intercept',axis = 1)
    ''')
    
def num_7():
    print('''model_sklearn = LinearRegression()

model_sklearn.fit(X, y)

intercept = model_sklearn.intercept_
coefficients = model_sklearn.coef_
print(intercept, coefficients)
    ''')
    
def num_8():
    print('''# MSE для модели из sklearn
MSE = mean_squared_error(model_sklearn.predict(X),y)
print(MSE)
# MSE для модели из sklearn
MSE1 = mean_squared_error(mod.predict(X),y)
print(MSE1)
# R^2 для модели из sklearn
r2 = r2_score(model_sklearn.predict(X),y)
print(r2)
# R^2 для модели из sklearn
r2_1 = r2_score(mod.predict(X),y)
print(r2_1)
# Выводы
# 1) Метрики показывают, что линейная регрессия не подходит для анализа данного датасета
# 2) Самописная модель не сходится именно на этих данных!!!!
# 3) Метод нахождения параметров с помощью матричного вида МНК сходится с результатами модели из sklearn
    ''')