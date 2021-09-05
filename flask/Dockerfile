# Python3 のイメージを使用して、イメージ構築
FROM python:3.5.3
# カレントディレクトリをイメージ内のパス /main に追加
ADD . /main
# 作業ディレクトリを /main に指定
WORKDIR /main
RUN pip install -r requirements.txt
CMD ["python", "app.py"]