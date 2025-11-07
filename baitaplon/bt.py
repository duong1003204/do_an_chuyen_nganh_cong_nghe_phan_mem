from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# tải dữ liệu iris
iris = load_iris()
X, y = iris.data, iris.target

# chia dữ liệu: 2/3 train, 1/3 test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=42)

# tạo và huấn luyện mô hình Naive Bayes
model = GaussianNB()
model.fit(X_train, y_train)

# dự đoán
y_pred = model.predict(X_test)

# đánh giá
print("Độ chính xác:", accuracy_score(y_test, y_pred))
print("\nBáo cáo phân loại:\n", classification_report(y_test, y_pred, target_names=iris.target_names))
