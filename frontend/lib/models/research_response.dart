class SourceItem {
  final String title;
  final String url;

  SourceItem({
    required this.title,
    required this.url,
  });

  factory SourceItem.fromJson(Map<String, dynamic> json) {
    return SourceItem(
      title: json['title'] as String? ?? '',
      url: json['url'] as String? ?? '',
    );
  }
}

class ArticleItem {
  final String title;
  final String url;
  final String snippet;
  final String articleContent;
  final String articleSummary;

  ArticleItem({
    required this.title,
    required this.url,
    required this.snippet,
    required this.articleContent,
    required this.articleSummary,
  });

  factory ArticleItem.fromJson(Map<String, dynamic> json) {
    return ArticleItem(
      title: json['title'] as String? ?? '',
      url: json['url'] as String? ?? '',
      snippet: json['snippet'] as String? ?? '',
      articleContent: json['article_content'] as String? ?? '',
      articleSummary: json['article_summary'] as String? ?? '',
    );
  }
}

class ResearchResponse {
  final String question;
  final String summary;
  final List<String> keyPoints;
  final List<SourceItem> sources;
  final List<ArticleItem> articles;

  ResearchResponse({
    required this.question,
    required this.summary,
    required this.keyPoints,
    required this.sources,
    required this.articles,
  });

  factory ResearchResponse.fromJson(Map<String, dynamic> json) {
    return ResearchResponse(
      question: json['question'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      keyPoints: (json['key_points'] as List<dynamic>? ?? [])
          .map((item) => item.toString())
          .toList(),
      sources: (json['sources'] as List<dynamic>? ?? [])
          .map((item) => SourceItem.fromJson(item as Map<String, dynamic>))
          .toList(),
      articles: (json['articles'] as List<dynamic>? ?? [])
          .map((item) => ArticleItem.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }
}