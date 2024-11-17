def calculate_scores(answer, keywords=None):
    """
    応答のスコアを計算します。
    :param answer: ユーザーの回答（文字列）
    :param keywords: スコアリング用のキーワードリスト（デフォルトは空リスト）
    :return: スコア（整数）
    """
    if keywords is None:
        keywords = ["Python", "データ分析"]
    score = sum(1 for keyword in keywords if keyword in answer)
    return score * 10  # 10点単位でスコア化

if __name__ == "__main__":
    response = "Pythonとデータ分析が得意です。"
    print(calculate_scores(response))  # 出力: 20
